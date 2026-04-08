# GitHub Setup for IDEAL Brief

## Repository Structure

You need two repositories:

```
ideal-brief-site/        # Code repo (Jekyll templates, styles, config)
├── .github/
│   └── workflows/
│       └── deploy-and-notify.yml   # Copy from this directory
├── _config.yml
├── _layouts/
├── _includes/
├── assets/
├── scripts/
│   └── validate_brief.py
└── Gemfile

ideal-brief-content/     # Data repo (generated briefs only)
├── _briefs/
│   ├── 2026-02-08/
│   │   ├── index.md
│   │   └── [leader-dossiers].md
│   └── ...
└── _data/
    └── briefs_index.yml
```

## Step 1: Create the Content Repository

```bash
# Create new repo on GitHub
gh repo create ideal-brief-content --private --description "IDEAL Brief generated content"

# Clone and set up structure
git clone git@github.com:YOUR_USERNAME/ideal-brief-content.git
cd ideal-brief-content

mkdir -p _briefs _data
echo "briefs: []" > _data/briefs_index.yml
echo "# IDEAL Brief Content\n\nGenerated briefs are stored here." > README.md

git add -A
git commit -m "Initial structure"
git push
```

## Step 2: Configure GitHub Secrets

In your **ideal-brief-site** repository, add these secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `API_GATEWAY_KEY` | `3fa07b1d285d7f688d0e94d7c6fb316af7fe9555826412d24dd73cfd1d61f460` | API key for webhook auth |
| `EMAIL_TRIGGER_WEBHOOK` | `https://0w6nza4l7i.execute-api.us-east-1.amazonaws.com/prod` | API Gateway endpoint |
| `CONTENT_REPO_TOKEN` | `ghp_...` | GitHub PAT with `repo` scope for content repo |

### Creating the Content Repo Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Create new token with:
   - Repository access: Only select repositories → `ideal-brief-content`
   - Permissions: Contents (Read-only)
3. Copy the token and add as `CONTENT_REPO_TOKEN` secret

## Step 3: Enable GitHub Pages

1. Go to ideal-brief-site → Settings → Pages
2. Source: GitHub Actions
3. Save

## Step 4: Copy the Workflow

Copy `deploy-and-notify.yml` to your site repo:

```bash
cd ideal-brief-site
mkdir -p .github/workflows
cp /path/to/deploy-and-notify.yml .github/workflows/
git add .github/workflows/deploy-and-notify.yml
git commit -m "Add deploy and notify workflow"
git push
```

## Step 5: Test the Pipeline

### Manual Test (No Email)

```bash
# Trigger deploy without email
gh workflow run deploy-and-notify.yml -f send_email=false
```

### End-to-End Test

1. Add a test subscriber to DynamoDB:

```bash
aws dynamodb put-item \
  --table-name ideal-brief-prod-subscribers \
  --item '{
    "email": {"S": "hi@jonathanb.ai"},
    "status": {"S": "active"},
    "subscribed_at": {"S": "2026-02-13T00:00:00Z"},
    "unsubscribe_token": {"S": "test-token-12345"}
  }'
```

2. Upload test artifacts to S3:

```bash
# Create test email HTML
echo "<html><body><h1>Test Brief</h1><p>This is a test.</p></body></html>" > /tmp/email.html
echo '{"subject": "IDEAL Brief: Test"}' > /tmp/meta.json

# Upload to S3
aws s3 cp /tmp/email.html s3://ideal-brief-artifacts-pdb/briefs/2026-02-08/email.html
aws s3 cp /tmp/meta.json s3://ideal-brief-artifacts-pdb/briefs/2026-02-08/meta.json
```

3. Test the webhook directly:

```bash
curl -X POST "https://0w6nza4l7i.execute-api.us-east-1.amazonaws.com/prod/send" \
  -H "Content-Type: application/json" \
  -H "x-api-key: 3fa07b1d285d7f688d0e94d7c6fb316af7fe9555826412d24dd73cfd1d61f460" \
  -d '{"brief_date": "2026-02-08", "deployed_url": "https://idealbrief.org/"}'
```

## Troubleshooting

### Workflow fails at "Checkout content repo"
- Check that `CONTENT_REPO_TOKEN` has read access to the content repo

### Email not sent
- Verify SES email identity is verified: `aws ses get-identity-verification-attributes --identities brief@idealbrief.org`
- Check Lambda logs: `aws logs tail /aws/lambda/ideal-brief-prod-email-sender --follow`

### 403 from API Gateway
- Verify `API_GATEWAY_KEY` matches the secret in AWS
- Check authorizer Lambda logs: `aws logs tail /aws/lambda/ideal-brief-prod-authorizer --follow`
