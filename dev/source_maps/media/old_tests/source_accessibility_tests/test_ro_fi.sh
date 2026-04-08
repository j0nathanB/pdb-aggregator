#!/bin/bash
# Source accessibility testing script for Romania and Finland
# macOS compatible (no grep -P)

OUTPUT_DIR="/Users/zen/dev/src/pdb/docs/source_intelligence_maps/tests"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

test_source() {
  local name="$1"
  local domain="$2"
  local homepage_url="$3"
  local notes="$4"

  echo "Testing: $name ($domain)" >&2

  # 1. Homepage test
  local status
  status=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 10 -A "$UA" "$homepage_url" 2>/dev/null)
  local can_fetch="false"
  if [ "$status" -ge 200 ] 2>/dev/null && [ "$status" -lt 400 ] 2>/dev/null; then
    can_fetch="true"
  fi

  # 2. Find and fetch article
  local html=""
  local article_url=""
  local can_fetch_article="false"
  local can_get_full_text="false"
  local first_p="null"
  local last_p="null"
  local pub_date="null"

  if [ "$can_fetch" = "true" ]; then
    html=$(curl -sL --max-time 15 -A "$UA" "$homepage_url" 2>/dev/null | head -c 80000)

    # Extract article links - try absolute URLs first
    article_url=$(echo "$html" | tr '"' '\n' | grep -iE "https?://[^[:space:]]*${domain}[^[:space:]]*/[a-z0-9].*[a-z0-9-]" | grep -vE '\.(css|js|png|jpg|gif|svg|ico|woff|ttf|eot)' | grep -vE '(^$|#|mailto:|javascript:)' | grep -E '/' | sort -u | head -1)

    # Try relative URLs if no absolute found
    if [ -z "$article_url" ]; then
      local rel
      rel=$(echo "$html" | tr '"' '\n' | grep -E '^/[a-z0-9]' | grep -vE '\.(css|js|png|jpg|gif|svg|ico|woff|ttf|eot)' | grep -E '/[a-z0-9].*[a-z0-9-]' | grep -vE '^/(rss|feed|atom|sitemap|robots|favicon|wp-content|wp-includes|static|assets|css|js|img|images|fonts|media)' | sort -u | head -1)
      if [ -n "$rel" ]; then
        article_url="https://$domain$rel"
      fi
    fi

    if [ -n "$article_url" ]; then
      local art_code
      art_code=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 10 -A "$UA" "$article_url" 2>/dev/null)
      if [ "$art_code" -ge 200 ] 2>/dev/null && [ "$art_code" -lt 400 ] 2>/dev/null; then
        can_fetch_article="true"
        local art_html
        art_html=$(curl -sL --max-time 15 -A "$UA" "$article_url" 2>/dev/null)

        # Extract paragraphs
        local paragraphs
        paragraphs=$(echo "$art_html" | sed 's/<\/p>/ENDPARA\n/g' | tr '\n' ' ' | sed 's/ENDPARA/\n/g' | sed 's/<[^>]*>//g' | sed 's/&nbsp;/ /g; s/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g; s/&#[0-9]*;//g; s/&[a-z]*;//g' | sed 's/^[[:space:]]*//' | sed '/^$/d' | awk 'length > 40' | head -20)

        if [ -n "$paragraphs" ]; then
          can_get_full_text="true"
          first_p=$(echo "$paragraphs" | head -1 | cut -c1-300 | sed 's/\\/\\\\/g; s/"/\\"/g; s/	/ /g' | tr '\n' ' ')
          last_p=$(echo "$paragraphs" | tail -1 | cut -c1-300 | sed 's/\\/\\\\/g; s/"/\\"/g; s/	/ /g' | tr '\n' ' ')
        fi

        # Extract date
        local date_found
        date_found=$(echo "$art_html" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)
        if [ -n "$date_found" ]; then
          pub_date="\"$date_found\""
        fi
      fi
    fi
  fi

  # 3. RSS test
  local has_rss="false"
  local rss_url_found="null"
  local rss_full="false"

  for rss_path in /rss /feed /rss.xml /feed/ /atom.xml /feeds; do
    local rss_test="https://$domain$rss_path"
    local rss_code
    rss_code=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 8 -A "$UA" "$rss_test" 2>/dev/null)
    if [ "$rss_code" -ge 200 ] 2>/dev/null && [ "$rss_code" -lt 400 ] 2>/dev/null; then
      local rss_sample
      rss_sample=$(curl -sL --max-time 8 -A "$UA" "$rss_test" 2>/dev/null | head -c 5000)
      if echo "$rss_sample" | grep -qiE '(<rss|<feed|<channel|<atom|xml version)'; then
        has_rss="true"
        rss_url_found="\"$rss_test\""
        # Check full text in RSS
        local big_content
        big_content=$(curl -sL --max-time 10 -A "$UA" "$rss_test" 2>/dev/null | head -c 20000)
        if echo "$big_content" | grep -qiE '(content:encoded|<content )'; then
          rss_full="true"
        elif echo "$big_content" | grep -oE '<description>[^<]{500,}' | head -1 | grep -q '.'; then
          rss_full="true"
        fi
        break
      fi
    fi
  done

  # Also check for RSS link in HTML
  if [ "$has_rss" = "false" ] && [ -n "$html" ]; then
    local rss_from_html
    rss_from_html=$(echo "$html" | tr '"' '\n' | grep -iE '(rss|feed|atom)\.(xml|rss)' | head -1)
    if [ -z "$rss_from_html" ]; then
      rss_from_html=$(echo "$html" | tr "'" '\n' | grep -iE 'type=.application/(rss|atom)' | head -1)
    fi
    if [ -n "$rss_from_html" ]; then
      # Try fetching it
      local full_rss_url="$rss_from_html"
      if ! echo "$full_rss_url" | grep -q '^http'; then
        full_rss_url="https://$domain$full_rss_url"
      fi
      local rss_code2
      rss_code2=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 8 -A "$UA" "$full_rss_url" 2>/dev/null)
      if [ "$rss_code2" -ge 200 ] 2>/dev/null && [ "$rss_code2" -lt 400 ] 2>/dev/null; then
        local rss_sample2
        rss_sample2=$(curl -sL --max-time 8 -A "$UA" "$full_rss_url" 2>/dev/null | head -c 5000)
        if echo "$rss_sample2" | grep -qiE '(<rss|<feed|<channel|xml version)'; then
          has_rss="true"
          rss_url_found="\"$full_rss_url\""
        fi
      fi
    fi
  fi

  # Build JSON
  local art_url_json="null"
  [ -n "$article_url" ] && art_url_json="\"$article_url\""
  local fp_json="null"
  [ "$first_p" != "null" ] && fp_json="\"$first_p\""
  local lp_json="null"
  [ "$last_p" != "null" ] && lp_json="\"$last_p\""

  printf '    {\n'
  printf '      "source_name": "%s",\n' "$name"
  printf '      "domain": "%s",\n' "$domain"
  printf '      "can_fetch_homepage": %s,\n' "$can_fetch"
  printf '      "homepage_status_code": %s,\n' "${status:-0}"
  printf '      "can_fetch_article": %s,\n' "$can_fetch_article"
  printf '      "can_get_full_text": %s,\n' "$can_get_full_text"
  printf '      "first_paragraph": %s,\n' "$fp_json"
  printf '      "last_paragraph": %s,\n' "$lp_json"
  printf '      "test_article_url": %s,\n' "$art_url_json"
  printf '      "publication_date": %s,\n' "$pub_date"
  printf '      "has_rss": %s,\n' "$has_rss"
  printf '      "rss_url": %s,\n' "$rss_url_found"
  printf '      "rss_has_full_text": %s,\n' "$rss_full"
  printf '      "notes": "%s"\n' "$notes"
  printf '    }'
}

# ============ ROMANIA ============
echo "========== ROMANIA ==========" >&2

{
echo '['
first=true

# Source list: "Name|domain|homepage_url|notes"
ROMANIA_SOURCES=(
  "AGERPRES|agerpres.ro|https://agerpres.ro/english|State news agency; English feed"
  "MApN Press Releases|english.mapn.ro|https://english.mapn.ro/cpresa/|Defense ministry press office; no RSS per docs"
  "MAE Actuality|mae.ro|https://mae.ro/en/actuality|Foreign affairs ministry; no dedicated RSS per docs"
  "G4Media|g4media.ro|https://g4media.ro|Independent digital news; RSS available per docs"
  "Digi24|digi24.ro|https://digi24.ro|TV broadcaster + online portal"
  "HotNews|hotnews.ro|https://hotnews.ro|Digital-native news portal; RSS exists per docs"
  "Recorder|recorder.ro|https://recorder.ro|Independent investigative; video-heavy"
  "RISE Project|riseproject.ro|https://riseproject.ro|Non-profit investigative journalism"
  "Ziarul Financiar|zf.ro|https://zf.ro|Financial daily"
  "Profit.ro|profit.ro|https://profit.ro|Business/economic news; subscription tier"
  "Romania Insider|romania-insider.com|https://romania-insider.com|English-language news; RSS available per docs"
  "Libertatea|libertatea.ro|https://libertatea.ro|General news (Ringier-owned)"
  "PressOne|pressone.ro|https://pressone.ro|Independent investigative/narrative"
  "New Strategy Center|newstrategycenter.ro|https://newstrategycenter.ro/en/|Security/defense think tank"
  "Euronews Romania|euronews.com|https://euronews.com/tag/romania|International broadcast; Romania tag page"
  "Romanian Presidency|presidency.ro|https://presidency.ro|Presidential administration press office"
  "Antena 3 CNN|antena3.ro|https://antena3.ro|TV broadcaster; discourse monitoring source"
)

for src in "${ROMANIA_SOURCES[@]}"; do
  IFS='|' read -r name domain url note <<< "$src"
  if [ "$first" = "true" ]; then
    first=false
  else
    echo ','
  fi
  test_source "$name" "$domain" "$url" "$note"
done

echo ''
echo ']'
} > "$OUTPUT_DIR/romania_accessibility.json"

echo "Romania done" >&2

# ============ FINLAND ============
echo "========== FINLAND ==========" >&2

{
echo '['
first=true

FINLAND_SOURCES=(
  "Yle Uutiset|yle.fi|https://yle.fi/news|Public broadcaster; English at yle.fi/news"
  "Helsingin Sanomat|hs.fi|https://hs.fi|Largest subscription daily; paywalled"
  "Kauppalehti|kauppalehti.fi|https://kauppalehti.fi|Leading business daily; paywalled"
  "Talouselama|talouselama.fi|https://talouselama.fi|Weekly business magazine; paywalled"
  "Ilta-Sanomat|is.fi|https://is.fi|Most-visited Finnish news site; free with ads"
  "Iltalehti|iltalehti.fi|https://iltalehti.fi|Second tabloid; free with ads"
  "Hufvudstadsbladet|hbl.fi|https://hbl.fi|Largest Swedish-language daily; paywalled"
  "Suomen Kuvalehti|suomenkuvalehti.fi|https://suomenkuvalehti.fi|Current-affairs weekly; paywalled"
  "Maanpuolustus-lehti|maanpuolustus-lehti.fi|https://maanpuolustus-lehti.fi|Specialist defense magazine; free online"
  "Long Play|longplay.fi|https://longplay.fi|Slow-journalism outlet; subscription"
  "Uusi Suomi|uusisuomi.fi|https://uusisuomi.fi|Online opinion/analysis platform; free"
  "Verkkouutiset|verkkouutiset.fi|https://verkkouutiset.fi|Kokoomus party organ; free"
  "Kansan Uutiset|kansanuutiset.fi|https://kansanuutiset.fi|Left Alliance party organ; free online"
  "Helsinki Times|helsinkitimes.fi|https://helsinkitimes.fi|English-language outlet; free"
  "Eduskunta|eduskunta.fi|https://eduskunta.fi|Parliament of Finland; official"
  "Valtioneuvosto|valtioneuvosto.fi|https://valtioneuvosto.fi|Government press releases; official"
  "FIIA|fiia.fi|https://fiia.fi|Foreign policy research institute"
)

for src in "${FINLAND_SOURCES[@]}"; do
  IFS='|' read -r name domain url note <<< "$src"
  if [ "$first" = "true" ]; then
    first=false
  else
    echo ','
  fi
  test_source "$name" "$domain" "$url" "$note"
done

echo ''
echo ']'
} > "$OUTPUT_DIR/finland_accessibility.json"

echo "Finland done" >&2
echo "ALL DONE" >&2
