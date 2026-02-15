---
layout: default
title: Home
nav_order: 1
---

# The Middle Powers Monitor

Weekly intelligence briefs covering world leaders.
{: .fs-6 .fw-300 }

{% assign briefs = site.briefs | where: "doc_type", "brief" | sort: "date" | reverse %}

{% for brief in briefs %}
- [{{ brief.title }}]({{ brief.url | relative_url }}) — {{ brief.date | date: "%B %-d, %Y" }} ({{ brief.leader_count }} leaders, {{ brief.story_count }} stories)
{% endfor %}
