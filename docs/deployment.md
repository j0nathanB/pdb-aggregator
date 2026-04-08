# Deployment

## Topology

```
EventBridge Scheduler         AWS Fargate task                   GitHub repo                Mintlify Cloud
─────────────────────         ────────────────                   ────────────               ──────────────
Sun 9pm ET (cron)        →    Pull Docker image from ECR    →    git push origin main  →    Auto-deploy
                              Clone repo, run pipeline                                       middlepowers.fyi
                              Commit ledgers/, site/briefs/,
                              briefs/ (traces) → push
```

The pipeline does its own work. AWS provides the schedule, the Fargate runtime, and CloudWatch logs. GitHub holds the source of truth (code, ledgers, briefs, traces). Mintlify handles deployment to the public site automatically when commits land on `main`.

There is no email, no S3, no API Gateway, no DynamoDB. The only outputs are git commits and CloudWatch logs.

## What's in `infra/`

| File | What it manages |
|------|-----------------|
| `main.tf` | Terraform setup, AWS provider, default tags |
| `vpc.tf` | VPC, public subnet, Fargate security group |
| `ecr.tf` | Docker image registry for the pipeline container |
| `ecs.tf` | Fargate cluster + task definition + CloudWatch log group |
| `eventbridge.tf` | The Sunday 9pm Eastern cron schedule |
| `iam.tf` | ECS execution role, ECS task role, scheduler role |
| `secrets.tf` | Secrets Manager entries (Anthropic, GitHub, SearchAPI, Diffbot) |
| `variables.tf` | Tunable inputs (region, CPU/memory, image tag, schedule toggle) |
| `outputs.tf` | Resource ARNs for reference |
| `terraform.tfvars` | Local config (gitignored) |

## Initial deploy (or first deploy from this state)

### 1. Terraform: provision everything

```bash
cd infra
terraform init                  # only the first time
terraform plan                  # review what will be created/destroyed
terraform apply                 # type "yes" to proceed
```

If you're applying after the email-infra cleanup, the plan will show ~25 resources being **destroyed** (Lambdas, SES, DynamoDB, S3, API Gateway, IAM roles, secrets, SGs). Review that list carefully — those are real AWS resources tied to the old setup.

### 2. Populate secrets

After Terraform creates the empty secret containers, set their values:

```bash
aws secretsmanager put-secret-value \
  --secret-id ideal-brief-prod-anthropic-api-key \
  --secret-string 'sk-ant-...'

aws secretsmanager put-secret-value \
  --secret-id ideal-brief-prod-github-token \
  --secret-string '{"token":"ghp_..."}'

aws secretsmanager put-secret-value \
  --secret-id ideal-brief-prod-searchapi-key \
  --secret-string '...'

aws secretsmanager put-secret-value \
  --secret-id ideal-brief-prod-diffbot-token \
  --secret-string '...'
```

The GitHub token needs `repo` scope (push access to the repo).

### 3. Build and push the Docker image

The Docker image only contains `scripts/run_pipeline.py` as the entrypoint — everything else (the actual pipeline code) gets cloned from GitHub at runtime. So you only need to rebuild the image when:
- Dependencies in `requirements.txt` change
- The Dockerfile itself changes
- `scripts/run_pipeline.py` changes

```bash
# Get ECR login
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin \
    $(terraform -chdir=infra output -raw ecr_repository_url \
      | cut -d/ -f1)

# Build for ARM64 (Fargate runs ARM)
docker buildx build --platform linux/arm64 \
  -t $(terraform -chdir=infra output -raw ecr_repository_url):latest \
  --push .
```

### 4. Enable the schedule

In `infra/terraform.tfvars`:

```hcl
enable_schedules = true
```

Then `terraform apply` again. The schedule moves from `DISABLED` to `ENABLED`.

## Redeploy after code changes

### Pipeline code changes (most common)

The pipeline code (`src/monitor/`, `assets/`, etc.) is **not in the Docker image**. The Fargate task clones the repo at runtime. So a code change is just:

```bash
git push origin main
```

The next scheduled run picks it up automatically.

### `run_pipeline.py`, `requirements.txt`, or `Dockerfile` changes

Rebuild and push the image (same as step 3 above). Fargate pulls the latest tag on each run, so no Terraform change is needed.

If you want versioned images (e.g., `:v2`), update `pipeline_image_tag` in `infra/terraform.tfvars` and `terraform apply` to update the task definition.

### Terraform changes

```bash
cd infra
terraform plan
terraform apply
```

Always review the plan before applying. Schedule changes apply on the next cron tick.

## Manual runs

### Trigger the Fargate task on demand

Without waiting for Sunday:

```bash
aws ecs run-task \
  --cluster ideal-brief-prod-cluster \
  --task-definition ideal-brief-prod-pipeline \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={
    subnets=[$(terraform -chdir=infra output -raw public_subnet_id)],
    securityGroups=[$(terraform -chdir=infra output -raw fargate_security_group_id)],
    assignPublicIp=ENABLED
  }"
```

The task ID is returned in the response. Use it to tail logs (next section).

### Run the pipeline locally

You don't always need Fargate. The same `scripts/run_pipeline.py` runs locally:

```bash
.venv/bin/python scripts/run_pipeline.py --date 2026-04-12
```

In local mode it commits to your working tree. In Fargate mode (when `is_in_repo()` is false) it clones into `/tmp/repo` first.

## Schedule management

| Task | How |
|------|-----|
| **Disable** the cron | Set `enable_schedules = false` in `terraform.tfvars`, `terraform apply` |
| **Enable** the cron | Set `enable_schedules = true`, `terraform apply` |
| **Change the time** | Edit `schedule_expression` in `infra/eventbridge.tf` |
| **Verify next run** | `aws scheduler get-schedule --name ideal-brief-prod-generate-brief` |

The current schedule is `cron(0 21 ? * SUN *)` in timezone `America/New_York` — Sunday 9 PM Eastern, DST-aware.

## Debugging a failed (or successful) run

### CloudWatch logs (stdout/stderr from the ECS task)

```bash
# Tail live
aws logs tail /ecs/ideal-brief-prod-pipeline --follow

# Last hour
aws logs tail /ecs/ideal-brief-prod-pipeline --since 1h

# Specific task
aws logs tail /ecs/ideal-brief-prod-pipeline \
  --log-stream-names pipeline/pipeline/<task-id>
```

Or in the AWS Console: CloudWatch → Log groups → `/ecs/ideal-brief-prod-pipeline`. Logs are retained for 30 days.

### Pipeline traces (in the repo after the Fargate run)

`scripts/run_pipeline.py` commits the trace directory after each run, so:

```bash
git pull origin main
ls briefs/$(date +%Y%m%d)/traces/    # raw LLM responses, manifests
ls site/briefs/$(date +%Y-%m-%d)/    # the published MDX
ls ledgers/                          # updated ledger state
```

Per-stage trace files (`country_*.json`, `editor_*.json`, `copyeditor_*.json`, `style_editor_*.json`, `story_map_*.json`, `government_*.json`) record both inputs and outputs of every LLM call. Use them with the `replay` CLI command to re-parse without re-running the API calls:

```bash
.venv/bin/python -m src.monitor.cli replay --date 2026-04-12 --agent country
```

### Re-running a failed country/region locally

If a single country failed in production:

```bash
git pull origin main
# Patch the trace if needed, then:
.venv/bin/python scripts/reedit.py --date 2026-04-12 --country pl --from country
```

See `docs/adding_a_country.md` and the `reedit.py` docstring for the recovery patterns.

## Operational tasks

### Rotating a secret

```bash
aws secretsmanager put-secret-value \
  --secret-id ideal-brief-prod-anthropic-api-key \
  --secret-string 'sk-ant-NEW...'
```

The change applies on the next Fargate run (each task pulls fresh secret values at startup).

### Checking task history

```bash
aws ecs list-tasks --cluster ideal-brief-prod-cluster --desired-status STOPPED
aws ecs describe-tasks --cluster ideal-brief-prod-cluster --tasks <task-arn>
```

`stopCode` and `stoppedReason` tell you why a task ended. Common values: `EssentialContainerExited` (the script ran to completion or errored out), `TaskFailedToStart` (image pull failed, secrets missing, etc.).

### Cost monitoring

Roughly the only ongoing AWS costs:
- **Fargate compute**: ~2 vCPU + 4 GB RAM × ~2 hours/week × $0.04/hr ≈ $0.20/week
- **CloudWatch Logs**: ~50 MB/week × $0.50/GB ≈ $0.025/week
- **ECR storage**: tiny (~1 GB) × $0.10/GB ≈ $0.10/month
- **Secrets Manager**: 4 secrets × $0.40/month = $1.60/month
- **Data transfer**: minimal (git operations + Anthropic API egress)

The big spend is **Anthropic API**, which is metered separately. The pipeline produces a cost summary at the end of each run.

### Tearing down everything

```bash
cd infra
terraform destroy
```

Will prompt before deleting. Schedule first, then ECS task definition, then VPC and IAM. Secrets Manager retains deleted secrets for 30 days by default — recover with `aws secretsmanager restore-secret` if needed.

## Things that surprise people

- **Pipeline code is NOT in the Docker image.** The container is essentially `python + scripts/run_pipeline.py`. The actual pipeline (`src/monitor/`, prompts, configs) comes from a fresh `git clone` at runtime. This means most code changes don't require an image rebuild.
- **The ECS task role is empty.** The container doesn't talk to AWS services — secrets are injected as env vars by the execution role at startup, then the script just clones, runs, and pushes.
- **Mintlify deployment is invisible to AWS.** Once the Fargate task pushes to `main`, AWS is done. Mintlify Cloud watches the repo via GitHub integration and rebuilds on its own.
- **Trace files are committed to the repo** (since the email cleanup). They live in `briefs/{YYYYMMDD}/traces/` and accumulate. If they ever become too large, the cleanup pattern is to archive old dates or move them to `briefs/_old/`.
- **CloudWatch logs are the only place stdout lives.** They're not committed to the repo. If you need a log and the 30-day retention has lapsed, it's gone.
