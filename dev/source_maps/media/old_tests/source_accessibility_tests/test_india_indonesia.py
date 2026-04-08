#!/usr/bin/env python3
"""Test source accessibility for India and Indonesia OSINT pipeline sources."""
import subprocess
import json
import re
import sys
import html as html_mod

def curl_status(url, timeout=10):
    try:
        r = subprocess.run(
            ["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", str(timeout), url],
            capture_output=True, text=True, timeout=timeout+5
        )
        return int(r.stdout.strip()) if r.stdout.strip().isdigit() else 0
    except Exception:
        return 0

def curl_get(url, timeout=15, max_bytes=80000):
    try:
        r = subprocess.run(
            ["curl", "-sL", "--max-time", str(timeout),
             "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
             "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
             url],
            capture_output=True, text=True, timeout=timeout+5
        )
        return r.stdout[:max_bytes] if r.stdout else ""
    except Exception:
        return ""

def extract_article_urls(html_content, domain):
    urls = []
    all_hrefs = re.findall(r'href="([^"]+)"', html_content)
    for href in all_hrefs:
        if any(x in href.lower() for x in [
            '.css', '.js', '.png', '.jpg', '.svg', '.ico', '.woff', '.webmanifest',
            '.json', '.xml', '#', 'cookie', 'login', 'subscribe', 'suscri',
            'favicon', 'assets/', 'static/', 'fonts/', 'images/', 'manifest',
            'oembed', 'wp-json', 'wp-content', 'wp-includes',
            'javascript:', 'mailto:', 'tel:', 'about:',
        ]):
            continue
        abs_url = href
        if href.startswith('/') and not href.startswith('//'):
            abs_url = f"https://{domain}{href}"
        elif href.startswith('//'):
            abs_url = f"https:{href}"
        if domain not in abs_url and not href.startswith('/'):
            continue
        path = abs_url.split(domain, 1)[-1] if domain in abs_url else href
        segments = [s for s in path.split('/') if s]
        if len(segments) < 2:
            continue
        is_article = False
        if re.search(r'\d{4}[-/]\d{2}', path):
            is_article = True
        elif path.endswith('.html') or path.endswith('.htm') or path.endswith('.ece') or path.endswith('.cms'):
            is_article = True
        elif len(segments) >= 2 and len(segments[-1]) > 10 and '-' in segments[-1]:
            is_article = True
        elif re.search(r'/article/', path) or re.search(r'/press-release/', path):
            is_article = True
        elif re.search(r'/berita/', path) or re.search(r'/news/', path):
            is_article = True
        elif re.search(r'/PRID=', path):
            is_article = True
        if is_article:
            urls.append(abs_url)
    seen = set()
    unique = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique.append(u)
    return unique[:10]

def extract_paragraphs(html_content):
    p_tags = re.findall(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL)
    paragraphs = []
    for p in p_tags:
        text = re.sub(r'<[^>]+>', '', p).strip()
        text = re.sub(r'\s+', ' ', text)
        text = html_mod.unescape(text)
        if len(text) > 50:
            paragraphs.append(text)
    return paragraphs

def extract_date(html_content):
    patterns = [
        r'"datePublished"\s*:\s*"([^"]+)"',
        r'content="(\d{4}-\d{2}-\d{2}[T ][^"]*)"[^>]*property="article:published',
        r'property="article:published[^"]*"[^>]*content="([^"]+)"',
        r'"publishedDate"\s*:\s*"([^"]+)"',
        r'datetime="(\d{4}-\d{2}-\d{2}[^"]*)"',
        r'"dateCreated"\s*:\s*"([^"]+)"',
        r'<time[^>]*>(\d{1,2}[./]\d{1,2}[./]\d{4})</time>',
        r'"date_published"\s*:\s*"([^"]+)"',
    ]
    for pat in patterns:
        m = re.search(pat, html_content)
        if m:
            return m.group(1)[:25]
    return None

KNOWN_RSS = {
    # India
    "thehindu.com": "https://www.thehindu.com/feeder/default.rss",
    "indianexpress.com": "https://indianexpress.com/feed/",
    "hindustantimes.com": "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml",
    "economictimes.indiatimes.com": "https://economictimes.indiatimes.com/rssfeeds/1977021501.cms",
    "livemint.com": "https://www.livemint.com/rss/news",
    "pib.gov.in": "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3",
    "idsa.in": "https://www.idsa.in/rss/idsacomments-rss.xml",
    "sansadtv.nic.in": "https://sansadtv.nic.in/rss",
    # Indonesia
    "antaranews.com": "https://antaranews.com/rss/terkini",
    "en.antaranews.com": "https://en.antaranews.com/rss/news",
    "thejakartapost.com": "https://www.thejakartapost.com/rss",
    "detik.com": "https://rss.detik.com/index.php/detikcom",
    "republika.co.id": "https://www.republika.co.id/rss",
    "fulcrum.sg": "https://fulcrum.sg/feed/",
}

KNOWN_SECTIONS = {
    # India
    "mea.gov.in": "https://mea.gov.in/press-releases.htm",
    "pib.gov.in": "https://pib.gov.in/allRel.aspx",
    "thehindu.com": "https://www.thehindu.com/news/international/",
    "theprint.in": "https://theprint.in/defence/",
    "orfonline.org": "https://www.orfonline.org/expert-speak",
    "idsa.in": "https://www.idsa.in/idsacomments",
    "carnegieindia.org": "https://carnegieindia.org/research",
    "takshashila.org.in": "https://takshashila.org.in/research",
    "jagran.com": "https://www.jagran.com/news/national-news",
    "forceindia.net": "https://forceindia.net",
    # Indonesia
    "kompas.id": "https://www.kompas.id/",
    "kompas.com": "https://news.kompas.com/",
    "tempo.co": "https://nasional.tempo.co/",
    "en.tempo.co": "https://en.tempo.co/",
    "kemlu.go.id": "https://kemlu.go.id/portal/id/list/berita/84/press-release",
    "setkab.go.id": "https://setkab.go.id/",
    "csis.or.id": "https://www.csis.or.id/publications",
    "bisnis.com": "https://www.bisnis.com/",
    "cnnindonesia.com": "https://www.cnnindonesia.com/nasional",
    "cnbcindonesia.com": "https://www.cnbcindonesia.com/news",
    "kontan.co.id": "https://nasional.kontan.co.id/",
    "kemhan.go.id": "https://www.kemhan.go.id/",
}

def test_rss(domain):
    if domain in KNOWN_RSS:
        url = KNOWN_RSS[domain]
        content = curl_get(url, timeout=10, max_bytes=15000)
        if content and re.search(r'<rss|<feed|<channel|xmlns.*atom|<\?xml', content, re.IGNORECASE):
            has_full = bool(re.search(r'<(content:encoded|content|description)[^>]*>.{500,}', content, re.DOTALL))
            return True, url, has_full
    for path in ["/rss", "/feed", "/feed/", "/rss.xml", "/feeds", "/atom.xml", "/rss/", "/feed/rss"]:
        url = f"https://{domain}{path}"
        if url == KNOWN_RSS.get(domain):
            continue
        content = curl_get(url, timeout=10, max_bytes=10000)
        if content and re.search(r'<rss|<feed|<channel|xmlns.*atom', content[:500], re.IGNORECASE):
            has_full = bool(re.search(r'<(content:encoded|content|description)[^>]*>.{500,}', content, re.DOTALL))
            return True, url, has_full
    # Also try www variant
    for path in ["/rss", "/feed", "/feed/", "/rss.xml"]:
        url = f"https://www.{domain}{path}"
        content = curl_get(url, timeout=10, max_bytes=10000)
        if content and re.search(r'<rss|<feed|<channel|xmlns.*atom', content[:500], re.IGNORECASE):
            has_full = bool(re.search(r'<(content:encoded|content|description)[^>]*>.{500,}', content, re.DOTALL))
            return True, url, has_full
    return False, None, False

def find_article_from_rss(domain):
    if domain in KNOWN_RSS:
        rss_content = curl_get(KNOWN_RSS[domain], timeout=10, max_bytes=15000)
        if rss_content:
            links = re.findall(r'<link>([^<]+)</link>', rss_content)
            links += re.findall(r'<link[^>]*href="([^"]+)"', rss_content)
            for link in links:
                link = link.strip()
                if (domain in link or domain.split('.')[-2] in link) and len(link) > 30:
                    # Skip the channel link (just domain)
                    path = link.replace(f"https://", "").replace(f"http://", "")
                    if path.count('/') >= 2:
                        return link
    return None

def test_source(name, domain):
    print(f"  Testing: {name} ({domain})", file=sys.stderr)
    result = {
        "source_name": name,
        "domain": domain,
        "can_fetch_homepage": False,
        "can_fetch_article": False,
        "can_get_full_text": False,
        "first_paragraph": None,
        "last_paragraph": None,
        "test_article_url": None,
        "publication_date": None,
        "has_rss": False,
        "rss_url": None,
        "rss_has_full_text": False,
        "notes": ""
    }
    notes = []

    # 1. Homepage
    status = curl_status(f"https://{domain}")
    result["can_fetch_homepage"] = 200 <= status < 400
    if not result["can_fetch_homepage"]:
        www_status = curl_status(f"https://www.{domain}")
        if 200 <= www_status < 400:
            result["can_fetch_homepage"] = True
            notes.append(f"Requires www prefix (bare domain returned {status})")

    # 2. Find article
    article_url = None

    # Try homepage first
    homepage_html = curl_get(f"https://{domain}")
    article_urls = extract_article_urls(homepage_html, domain)
    if not article_urls:
        www_html = curl_get(f"https://www.{domain}")
        article_urls = extract_article_urls(www_html, domain)
        if not article_urls:
            article_urls = extract_article_urls(www_html, f"www.{domain}")

    # Try known section page
    if not article_urls and domain in KNOWN_SECTIONS:
        section_html = curl_get(KNOWN_SECTIONS[domain], timeout=15)
        if section_html:
            section_domain = KNOWN_SECTIONS[domain].split('/')[2]
            article_urls = extract_article_urls(section_html, section_domain)
            if not article_urls:
                article_urls = extract_article_urls(section_html, domain)

    # Try RSS
    if not article_urls:
        rss_article = find_article_from_rss(domain)
        if rss_article:
            article_urls = [rss_article]

    article_url = article_urls[0] if article_urls else None

    if article_url:
        result["test_article_url"] = article_url
        article_status = curl_status(article_url)
        result["can_fetch_article"] = 200 <= article_status < 400

        if result["can_fetch_article"]:
            article_html = curl_get(article_url)
            paragraphs = extract_paragraphs(article_html)
            if paragraphs:
                result["can_get_full_text"] = len(paragraphs) >= 3
                result["first_paragraph"] = paragraphs[0][:300]
                result["last_paragraph"] = paragraphs[-1][:300] if len(paragraphs) > 1 else paragraphs[0][:300]
            else:
                notes.append("No paragraphs extracted - JS-rendered or paywalled")
            pub_date = extract_date(article_html)
            result["publication_date"] = pub_date
        else:
            notes.append(f"Article returned HTTP {article_status}")
    else:
        notes.append("No article links found on homepage, section page, or via RSS")

    # 3. RSS
    has_rss, rss_url, rss_full = test_rss(domain)
    result["has_rss"] = has_rss
    result["rss_url"] = rss_url
    result["rss_has_full_text"] = rss_full
    if not has_rss:
        notes.append("No RSS feed found")

    result["notes"] = "; ".join(notes) if notes else "OK"
    return result

# India sources
india_sources = [
    ("Ministry of External Affairs", "mea.gov.in"),
    ("Press Information Bureau", "pib.gov.in"),
    ("The Hindu", "thehindu.com"),
    ("The Indian Express", "indianexpress.com"),
    ("Hindustan Times", "hindustantimes.com"),
    ("ThePrint", "theprint.in"),
    ("The Wire", "thewire.in"),
    ("The Economic Times", "economictimes.indiatimes.com"),
    ("LiveMint", "livemint.com"),
    ("Observer Research Foundation", "orfonline.org"),
    ("MP-IDSA", "idsa.in"),
    ("Carnegie India", "carnegieindia.org"),
    ("Gateway House", "gatewayhouse.in"),
    ("Takshashila Institution", "takshashila.org.in"),
    ("Economic and Political Weekly", "epw.in"),
    ("Dainik Jagran", "jagran.com"),
    ("Dainik Bhaskar", "bhaskar.com"),
    ("Sansad TV", "sansadtv.nic.in"),
    ("FORCE Magazine", "forceindia.net"),
]

# Indonesia sources
indonesia_sources = [
    ("Antara News Agency", "antaranews.com"),
    ("Kompas", "kompas.id"),
    ("Kompas.com", "kompas.com"),
    ("Tempo", "tempo.co"),
    ("Tempo English", "en.tempo.co"),
    ("The Jakarta Post", "thejakartapost.com"),
    ("Jakarta Globe", "jakartaglobe.id"),
    ("Detik.com", "detik.com"),
    ("CNN Indonesia", "cnnindonesia.com"),
    ("CNBC Indonesia", "cnbcindonesia.com"),
    ("Kontan", "kontan.co.id"),
    ("Tirto.id", "tirto.id"),
    ("Republika", "republika.co.id"),
    ("Ministry of Foreign Affairs (Kemlu)", "kemlu.go.id"),
    ("Cabinet Secretariat (Setkab)", "setkab.go.id"),
    ("CSIS Jakarta", "csis.or.id"),
    ("Fulcrum / ISEAS", "fulcrum.sg"),
    ("Bisnis Indonesia", "bisnis.com"),
    ("Ministry of Defense (Kemhan)", "kemhan.go.id"),
]

output_dir = "/Users/zen/dev/src/pdb/docs/source_intelligence_maps/tests"

# Test India
print("=== Testing India sources ===", file=sys.stderr)
india_results = []
for name, domain in india_sources:
    india_results.append(test_source(name, domain))

with open(f"{output_dir}/india_accessibility.json", "w") as f:
    json.dump(india_results, f, indent=2, ensure_ascii=False)
print("India results written", file=sys.stderr)

# Test Indonesia
print("\n=== Testing Indonesia sources ===", file=sys.stderr)
indonesia_results = []
for name, domain in indonesia_sources:
    indonesia_results.append(test_source(name, domain))

with open(f"{output_dir}/indonesia_accessibility.json", "w") as f:
    json.dump(indonesia_results, f, indent=2, ensure_ascii=False)
print("Indonesia results written", file=sys.stderr)

# Summary
print("\n=== SUMMARY ===", file=sys.stderr)
for label, results in [("India", india_results), ("Indonesia", indonesia_results)]:
    hp_ok = sum(1 for r in results if r["can_fetch_homepage"])
    art_ok = sum(1 for r in results if r["can_fetch_article"])
    ft_ok = sum(1 for r in results if r["can_get_full_text"])
    rss_ok = sum(1 for r in results if r["has_rss"])
    print(f"\n{label}: {hp_ok}/{len(results)} homepage, {art_ok}/{len(results)} article, {ft_ok}/{len(results)} full-text, {rss_ok}/{len(results)} RSS", file=sys.stderr)
    for r in results:
        status = "OK" if r["can_fetch_article"] else "FAIL"
        rss_s = "RSS" if r["has_rss"] else "no-RSS"
        ft_s = "FT" if r["can_get_full_text"] else "no-FT"
        print(f"  [{status}] [{rss_s}] [{ft_s}] {r['source_name']} ({r['domain']}) - {r['notes']}", file=sys.stderr)

print("\nDONE")
