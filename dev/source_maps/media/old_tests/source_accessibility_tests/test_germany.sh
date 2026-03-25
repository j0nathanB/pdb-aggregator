#!/bin/bash
# Test script for German source accessibility

OUTPUT_DIR="/Users/zen/dev/src/pdb/docs/source_intelligence_maps/tests"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

test_source() {
  local name="$1"
  local domain="$2"

  echo "Testing: $name ($domain)" >&2

  # 1. Homepage status
  local homepage_code
  homepage_code=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 10 -A "$UA" "https://$domain" 2>/dev/null)
  local can_fetch_homepage="false"
  if [ "$homepage_code" -ge 200 ] 2>/dev/null && [ "$homepage_code" -lt 400 ] 2>/dev/null; then
    can_fetch_homepage="true"
  fi

  # 2. Fetch homepage content and find article link
  local homepage_html
  homepage_html=$(curl -sL --max-time 15 -A "$UA" "https://$domain" 2>/dev/null | head -c 80000)

  local article_url=""
  local can_fetch_article="false"
  local can_get_full_text="false"
  local first_paragraph=""
  local last_paragraph=""
  local pub_date=""

  # Extract article URLs - look for absolute URLs on same domain
  article_url=$(echo "$homepage_html" | grep -o "href=\"https://$domain/[^\"]*\"" | grep -v -e '\.css' -e '\.js' -e '\.png' -e '\.jpg' -e '\.svg' -e '\.ico' -e 'login' -e 'register' -e 'cookie' -e 'datenschutz' -e 'impressum' -e 'newsletter' | head -1 | sed 's/href="//;s/"$//')

  if [ -z "$article_url" ]; then
    # Try relative URLs that look like articles
    local rel_path
    rel_path=$(echo "$homepage_html" | grep -o 'href="/[a-z][^"]*"' | grep -v -e '\.css' -e '\.js' -e '\.png' -e '\.jpg' -e '\.svg' -e '\.ico' -e 'login' -e 'register' -e 'cookie' -e 'datenschutz' -e 'impressum' -e 'newsletter' -e 'suche' -e 'abo' | grep '/' | head -3 | tail -1 | sed 's/href="//;s/"$//')
    if [ -n "$rel_path" ]; then
      article_url="https://$domain$rel_path"
    fi
  fi

  if [ -n "$article_url" ]; then
    local article_html
    article_html=$(curl -sL --max-time 15 -A "$UA" "$article_url" 2>/dev/null | head -c 150000)
    local article_code
    article_code=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 10 -A "$UA" "$article_url" 2>/dev/null)

    if [ "$article_code" -ge 200 ] 2>/dev/null && [ "$article_code" -lt 400 ] 2>/dev/null; then
      can_fetch_article="true"
    fi

    # Extract paragraphs using sed-based approach (macOS compatible)
    local paragraphs
    paragraphs=$(echo "$article_html" | sed 's/<\/p>/\nENDPARA\n/g' | sed 's/<p[^>]*>/\nSTARTPARA/g' | grep 'STARTPARA' | sed 's/STARTPARA//' | sed 's/<[^>]*>//g' | sed 's/^[[:space:]]*//' | sed '/^$/d' | awk 'length > 40' | head -20)

    if [ -n "$paragraphs" ]; then
      local p_count
      p_count=$(echo "$paragraphs" | wc -l | tr -d ' ')
      if [ "$p_count" -ge 3 ]; then
        can_get_full_text="true"
      fi
      first_paragraph=$(echo "$paragraphs" | head -1 | head -c 300 | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/[[:cntrl:]]//g')
      last_paragraph=$(echo "$paragraphs" | tail -1 | head -c 300 | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/[[:cntrl:]]//g')
    fi

    # Extract publication date
    pub_date=$(echo "$article_html" | grep -o '"datePublished":"[^"]*"' | head -1 | sed 's/"datePublished":"//;s/"$//')
    if [ -z "$pub_date" ]; then
      pub_date=$(echo "$article_html" | grep -o 'datetime="[^"]*"' | head -1 | sed 's/datetime="//;s/"$//')
    fi
    if [ -z "$pub_date" ]; then
      pub_date=$(echo "$article_html" | grep -o 'article:published_time" content="[^"]*"' | head -1 | sed 's/.*content="//;s/"$//')
    fi
  fi

  # 3. Test RSS feeds
  local has_rss="false"
  local rss_url=""
  local rss_has_full_text="false"
  local notes=""

  for rss_path in /rss /feed /rss.xml /feeds /atom.xml /feed.xml /rss/aktuell; do
    local rss_test_url="https://$domain$rss_path"
    local rss_code
    rss_code=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 8 -A "$UA" "$rss_test_url" 2>/dev/null)
    if [ "$rss_code" -ge 200 ] 2>/dev/null && [ "$rss_code" -lt 400 ] 2>/dev/null; then
      local rss_content
      rss_content=$(curl -sL --max-time 8 -A "$UA" "$rss_test_url" 2>/dev/null | head -c 8000)
      if echo "$rss_content" | grep -qi '<rss\|<feed\|<channel\|<atom'; then
        has_rss="true"
        rss_url="$rss_test_url"
        if echo "$rss_content" | grep -q 'content:encoded'; then
          rss_has_full_text="true"
        fi
        break
      fi
    fi
  done

  # Build notes
  if [ "$can_fetch_homepage" = "false" ]; then
    notes="Homepage not accessible (HTTP $homepage_code)"
  fi
  if [ "$has_rss" = "true" ] && [ "$rss_has_full_text" = "true" ]; then
    notes="${notes:+$notes; }RSS feed includes content:encoded (potential full text)"
  elif [ "$has_rss" = "true" ]; then
    notes="${notes:+$notes; }RSS feed found but appears summary-only"
  fi
  if [ "$can_get_full_text" = "false" ] && [ "$can_fetch_article" = "true" ]; then
    notes="${notes:+$notes; }Article fetched but full text extraction limited (likely paywall or JS rendering)"
  fi

  # JSON output
  local art_json="null"
  [ -n "$article_url" ] && art_json="\"$(echo "$article_url" | sed 's/"/\\"/g')\""
  local fp_json="null"
  [ -n "$first_paragraph" ] && fp_json="\"$first_paragraph\""
  local lp_json="null"
  [ -n "$last_paragraph" ] && lp_json="\"$last_paragraph\""
  local pd_json="null"
  [ -n "$pub_date" ] && pd_json="\"$pub_date\""
  local ru_json="null"
  [ -n "$rss_url" ] && ru_json="\"$rss_url\""

  cat <<ENDJSON
  {
    "source_name": "$name",
    "domain": "$domain",
    "can_fetch_homepage": $can_fetch_homepage,
    "homepage_status_code": $homepage_code,
    "can_fetch_article": $can_fetch_article,
    "can_get_full_text": $can_get_full_text,
    "first_paragraph": $fp_json,
    "last_paragraph": $lp_json,
    "test_article_url": $art_json,
    "publication_date": $pd_json,
    "has_rss": $has_rss,
    "rss_url": $ru_json,
    "rss_has_full_text": $rss_has_full_text,
    "notes": "$notes"
  }
ENDJSON
}

GERMANY_SOURCES=(
  "Frankfurter Allgemeine Zeitung (FAZ)|www.faz.net"
  "Sueddeutsche Zeitung (SZ)|www.sueddeutsche.de"
  "Die Zeit|www.zeit.de"
  "Handelsblatt|www.handelsblatt.com"
  "WirtschaftsWoche|www.wiwo.de"
  "Der Spiegel|www.spiegel.de"
  "Die Welt|www.welt.de"
  "taz (Die Tageszeitung)|taz.de"
  "Der Tagesspiegel|www.tagesspiegel.de"
  "Politico Europe|www.politico.eu"
  "Deutsche Welle (DW)|www.dw.com"
  "SWP (Stiftung Wissenschaft und Politik)|www.swp-berlin.org"
  "DGAP|dgap.org"
  "Internationale Politik Quarterly (IPQ)|internationalepolitik.de"
  "Bundesregierung|www.bundesregierung.de"
  "Auswaertiges Amt|www.auswaertiges-amt.de"
  "Frankfurter Rundschau|www.fr.de"
  "n-tv|www.n-tv.de"
  "IPG Journal (Friedrich-Ebert-Stiftung)|www.ipg-journal.de"
)

echo "["
first=true
for src in "${GERMANY_SOURCES[@]}"; do
  IFS='|' read -r name domain <<< "$src"
  if [ "$first" = true ]; then
    first=false
  else
    echo "  ,"
  fi
  test_source "$name" "$domain"
done
echo "]"
