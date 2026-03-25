#!/usr/bin/env python3
"""Test source accessibility for Romania and Finland OSINT pipeline."""
import subprocess
import json
import re
import sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

def curl_status(url, timeout=10):
    """Get HTTP status code."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", str(timeout), "-A", UA, url],
            capture_output=True, text=True, timeout=timeout+5
        )
        return int(r.stdout.strip()) if r.stdout.strip().isdigit() else 0
    except Exception:
        return 0

def curl_get(url, timeout=15, max_bytes=80000):
    """Fetch URL content."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "--max-time", str(timeout), "-A", UA, url],
            capture_output=True, text=True, timeout=timeout+5
        )
        return r.stdout[:max_bytes] if r.stdout else ""
    except Exception:
        return ""

def extract_article_urls(html, domain):
    """Extract article URLs from homepage HTML."""
    # Blocklist for non-article paths
    blocklist = ['.css', '.js', '.png', '.jpg', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.eot',
                 '.gif', '.webp', '.mp4', '.mp3', '.pdf', '.zip',
                 '#', 'cookie', 'login', 'subscribe', 'register', 'signup',
                 'wp-json', 'wp-content/themes', 'wp-content/plugins', 'wp-includes',
                 '/feed', '/rss', '/atom', '/sitemap', '/robots',
                 '/tag/', '/category/', '/author/', '/page/', '/search',
                 '/static/', '/assets/', '/fonts/', '/images/', '/img/',
                 'oembed', 'embed?', 'webmanifest', 'favicon',
                 'javascript:', 'mailto:', 'tel:']

    urls = []
    all_hrefs = re.findall(r'href=["\']([^"\']+)["\']', html)

    for href in all_hrefs:
        # Skip blocked patterns
        if any(b in href.lower() for b in blocklist):
            continue

        # Build full URL
        full_url = href
        if href.startswith('/') and not href.startswith('//'):
            full_url = f"https://{domain}{href}"
        elif href.startswith('//'):
            full_url = f"https:{href}"
        elif not href.startswith('http'):
            continue

        # Must be on the same domain (or www variant)
        if domain not in full_url and f"www.{domain}" not in full_url:
            continue

        # Get the path
        path_match = re.search(r'https?://[^/]+(/.+)', full_url)
        if not path_match:
            continue
        path = path_match.group(1)

        # Must look like an article URL (has meaningful path depth or date patterns)
        is_article = False
        # Has date pattern like /2026/03/ or /2026-03-
        if re.search(r'/20\d{2}[-/]\d{2}', path):
            is_article = True
        # Has slug-like segments (multiple path segments with hyphens)
        elif re.search(r'/[a-z0-9]+-[a-z0-9]+-[a-z0-9]+', path):
            is_article = True
        # Has UUID-like segment
        elif re.search(r'/[a-f0-9]{8}-[a-f0-9]{4}', path):
            is_article = True
        # Has a .html extension
        elif path.endswith('.html') or path.endswith('.htm'):
            is_article = True
        # Has numeric article ID at end
        elif re.search(r'/\d{5,}$', path):
            is_article = True
        # Has path depth >= 3 segments
        elif path.count('/') >= 3 and len(path) > 20:
            is_article = True

        if is_article:
            urls.append(full_url)

    return urls[:5]

def extract_paragraphs(html):
    """Extract paragraphs from article HTML."""
    p_tags = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    paragraphs = []
    for p in p_tags:
        text = re.sub(r'<[^>]+>', '', p).strip()
        text = re.sub(r'&nbsp;', ' ', text)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'&#\d+;', '', text)
        text = re.sub(r'&\w+;', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 40:
            paragraphs.append(text)
    return paragraphs

def extract_date(html):
    """Extract publication date from article HTML."""
    patterns = [
        r'"datePublished"\s*:\s*"([^"]+)"',
        r'content="(\d{4}-\d{2}-\d{2}[T ][^"]*)"[^>]*property="article:published',
        r'property="article:published[^"]*"[^>]*content="([^"]+)"',
        r'"publishedDate"\s*:\s*"([^"]+)"',
        r'datetime="(\d{4}-\d{2}-\d{2}[^"]*)"',
        r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})',
    ]
    for pat in patterns:
        m = re.search(pat, html)
        if m:
            return m.group(1)[:25]
    return None

def test_rss(domain):
    """Test RSS feed availability."""
    rss_paths = ["/rss", "/feed", "/feed/", "/rss.xml", "/atom.xml", "/feeds",
                 "/rss/rss.cshtml", "/index.xml", "/news/rss", "/en/rss"]
    for path in rss_paths:
        url = f"https://{domain}{path}"
        content = curl_get(url, timeout=8, max_bytes=20000)
        if content and re.search(r'<rss|<feed|<channel|<atom|xmlns.*atom|<\?xml', content, re.IGNORECASE):
            has_full = bool(re.search(r'<(content:encoded|content)[^>]*>.{500,}', content, re.DOTALL))
            if not has_full:
                has_full = bool(re.search(r'<description>[^<]{500,}', content))
            return True, url, has_full
    # Also try www variant
    for path in ["/rss", "/feed", "/feed/"]:
        url = f"https://www.{domain}{path}"
        content = curl_get(url, timeout=8, max_bytes=20000)
        if content and re.search(r'<rss|<feed|<channel|<atom|xmlns.*atom|<\?xml', content, re.IGNORECASE):
            has_full = bool(re.search(r'<(content:encoded|content)[^>]*>.{500,}', content, re.DOTALL))
            if not has_full:
                has_full = bool(re.search(r'<description>[^<]{500,}', content))
            return True, url, has_full
    return False, None, False

def extract_article_from_rss(rss_url):
    """Extract first article URL from RSS feed."""
    if not rss_url:
        return None
    content = curl_get(rss_url, timeout=10, max_bytes=10000)
    links = re.findall(r'<link>([^<]+)</link>', content)
    for link in links:
        link = link.strip()
        if link and re.search(r'/20\d{2}|/[a-z]+-[a-z]+-[a-z]+|/\d{5,}', link):
            return link
    # Try guid links
    guids = re.findall(r'<guid[^>]*>([^<]+)</guid>', content)
    for g in guids:
        g = g.strip()
        if g.startswith('http'):
            return g
    return None

def test_source(name, domain, homepage_url, source_notes):
    """Test a single source."""
    print(f"  Testing: {name} ({domain})", file=sys.stderr, flush=True)

    result = {
        "source_name": name,
        "domain": domain,
        "can_fetch_homepage": False,
        "homepage_status_code": 0,
        "can_fetch_article": False,
        "can_get_full_text": False,
        "first_paragraph": None,
        "last_paragraph": None,
        "test_article_url": None,
        "publication_date": None,
        "has_rss": False,
        "rss_url": None,
        "rss_has_full_text": False,
        "notes": source_notes
    }

    # 1. Homepage test
    status = curl_status(homepage_url)
    result["homepage_status_code"] = status
    result["can_fetch_homepage"] = 200 <= status < 400

    notes_extra = []

    # 2. Find and fetch article
    article_url = None
    if result["can_fetch_homepage"]:
        homepage_html = curl_get(homepage_url)
        article_urls = extract_article_urls(homepage_html, domain)
        if article_urls:
            article_url = article_urls[0]
    else:
        notes_extra.append(f"Homepage returned status {status}")

    # 3. RSS test (do this before article fetch so we can use RSS as fallback)
    has_rss, rss_url, rss_full = test_rss(domain)
    result["has_rss"] = has_rss
    result["rss_url"] = rss_url
    result["rss_has_full_text"] = rss_full

    # If no article from homepage, try extracting from RSS
    if not article_url and has_rss:
        article_url = extract_article_from_rss(rss_url)
        if article_url:
            notes_extra.append("Article URL extracted from RSS feed (not homepage)")

    if not article_url:
        notes_extra.append("No article links found on homepage or RSS")

    if article_url:
        result["test_article_url"] = article_url
        article_status = curl_status(article_url)
        result["can_fetch_article"] = 200 <= article_status < 400

        if result["can_fetch_article"]:
            article_html = curl_get(article_url)
            paragraphs = extract_paragraphs(article_html)

            if paragraphs:
                result["can_get_full_text"] = len(paragraphs) >= 2
                result["first_paragraph"] = paragraphs[0][:300]
                result["last_paragraph"] = paragraphs[-1][:300] if len(paragraphs) > 1 else paragraphs[0][:300]
            else:
                notes_extra.append("No paragraphs extracted - may be JS-rendered or paywalled")

            result["publication_date"] = extract_date(article_html)

    if notes_extra:
        result["notes"] = result["notes"] + "; " + "; ".join(notes_extra)

    return result

output_dir = "/Users/zen/dev/src/pdb/docs/source_intelligence_maps/tests"

# ROMANIA
print("=== Testing Romania sources ===", file=sys.stderr, flush=True)
romania_sources = [
    ("AGERPRES", "agerpres.ro", "https://agerpres.ro/english", "State news agency; English feed"),
    ("MApN Press Releases", "english.mapn.ro", "https://english.mapn.ro/cpresa/", "Defense ministry press office; no RSS per docs"),
    ("MAE Actuality", "mae.ro", "https://mae.ro/en/actuality", "Foreign affairs ministry; no dedicated RSS per docs"),
    ("G4Media", "g4media.ro", "https://g4media.ro", "Independent digital news; RSS available per docs"),
    ("Digi24", "digi24.ro", "https://digi24.ro", "TV broadcaster + online portal"),
    ("HotNews", "hotnews.ro", "https://hotnews.ro", "Digital-native news portal; RSS exists per docs"),
    ("Recorder", "recorder.ro", "https://recorder.ro", "Independent investigative; video-heavy"),
    ("RISE Project", "riseproject.ro", "https://riseproject.ro", "Non-profit investigative journalism"),
    ("Ziarul Financiar", "zf.ro", "https://zf.ro", "Financial daily"),
    ("Profit.ro", "profit.ro", "https://profit.ro", "Business/economic news; subscription tier"),
    ("Romania Insider", "romania-insider.com", "https://romania-insider.com", "English-language news; RSS available per docs"),
    ("Libertatea", "libertatea.ro", "https://libertatea.ro", "General news (Ringier-owned)"),
    ("PressOne", "pressone.ro", "https://pressone.ro", "Independent investigative/narrative"),
    ("New Strategy Center", "newstrategycenter.ro", "https://newstrategycenter.ro/en/", "Security/defense think tank"),
    ("Euronews Romania", "euronews.com", "https://euronews.com/tag/romania", "International broadcast; Romania tag page"),
    ("Romanian Presidency", "presidency.ro", "https://presidency.ro", "Presidential administration press office"),
    ("Antena 3 CNN", "antena3.ro", "https://antena3.ro", "TV broadcaster; discourse monitoring source"),
]

romania_results = []
for name, domain, url, notes in romania_sources:
    romania_results.append(test_source(name, domain, url, notes))

with open(f"{output_dir}/romania_accessibility.json", "w") as f:
    json.dump(romania_results, f, indent=2, ensure_ascii=False)
print(f"Romania results written to {output_dir}/romania_accessibility.json", file=sys.stderr, flush=True)

# FINLAND
print("\n=== Testing Finland sources ===", file=sys.stderr, flush=True)
finland_sources = [
    ("Yle Uutiset", "yle.fi", "https://yle.fi/news", "Public broadcaster; English at yle.fi/news"),
    ("Helsingin Sanomat", "hs.fi", "https://hs.fi", "Largest subscription daily; paywalled"),
    ("Kauppalehti", "kauppalehti.fi", "https://kauppalehti.fi", "Leading business daily; paywalled"),
    ("Talouselama", "talouselama.fi", "https://talouselama.fi", "Weekly business magazine; paywalled"),
    ("Ilta-Sanomat", "is.fi", "https://is.fi", "Most-visited Finnish news site; free with ads"),
    ("Iltalehti", "iltalehti.fi", "https://iltalehti.fi", "Second tabloid; free with ads"),
    ("Hufvudstadsbladet", "hbl.fi", "https://hbl.fi", "Largest Swedish-language daily; paywalled"),
    ("Suomen Kuvalehti", "suomenkuvalehti.fi", "https://suomenkuvalehti.fi", "Current-affairs weekly; paywalled"),
    ("Maanpuolustus-lehti", "maanpuolustus-lehti.fi", "https://maanpuolustus-lehti.fi", "Specialist defense magazine; free online"),
    ("Long Play", "longplay.fi", "https://longplay.fi", "Slow-journalism outlet; subscription"),
    ("Uusi Suomi", "uusisuomi.fi", "https://uusisuomi.fi", "Online opinion/analysis platform; free"),
    ("Verkkouutiset", "verkkouutiset.fi", "https://verkkouutiset.fi", "Kokoomus party organ; free"),
    ("Kansan Uutiset", "kansanuutiset.fi", "https://kansanuutiset.fi", "Left Alliance party organ; free online"),
    ("Helsinki Times", "helsinkitimes.fi", "https://helsinkitimes.fi", "English-language outlet; free"),
    ("Eduskunta", "eduskunta.fi", "https://eduskunta.fi", "Parliament of Finland; official"),
    ("Valtioneuvosto", "valtioneuvosto.fi", "https://valtioneuvosto.fi", "Government press releases; official"),
    ("FIIA", "fiia.fi", "https://fiia.fi", "Foreign policy research institute"),
]

finland_results = []
for name, domain, url, notes in finland_sources:
    finland_results.append(test_source(name, domain, url, notes))

with open(f"{output_dir}/finland_accessibility.json", "w") as f:
    json.dump(finland_results, f, indent=2, ensure_ascii=False)
print(f"Finland results written to {output_dir}/finland_accessibility.json", file=sys.stderr, flush=True)

# Summary
print("\n=== SUMMARY ===", file=sys.stderr, flush=True)
for label, results in [("Romania", romania_results), ("Finland", finland_results)]:
    hp_ok = sum(1 for r in results if r["can_fetch_homepage"])
    art_ok = sum(1 for r in results if r["can_fetch_article"])
    ft_ok = sum(1 for r in results if r["can_get_full_text"])
    rss_ok = sum(1 for r in results if r["has_rss"])
    print(f"{label}: {hp_ok}/{len(results)} homepage, {art_ok}/{len(results)} article, {ft_ok}/{len(results)} full-text, {rss_ok}/{len(results)} RSS", file=sys.stderr, flush=True)

print("DONE")
