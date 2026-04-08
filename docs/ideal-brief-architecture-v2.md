# IDEAL Brief: Last-Mile Architecture v2

## TL;DR

Sunday night cron generates the brief and creates a **Pull Request** (not a direct push). Monday morning, the human reviews and merges. The merge triggers GitHub Pages deploy, which fires a webhook to send the email **only after confirmed deployment**. Subscribers live in DynamoDB with idempotency keys to prevent double-sends. Total infrastructure cost: ~$10-15/month.

This revision addresses critical issues from Staff Engineer review:
1. Git-as-database anti-pattern → Content in separate repo, PR-based flow
2. Hope-based scheduling → Event-driven email triggered by deploy success
3. No human review → PR gate before any public distribution
4. S3 JSON subscribers → DynamoDB with ACID guarantees
5. NAT Gateway cost trap → Public subnet with locked-down security groups (Section 7.1)
6. Webhook replay attacks → API Gateway API Key required (Section 2.2)
7. No recovery playbook → Manual trigger documented (Section 6.5)
8. Regional preferences → Explicitly ignored in v1, full brief to all subscribers

---

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         GENERATION STAGE                                 │
│  EventBridge (Sun 11 PM ET) → ECS Fargate Task                          │
│                                                                         │
│  1. Run pipeline → briefs/YYYYMMDD/                                     │
│  2. Validate output (schema check)                                      │
│  3. Transform to Jekyll pages                                           │
│  4. Create Pull Request (not push to main)                              │
│  5. Send preview email to admin                                         │
│  6. Upload artifacts to S3 (for email sender)                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         REVIEW GATE (Human)                              │
│                                                                         │
│  Monday morning:                                                        │
│  - Admin receives preview email with PR link                            │
│  - Reviews generated content for hallucinations/errors                  │
│  - Merges PR (or requests changes via commit)                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         PUBLISH STAGE (Automated)                        │
│                                                                         │
│  PR Merge triggers:                                                     │
│  1. GitHub Actions builds Jekyll site                                   │
│  2. Deploys to GitHub Pages                                             │
│  3. Verifies deployment (curl health check)                             │
│  4. Fires webhook to API Gateway                                        │
│           │                                                             │
│           ▼                                                             │
│  5. Lambda sends digest email via SES                                   │
│     - Reads artifacts from S3                                           │
│     - Reads subscribers from DynamoDB                                   │
│     - Checks idempotency (sent_for_brief_id)                            │
│     - Sends with tracking configuration set                             │
└─────────────────────────────────────────────────────────────────────────┘
```

## 2. Key Architectural Decisions

### 2.1 PR-Based Review Gate

**Why**: LLMs hallucinate. A single bad headline ("President Zelenskyy Surrenders") blasted to journalists and policymakers is career-ending. The PR gate provides:

- **Human verification** before any public distribution
- **Audit trail** of what was reviewed and when
- **Rollback capability** via git revert
- **Diff visibility** showing exactly what's being published

**Implementation**:
```python
def create_review_pr(brief_dir: Path, meta: BriefMetadata) -> str:
    """Create PR instead of pushing directly to main."""
    branch_name = f"brief/{meta.date_slug}"

    # Create branch, add files, push
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", f"Brief: {meta.week_label}"], check=True)
    subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)

    # Create PR via GitHub CLI
    result = subprocess.run(
        ["gh", "pr", "create",
         "--title", f"Brief: {meta.week_label}",
         "--body", PR_BODY_TEMPLATE.format(meta=meta),
         "--base", "main",
         "--head", branch_name],
        capture_output=True, text=True, check=True
    )

    # Extract PR URL from output
    pr_url = result.stdout.strip()
    return pr_url

PR_BODY_TEMPLATE = """
## Brief Preview: {meta.week_label}

**Coverage period**: {meta.date_start} to {meta.date_end}
**Generated**: {meta.generated_at}

### Pre-merge checklist

- [ ] Executive summary is factually accurate
- [ ] No hallucinated events or quotes
- [ ] Leader names and titles are correct
- [ ] No inflammatory or potentially defamatory content
- [ ] Links resolve correctly

### Preview

View the rendered preview at: [Netlify Deploy Preview](will be auto-linked)

Or review the raw markdown files in the Files Changed tab.

---
*Merging this PR will deploy to production and trigger email distribution.*
"""
```

### 2.2 Event-Driven Email (Not Cron)

**Why**: Temporal coupling ("hope the deploy finishes before email sends") fails when:
- GitHub Actions has an outage
- Jekyll build fails on syntax error
- Network issues delay the push

**Implementation**: GitHub Actions workflow fires webhook on successful deploy:

```yaml
# .github/workflows/deploy-and-notify.yml
name: Deploy and Notify

on:
  push:
    branches: ["main"]
    paths: ["_briefs/**"]  # Only trigger on brief content changes

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate brief schema
        run: python scripts/validate_brief.py

      - name: Build Jekyll site
        uses: actions/jekyll-build-pages@v1

      - name: Check for broken links
        run: |
          npm install -g html-proofer
          htmlproofer ./_site --disable-external

      - uses: actions/upload-pages-artifact@v3

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    outputs:
      page_url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4

  notify:
    runs-on: ubuntu-latest
    needs: deploy
    steps:
      - name: Verify deployment is live
        run: |
          # Wait for CDN propagation
          sleep 30
          # Health check
          curl -f "${{ needs.deploy.outputs.page_url }}" || exit 1

      - name: Trigger email distribution
        run: |
          curl -X POST "${{ secrets.EMAIL_TRIGGER_WEBHOOK }}" \
            -H "Content-Type: application/json" \
            -H "x-api-key: ${{ secrets.API_GATEWAY_KEY }}" \
            -d '{"brief_date": "${{ github.event.head_commit.message }}", "deployed_url": "${{ needs.deploy.outputs.page_url }}"}'
```

**Webhook security**: API Gateway is configured to require an API key (`x-api-key` header) via a Usage Plan. This prevents replay attacks if the secret leaks—an attacker cannot spam the endpoint without the key. The Lambda also validates that `brief_date` corresponds to existing artifacts in S3, rejecting arbitrary payloads.

### 2.3 Separate Content Repository

**Why**: Mixing application code with volatile data creates:
- Bloated git history (thousands of "Publish brief" commits)
- Merge conflicts when fixing code during pipeline run
- Unclear separation of concerns

**Structure**:
```
ideal-brief-site/          # Code repo (templates, styles, config)
├── _config.yml
├── _layouts/
├── _includes/
├── assets/
├── scripts/
└── .github/workflows/

ideal-brief-content/       # Data repo (generated briefs only)
├── _briefs/
│   ├── 2026-02-08/
│   ├── 2026-02-01/
│   └── ...
└── _data/
    └── briefs_index.yml
```

**Build-time fetch**: The GitHub Actions workflow fetches content at build time:

```yaml
- name: Fetch brief content
  run: |
    git clone --depth 1 https://github.com/you/ideal-brief-content.git _content
    cp -r _content/_briefs ./_briefs
    cp -r _content/_data ./_data
```

**Alternative**: Git submodule (simpler but couples the repos more tightly).

**Dependency management**: The two-repo split creates a versioning risk. If you change the front matter schema in the content repo (e.g., rename `flag` to `emoji`), the site repo's Liquid templates will break. Mitigation: **Always merge site repo changes first, then regenerate content.** For a solo operator this is sufficient; a team would need pinned versions or schema validation in CI.

---

## 3. DynamoDB Schema

### 3.1 Subscribers Table

```
Table: ideal-brief-subscribers
├── Partition Key: email (String)
├── Attributes:
│   ├── subscribed_at (String, ISO8601)
│   ├── status (String: "active" | "unsubscribed" | "bounced" | "complained")
│   ├── unsubscribe_token (String, UUID)
│   ├── preferences (Map)  # NOTE: v1 ignores preferences, sends full brief to all
│   │   ├── frequency: "weekly" | "breaking"
│   │   └── regions: ["europe", "americas", ...]
│   ├── last_sent_brief_id (String, e.g., "2026-02-08")
│   └── updated_at (String, ISO8601)
└── GSI: status-index (for querying active subscribers)
```

**Why DynamoDB over S3 JSON**:
- **ACID transactions**: No race conditions on concurrent subscribe/unsubscribe
- **Conditional writes**: `last_sent_brief_id` enables idempotency
- **Query patterns**: Efficiently fetch only active subscribers
- **Cost**: ~$0.25/month at low scale (on-demand pricing)

### 3.2 Email Events Table

```
Table: ideal-brief-email-events
├── Partition Key: email (String)
├── Sort Key: event_timestamp (String, ISO8601)
├── Attributes:
│   ├── event_type (String: "send" | "open" | "click" | "bounce" | "complaint")
│   ├── brief_id (String)
│   ├── link_url (String, for click events)
│   └── metadata (Map)
└── TTL: 90 days (auto-expire old events)
```

### 3.3 Idempotency Pattern

```python
def send_to_subscriber(email: str, brief_id: str, html_body: str) -> bool:
    """
    Send email with idempotency guarantee.
    Returns True if sent, False if already sent.
    """
    try:
        # Conditional update: only proceed if last_sent_brief_id != this brief
        dynamodb.update_item(
            TableName="ideal-brief-subscribers",
            Key={"email": {"S": email}},
            UpdateExpression="SET last_sent_brief_id = :brief_id, updated_at = :now",
            ConditionExpression="attribute_not_exists(last_sent_brief_id) OR last_sent_brief_id <> :brief_id",
            ExpressionAttributeValues={
                ":brief_id": {"S": brief_id},
                ":now": {"S": datetime.utcnow().isoformat()},
            },
        )
    except dynamodb.exceptions.ConditionalCheckFailedException:
        # Already sent to this subscriber for this brief
        logger.info(f"Skipping {email}: already sent {brief_id}")
        return False

    # Proceed with send
    ses.send_email(...)
    return True
```

This prevents double-sends even if Lambda retries due to transient failures.

---

## 4. Email Sender Lambda

```python
"""
email_sender.py — Idempotent email distribution triggered by deploy webhook.
"""

import boto3
import json
import logging
from datetime import datetime

logger = logging.getLogger()
dynamodb = boto3.client("dynamodb")
ses = boto3.client("ses")
s3 = boto3.client("s3")

BUCKET = "ideal-brief-artifacts"
MAX_EMAIL_SIZE_KB = 90  # Stay under Gmail's 102KB clip threshold


def handler(event, context):
    """
    Triggered by API Gateway webhook from GitHub Actions.

    Event body: {"brief_date": "2026-02-08", "deployed_url": "https://..."}
    """
    body = json.loads(event["body"])
    brief_id = body["brief_date"]
    deployed_url = body["deployed_url"]

    logger.info(f"Processing email distribution for brief: {brief_id}")

    # 1. Load brief artifacts from S3
    artifacts = load_artifacts(brief_id)

    # 2. Render email HTML
    html_body = render_email(artifacts, deployed_url)

    # 3. Validate size (Gmail clipping prevention)
    if len(html_body.encode("utf-8")) > MAX_EMAIL_SIZE_KB * 1024:
        logger.warning(f"Email too large ({len(html_body)} bytes), truncating...")
        html_body = truncate_email(html_body, MAX_EMAIL_SIZE_KB * 1024)

    # 4. Fetch active subscribers
    subscribers = get_active_subscribers()
    logger.info(f"Found {len(subscribers)} active subscribers")

    # 5. Send with idempotency
    sent_count = 0
    skip_count = 0

    for subscriber in subscribers:
        email = subscriber["email"]

        # Personalize unsubscribe link
        personalized_html = html_body.replace(
            "{{unsubscribe_url}}",
            f"https://api.idealbrief.org/unsubscribe?token={subscriber['unsubscribe_token']}"
        )

        if send_to_subscriber(email, brief_id, personalized_html):
            sent_count += 1
        else:
            skip_count += 1

    logger.info(f"Distribution complete: {sent_count} sent, {skip_count} skipped (idempotent)")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "brief_id": brief_id,
            "sent": sent_count,
            "skipped": skip_count,
        })
    }


def get_active_subscribers() -> list[dict]:
    """Query DynamoDB for active subscribers."""
    response = dynamodb.query(
        TableName="ideal-brief-subscribers",
        IndexName="status-index",
        KeyConditionExpression="status = :active",
        ExpressionAttributeValues={":active": {"S": "active"}},
    )

    return [
        {
            "email": item["email"]["S"],
            "unsubscribe_token": item["unsubscribe_token"]["S"],
        }
        for item in response["Items"]
    ]


def send_to_subscriber(email: str, brief_id: str, html_body: str) -> bool:
    """Send with idempotency check."""
    try:
        dynamodb.update_item(
            TableName="ideal-brief-subscribers",
            Key={"email": {"S": email}},
            UpdateExpression="SET last_sent_brief_id = :brief_id, updated_at = :now",
            ConditionExpression="attribute_not_exists(last_sent_brief_id) OR last_sent_brief_id <> :brief_id",
            ExpressionAttributeValues={
                ":brief_id": {"S": brief_id},
                ":now": {"S": datetime.utcnow().isoformat()},
            },
        )
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        return False

    ses.send_email(
        Source="IDEAL Brief <brief@idealbrief.org>",
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": f"IDEAL Brief: Week of {brief_id}"},
            "Body": {"Html": {"Data": html_body}},
        },
        ConfigurationSetName="ideal-brief-tracking",
        Tags=[
            {"Name": "brief_id", "Value": brief_id},
        ],
    )
    return True
```

---

## 5. Edge Case Handling

### 5.1 Unsubscribe Forwarding Attack

**Problem**: User A forwards email to User B. User B clicks unsubscribe. User A gets unsubscribed.

**Solution**: Two-step unsubscribe with confirmation:

```python
# Lambda: unsubscribe_handler.py

def handler(event, context):
    token = event["queryStringParameters"]["token"]

    # Look up subscriber by token
    subscriber = get_subscriber_by_token(token)
    if not subscriber:
        return {"statusCode": 404, "body": "Invalid token"}

    # Show confirmation page (not instant unsubscribe)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": f"""
        <html>
        <body>
            <h1>Unsubscribe from IDEAL Brief</h1>
            <p>You are unsubscribing: <strong>{subscriber['email']}</strong></p>
            <form method="POST" action="/unsubscribe/confirm">
                <input type="hidden" name="token" value="{token}">
                <button type="submit">Confirm Unsubscribe</button>
            </form>
            <p><small>Not your email? Someone may have forwarded our newsletter to you.
            Just close this page.</small></p>
        </body>
        </html>
        """
    }
```

### 5.2 Gmail Clipping Prevention

**Problem**: >102KB HTML gets clipped, hiding tracking pixel and unsubscribe link.

**Solution**:
1. Enforce size limit in email renderer
2. Move tracking pixel and unsubscribe link to TOP of email
3. Truncate thread summaries if needed

```python
def truncate_email(html: str, max_bytes: int) -> str:
    """Truncate email content while preserving critical elements."""
    # Parse HTML
    soup = BeautifulSoup(html, "html.parser")

    # Never truncate: header, footer (unsubscribe), tracking pixel
    protected = soup.select(".header, .footer, .tracking-pixel")

    # Truncate from bottom: thread summaries, then leader items
    while len(str(soup).encode("utf-8")) > max_bytes:
        # Remove last thread
        threads = soup.select(".thread")
        if threads:
            threads[-1].decompose()
            continue

        # Remove last leader from context tier
        context_leaders = soup.select(".context-tier .leader-item")
        if context_leaders:
            context_leaders[-1].decompose()
            continue

        # Last resort: truncate executive summary
        break

    return str(soup)
```

### 5.3 Double-Send Prevention

Handled by DynamoDB idempotency pattern (Section 3.3).

### 5.4 Bounce/Complaint Auto-Unsubscribe

```python
# Lambda: ses_event_handler.py (triggered by SNS from SES)

def handler(event, context):
    for record in event["Records"]:
        message = json.loads(record["Sns"]["Message"])
        event_type = message["eventType"]

        if event_type in ("Bounce", "Complaint"):
            email = message["mail"]["destination"][0]

            # Auto-unsubscribe
            dynamodb.update_item(
                TableName="ideal-brief-subscribers",
                Key={"email": {"S": email}},
                UpdateExpression="SET status = :status, updated_at = :now",
                ExpressionAttributeValues={
                    ":status": {"S": "bounced" if event_type == "Bounce" else "complained"},
                    ":now": {"S": datetime.utcnow().isoformat()},
                },
            )

            logger.warning(f"Auto-unsubscribed {email} due to {event_type}")
```

---

## 6. Test Plan

### 6.1 Unit Tests

| Component | Test | Tooling |
|-----------|------|---------|
| Pipeline output | JSON schema validation | `pydantic` / `pytest` |
| Publisher | Front matter generation | `pytest` with snapshots |
| Email renderer | Template rendering | `pytest` + Jinja2 |
| Email size | Under 90KB threshold | `pytest` |

```python
# tests/test_publisher.py

def test_schema_validation():
    """Validate pipeline output matches expected schema."""
    from pydantic import BaseModel

    class Story(BaseModel):
        headline: str
        description: str
        sources: list[dict]

    class LeaderDossier(BaseModel):
        leader: str
        country: str
        stories: list[Story]

    # Load actual output
    with open("briefs/20260208/dossiers.json") as f:
        data = json.load(f)

    # Validate each leader
    for leader_name, dossier in data.items():
        LeaderDossier(**dossier)  # Raises if invalid


def test_email_size_under_threshold():
    """Ensure rendered email stays under Gmail clip threshold."""
    html = render_email(load_test_artifacts())
    size_kb = len(html.encode("utf-8")) / 1024
    assert size_kb < 90, f"Email too large: {size_kb:.1f}KB"
```

### 6.2 Integration Tests

```python
# tests/test_integration.py

def test_publisher_dry_run():
    """Publisher generates correct files without git operations."""
    result = subprocess.run(
        ["python", "scripts/publish.py", "--dry-run", "briefs/20260208/"],
        capture_output=True, text=True
    )
    assert result.returncode == 0

    # Check files were generated
    assert Path("_briefs/2026-02-08/index.md").exists()
    assert Path("_briefs/2026-02-08/canada-mark-carney.md").exists()


def test_jekyll_build():
    """Jekyll builds without errors."""
    result = subprocess.run(
        ["bundle", "exec", "jekyll", "build"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "error" not in result.stderr.lower()


def test_no_broken_links():
    """All internal links resolve."""
    subprocess.run(["bundle", "exec", "jekyll", "build"], check=True)
    result = subprocess.run(
        ["htmlproofer", "./_site", "--disable-external"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
```

### 6.3 Staging Environment

```
ideal-brief-staging/           # Separate GitHub repo
ideal-brief-staging-content/   # Separate content repo
staging-subscribers (DynamoDB) # Table with only admin email
```

**Staging workflow**:
1. Pipeline runs against staging repos
2. Creates PR in staging-content
3. Admin merges
4. Email sends to admin only
5. Verify end-to-end before production

### 6.4 Dead Man's Switch

**Problem**: Pipeline fails silently, no brief goes out, nobody notices until Monday.

**Solution**: Negative alerting - alert if expected event DOESN'T happen.

```python
# Lambda: dead_mans_switch.py (triggered Mon 8 AM ET)

def handler(event, context):
    """Alert if no brief was published this week."""

    # Check S3 for this week's artifacts
    brief_id = get_expected_brief_id()  # e.g., "2026-02-08"

    try:
        s3.head_object(Bucket=BUCKET, Key=f"briefs/{brief_id}/meta.json")
    except s3.exceptions.ClientError:
        # Brief doesn't exist - pipeline failed
        send_alert(
            subject="ALERT: IDEAL Brief pipeline failed",
            body=f"No brief artifacts found for {brief_id}. Check ECS logs."
        )
        return

    # Check if email was sent
    response = dynamodb.query(
        TableName="ideal-brief-email-events",
        KeyConditionExpression="brief_id = :bid AND event_type = :send",
        ExpressionAttributeValues={
            ":bid": {"S": brief_id},
            ":send": {"S": "send"},
        },
        Limit=1,
    )

    if not response["Items"]:
        send_alert(
            subject="ALERT: IDEAL Brief email not sent",
            body=f"Brief {brief_id} was generated but email distribution didn't happen."
        )
```

### 6.5 Manual Trigger (Recovery Playbook)

**Scenario**: GitHub Pages deploy succeeds but the webhook times out or fails. The dead man's switch fires Monday morning.

**Recovery steps**:

1. Verify the brief is live at `https://idealbrief.org/briefs/2026-02-08/`
2. Open AWS Console → Lambda → `email-distributor`
3. Create a test event with this payload:

```json
{
  "body": "{\"brief_date\": \"2026-02-08\", \"deployed_url\": \"https://idealbrief.org/briefs/2026-02-08/\"}"
}
```

4. Click "Test" to manually trigger the email distribution
5. Verify in CloudWatch Logs that emails were sent

**CLI alternative**:
```bash
aws lambda invoke \
  --function-name email-distributor \
  --payload '{"body": "{\"brief_date\": \"2026-02-08\", \"deployed_url\": \"https://idealbrief.org/briefs/2026-02-08/\"}"}' \
  --cli-binary-format raw-in-base64-out \
  /dev/stdout
```

The idempotency check ensures this is safe to run multiple times—subscribers who already received the email will be skipped.

---

## 7. Revised AWS Infrastructure

### 7.1 Networking (Cost Optimization)

**Critical**: Fargate tasks need internet access to pull Docker images, clone GitHub repos, and call external APIs. The default approach (private subnet + NAT Gateway) costs ~$32/month in NAT charges alone.

**Solution**: Run Fargate in a **public subnet** with `assign_public_ip = ENABLED`:

```hcl
resource "aws_ecs_service" "brief_generator" {
  # ...
  network_configuration {
    subnets          = [aws_subnet.public.id]
    assign_public_ip = true
    security_groups  = [aws_security_group.fargate_task.id]
  }
}

resource "aws_security_group" "fargate_task" {
  name        = "ideal-brief-fargate"
  description = "Fargate task - no inbound, all outbound"
  vpc_id      = aws_vpc.main.id

  # No ingress rules - task is not accessible from internet

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

This gives the task a public IP for outbound traffic while the security group blocks all inbound connections. Result: **$0/month for networking**.

### 7.2 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         EventBridge Scheduler                            │
│                                                                         │
│  Rule 1: "generate-brief"    cron(0 4 ? * MON *)   (Sun 11 PM ET)      │
│  Rule 2: "dead-mans-switch"  cron(0 13 ? * MON *)  (Mon 8 AM ET)       │
└────────────────┬────────────────────────────────────┬───────────────────┘
                 │                                    │
                 ▼                                    ▼
┌────────────────────────────┐          ┌─────────────────────────────────┐
│ ECS Fargate Task           │          │ Lambda: dead-mans-switch        │
│ "ideal-brief-generate"     │          │ Alerts if brief missing         │
│                            │          └─────────────────────────────────┘
│ - Run pipeline             │
│ - Validate output          │
│ - Create PR (not push)     │
│ - Upload artifacts to S3   │
│ - Send preview to admin    │
└────────────────────────────┘

                    ┌──────────────────────────────────┐
                    │        HUMAN REVIEW GATE          │
                    │                                  │
                    │  Admin reviews PR, merges if OK  │
                    └───────────────┬──────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    GitHub Actions (on PR merge)                          │
│                                                                         │
│  1. Validate schema                                                     │
│  2. Build Jekyll                                                        │
│  3. Check links                                                         │
│  4. Deploy to Pages                                                     │
│  5. Verify live (curl health check)                                     │
│  6. POST webhook to API Gateway ─────────────────────┐                  │
└─────────────────────────────────────────────────────────────────────────┘
                                                       │
                                                       ▼
                                    ┌─────────────────────────────────────┐
                                    │ API Gateway + Lambda                 │
                                    │ "email-distributor"                  │
                                    │                                     │
                                    │ - Load artifacts from S3            │
                                    │ - Query active subscribers          │
                                    │ - Send via SES (idempotent)         │
                                    └─────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         Supporting Resources                             │
│                                                                         │
│  S3: ideal-brief-artifacts                                              │
│    └── briefs/{date}/meta.json, dossiers.json, email.html               │
│                                                                         │
│  DynamoDB:                                                              │
│    ├── ideal-brief-subscribers (email, status, token, last_sent)        │
│    └── ideal-brief-email-events (email, timestamp, event_type)          │
│                                                                         │
│  SES:                                                                   │
│    ├── Configuration Set: ideal-brief-tracking                          │
│    └── SNS → Lambda (bounce/complaint handler)                          │
│                                                                         │
│  Secrets Manager:                                                       │
│    ├── github-deploy-key                                                │
│    ├── webhook-secret                                                   │
│    └── api-keys                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Cost Estimate (Revised)

| Resource | Monthly Cost |
|----------|-------------|
| ECS Fargate (4 runs × 15 min) | ~$0.16 |
| Lambda (email sender + handlers) | ~$0.01 |
| API Gateway (webhook endpoint) | ~$0.01 |
| DynamoDB (on-demand, 2 tables) | ~$0.50 |
| S3 (artifacts storage) | ~$0.10 |
| SES (4 sends × 500 subscribers) | ~$0.20 |
| ECR (image storage) | ~$0.10 |
| Networking (public subnet) | $0.00 |
| Plausible Analytics | $9.00 |
| **Total** | **~$10-11/month** |

**Note**: Using public subnets with `assign_public_ip` avoids NAT Gateway charges (~$32/month). See Section 7.1.

---

## 9. Migration Path from v1

1. **Create content repo**: `ideal-brief-content`
2. **Update ECS task**: Change from `git push` to `gh pr create`
3. **Deploy DynamoDB tables**: Migrate S3 JSON subscribers
4. **Update GitHub Actions**: Add webhook step after deploy
5. **Create API Gateway + Lambda**: Email distributor endpoint
6. **Add dead man's switch**: Monday morning alerting
7. **Test in staging**: Full cycle with admin-only subscriber list
8. **Cut over**: Point production EventBridge to new task

---

## 10. Summary of Changes from v1

| v1 (Original) | v2 (Revised) | Why |
|---------------|--------------|-----|
| Direct push to main | PR-based review gate | Human verification before publish |
| Cron-based email (6:30 AM) | Event-driven (post-deploy webhook) | Prevents 404 race condition |
| Single repo (code + content) | Separate content repo | Clean history, no merge conflicts |
| S3 JSON subscribers | DynamoDB with idempotency | ACID guarantees, no race conditions |
| No size checking | 90KB email limit enforced | Gmail clipping prevention |
| Instant unsubscribe | Two-step confirmation | Forwarding attack prevention |
| No failure alerting | Dead man's switch | Know when pipeline fails silently |
