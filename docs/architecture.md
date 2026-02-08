# PDB Architecture Plan

## Overview

This document outlines the architecture for deploying the Presidential Daily Brief (PDB) system with automated generation, hosting, subscriber notifications, and archive management.

## Components

### 1. Archive Structure

```
briefs/
  2026/
    02/
      07/
        index.html          # Rendered brief
        brief.json          # Structured data
        dossiers/
          lula_da_silva.html
          mark_carney.html
          claudia_sheinbaum.html
          yamandú_orsi.html
      14/
        ...
    01/
      ...
  2025/
    ...
```

Each week is a self-contained snapshot. Archives are immutable once published.

### 2. Hosting

**Stack: S3 + CloudFront**

- **S3**: Store rendered HTML/JSON briefs
- **CloudFront**: CDN for fast global delivery, HTTPS
- **Alternative**: Cloudflare R2 (S3-compatible, no egress fees)

Benefits:
- Cheap at scale (pennies per GB)
- Archives are just folders - no database needed for storage
- Static files = no server maintenance

URL structure:
```
https://briefs.example.com/2026/02/07/              # Weekly brief
https://briefs.example.com/2026/02/07/dossiers/lula_da_silva.html
https://briefs.example.com/latest/                  # Redirect to most recent
```

### 3. Backend API

**Stack: FastAPI + Postgres**

A lightweight API for:
- Subscriber management (signup, preferences, unsubscribe)
- Email tracking (opens, clicks)
- Brief metadata & search
- Future: authentication, access control

**Postgres Schema:**

```sql
-- Subscribers
CREATE TABLE subscribers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    confirmed BOOLEAN DEFAULT FALSE,
    confirmation_token VARCHAR(64),
    preferences JSONB DEFAULT '{}',  -- e.g., {"regions": ["americas", "europe"]}
    created_at TIMESTAMPTZ DEFAULT NOW(),
    unsubscribed_at TIMESTAMPTZ
);

-- Published briefs
CREATE TABLE briefs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE UNIQUE NOT NULL,
    s3_path VARCHAR(512) NOT NULL,
    metadata JSONB NOT NULL,  -- leader_count, story_count, etc.
    published_at TIMESTAMPTZ DEFAULT NOW()
);

-- Email sends (for tracking)
CREATE TABLE email_sends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscriber_id UUID REFERENCES subscribers(id),
    brief_id UUID REFERENCES briefs(id),
    sent_at TIMESTAMPTZ DEFAULT NOW(),
    opened_at TIMESTAMPTZ,
    clicked_at TIMESTAMPTZ,
    bounce_type VARCHAR(50)  -- null, 'soft', 'hard'
);

-- Indexes
CREATE INDEX idx_subscribers_email ON subscribers(email);
CREATE INDEX idx_briefs_date ON briefs(date DESC);
CREATE INDEX idx_email_sends_subscriber ON email_sends(subscriber_id);
```

### 4. Email Service

**Recommended: Postmark or SendGrid**

Features needed:
- Transactional email (not marketing)
- Webhook callbacks for opens/clicks/bounces
- Good deliverability reputation
- Template support (HTML emails)

**Email flow:**
1. Brief generated and uploaded to S3
2. API records brief in Postgres
3. API fetches confirmed subscribers
4. For each subscriber: render email, send via Postmark
5. Record send in `email_sends`
6. Postmark webhooks update `opened_at`, `clicked_at`, `bounce_type`

**Email content:**
- Subject: "PDB Weekly Brief: [Date Range]"
- Body: Top 5 stories with summaries
- CTA: "Read full brief" → link to hosted version
- Footer: Unsubscribe link

### 5. GitHub Actions Automation

**Weekly generation workflow:**

```yaml
name: Generate Weekly Brief

on:
  schedule:
    - cron: '0 12 * * 1'  # Every Monday at 12:00 UTC
  workflow_dispatch:  # Manual trigger

jobs:
  generate:
    runs-on: ubuntu-latest
    timeout-minutes: 60

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Generate brief
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          SERPAPI_KEY: ${{ secrets.SERPAPI_KEY }}
          DIFFBOT_TOKEN: ${{ secrets.DIFFBOT_TOKEN }}
        run: |
          python -m src.main --output-format html

      - name: Upload to S3
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          aws s3 sync briefs/ s3://pdb-briefs/ --acl public-read

      - name: Notify subscribers
        env:
          PDB_API_URL: ${{ secrets.PDB_API_URL }}
          PDB_API_KEY: ${{ secrets.PDB_API_KEY }}
        run: |
          python -m src.notify --brief-date $(date +%Y%m%d)

      - name: Invalidate CloudFront cache
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          CLOUDFRONT_DISTRIBUTION_ID: ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }}
        run: |
          aws cloudfront create-invalidation \
            --distribution-id $CLOUDFRONT_DISTRIBUTION_ID \
            --paths "/latest/*" "/"
```

### 6. Future: Trajectory Analysis

For analyzing leader activity over time, a hybrid approach:

**Structured Data (Postgres)**

Store extracted entities and events for quantitative queries:

```sql
-- Events extracted from stories
CREATE TABLE events (
    id UUID PRIMARY KEY,
    brief_id UUID REFERENCES briefs(id),
    leader_name VARCHAR(255) NOT NULL,
    event_type VARCHAR(50),  -- 'bilateral_meeting', 'policy_announcement', etc.
    event_date DATE,
    entities JSONB,  -- [{uri, name, type, salience}, ...]
    narrative TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Entity co-occurrences for relationship tracking
CREATE TABLE entity_relationships (
    id UUID PRIMARY KEY,
    event_id UUID REFERENCES events(id),
    entity_a_uri VARCHAR(512),
    entity_b_uri VARCHAR(512),
    relationship_type VARCHAR(50),
    context TEXT
);

CREATE INDEX idx_events_leader ON events(leader_name, event_date);
CREATE INDEX idx_events_type ON events(event_type);
```

Example queries:
- "Count Xi Jinping's bilateral meetings by region over 6 months"
- "Show all events involving both Sheinbaum and Trump"
- "Track mentions of 'tariff' across all leaders by week"

**Vector Search (pgvector or Pinecone)**

Embed story narratives for semantic search:

```sql
-- Add to events table or separate
ALTER TABLE events ADD COLUMN embedding vector(1536);

-- Semantic search
SELECT * FROM events
ORDER BY embedding <=> $query_embedding
LIMIT 10;
```

Example queries:
- "Find coverage similar to Orsi's China visit"
- "Stories about leaders resisting US pressure"
- "Trade negotiation themes across Latin America"

**Combined Queries**

1. Semantic search to find relevant events
2. Structured aggregation to show trends
3. Visualization of leader trajectories over time

---

## Implementation Phases

### Phase 1: Basic Automation (MVP)
- [ ] GitHub Actions workflow for weekly generation
- [ ] S3 upload for hosting
- [ ] Simple subscriber list (CSV or Postgres)
- [ ] Basic email notification

### Phase 2: Subscriber Management
- [ ] FastAPI backend
- [ ] Postgres schema for subscribers
- [ ] Signup/unsubscribe flows
- [ ] Email tracking (opens, clicks)

### Phase 3: Archive & Search
- [ ] Archive browser UI
- [ ] Full-text search across briefs
- [ ] Structured event extraction to Postgres

### Phase 4: Trajectory Analysis
- [ ] Vector embeddings for semantic search
- [ ] Leader activity dashboards
- [ ] Trend visualization
- [ ] API access for programmatic queries

---

## Cost Estimates

| Component | Service | Estimated Monthly Cost |
|-----------|---------|------------------------|
| Hosting | S3 + CloudFront | $5-20 |
| Database | Postgres (managed) | $15-50 |
| Email | Postmark | $10-25 (based on volume) |
| Compute | GitHub Actions | Free (2000 min/mo) |
| API hosting | Fly.io / Railway | $5-20 |
| **Total** | | **$35-115/mo** |

---

## Security Considerations

- API keys stored in GitHub Secrets
- Subscriber emails encrypted at rest
- Unsubscribe tokens are single-use
- Rate limiting on signup endpoints
- No PII in S3 (only published content)
