#!/usr/bin/env python3
"""Test accessibility of German news sources for OSINT pipeline."""
import subprocess
import json
import re
import sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def fetch(url, max_time=15):
    """Fetch URL content, return (status_code, body)"""
    try:
        r = subprocess.run(
            ["curl", "-sL", "--max-time", str(max_time), "-A", UA, url],
            capture_output=True, text=True, timeout=max_time + 10
        )
        r2 = subprocess.run(
            ["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", str(max_time), "-A", UA, url],
            capture_output=True, text=True, timeout=max_time + 10
        )
        code = int(r2.stdout.strip()) if r2.stdout.strip().isdigit() else 0
        return code, r.stdout
    except Exception as e:
        return 0, str(e)

def check_rss(url):
    """Check if URL returns valid RSS. Returns (exists, has_full_text, content)"""
    code, body = fetch(url, max_time=10)
    if code not in (200, 301, 302) or not body:
        return False, False, None
    is_rss = '<rss' in body[:500] or '<feed' in body[:500] or '<channel' in body[:2000]
    if not is_rss:
        return False, False, None
    # Check for content:encoded (full text) or long descriptions
    has_content_encoded = 'content:encoded' in body
    descs = re.findall(r'<description[^>]*>(.*?)</description>', body, re.DOTALL)
    if not descs:
        descs = re.findall(r'<content[^>]*>(.*?)</content>', body, re.DOTALL)
    has_full = has_content_encoded or any(len(d) > 500 for d in descs) if descs else has_content_encoded
    return True, has_full, body[:8000]

def extract_article_url(body, domain):
    """Try to find an article URL from homepage HTML"""
    patterns = [
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*\d{{6,}}\.html?[^"]*)"',
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*\d{{4}}[^"]*\.html?[^"]*)"',
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*\d{{4}}/\d{{2}}[^"]*)"',
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*(/[a-z0-9-]+){{3,}}[^"]*)"',
        rf'href="(/[^"]*\d{{4}}/\d{{2}}/[^"]*)"',
        rf'href="(/[^"]*\d{{4}}-\d{{2}}-\d{{2}}[^"]*)"',
    ]
    skip_patterns = re.compile(r'\.(css|js|png|jpg|svg|ico|gif|woff|ttf|pdf|zip)|login|register|cookie|datenschutz|impressum|newsletter|suche|abo|agb|kontakt|#')
    for pat in patterns:
        matches = re.findall(pat, body)
        if matches:
            url = matches[0] if isinstance(matches[0], str) else matches[0][0]
            if not skip_patterns.search(url):
                if url.startswith('/'):
                    url = f"https://{domain}{url}"
                return url
    # Broader: any internal link with article-like path depth
    links = re.findall(rf'href="(https?://[^"]*{re.escape(domain)}/[^"]+)"', body)
    for link in links:
        if not skip_patterns.search(link) and len(link.split('/')) >= 6:
            return link
    return None

def extract_article_url_from_rss(rss_body):
    """Extract first article URL from RSS - specifically from <item> or <entry> blocks"""
    # Try to find links inside <item> blocks first
    items = re.findall(r'<item[^>]*>(.*?)</item>', rss_body, re.DOTALL)
    if items:
        for item in items:
            item_links = re.findall(r'<link>([^<]+)</link>', item)
            if item_links:
                return item_links[0].strip()
            # Also check guid
            guids = re.findall(r'<guid[^>]*>(https?://[^<]+)</guid>', item)
            if guids:
                return guids[0].strip()
    # Try Atom entries
    entries = re.findall(r'<entry[^>]*>(.*?)</entry>', rss_body, re.DOTALL)
    if entries:
        for entry in entries:
            entry_links = re.findall(r'<link[^>]*href="(https?://[^"]+)"', entry)
            if entry_links:
                return entry_links[0].strip()
    # Fallback: skip channel link, find subsequent links
    links = re.findall(r'<link>(https?://[^<]+)</link>', rss_body)
    # Skip links that look like channel/homepage links (no path beyond /)
    for link in links:
        parsed = link.strip().rstrip('/')
        if len(parsed.split('/')) > 3:  # Has a meaningful path
            return link.strip()
    return None

def extract_date_from_rss(rss_body):
    """Extract publication date from first item in RSS"""
    dates = re.findall(r'<pubDate>([^<]+)</pubDate>', rss_body)
    if dates:
        return dates[0].strip()
    dates = re.findall(r'<updated>([^<]+)</updated>', rss_body)
    if dates:
        return dates[0].strip()
    return None

def extract_paragraphs(body):
    """Extract first and last meaningful paragraphs from article HTML"""
    clean = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    paras = re.findall(r'<p[^>]*>(.*?)</p>', clean, re.DOTALL)
    text_paras = []
    for p in paras:
        text = re.sub(r'<[^>]+>', '', p).strip()
        text = re.sub(r'&[a-z]+;', ' ', text)
        text = re.sub(r'&#\d+;', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 60:
            text_paras.append(text[:500])
    first = text_paras[0] if text_paras else None
    last = text_paras[-1] if text_paras else None
    return first, last, len(text_paras)

def extract_date_from_html(body):
    """Extract publication date from article HTML"""
    patterns = [
        r'"datePublished"\s*:\s*"([^"]+)"',
        r'article:published_time"\s+content="([^"]+)"',
        r'datetime="(\d{4}-\d{2}-\d{2}[^"]*)"',
        r'publishedDate["\s:]+(\d{4}-\d{2}-\d{2})',
    ]
    for pat in patterns:
        m = re.search(pat, body)
        if m:
            return m.group(1)
    return None

def test_source(name, domain, homepage_url, rss_urls):
    """Test a single source"""
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
        "notes": ""
    }

    notes = []

    # 1. Test homepage
    hp_code, hp_body = fetch(homepage_url)
    result["homepage_status_code"] = hp_code
    result["can_fetch_homepage"] = 200 <= hp_code < 400 and len(hp_body) > 500
    notes.append(f"Homepage: HTTP {hp_code}, {len(hp_body)} bytes")

    # 2. Test RSS feeds
    rss_body = None
    for rss_url in rss_urls:
        has_rss, has_full, rss_content = check_rss(rss_url)
        if has_rss:
            result["has_rss"] = True
            result["rss_url"] = rss_url
            result["rss_has_full_text"] = has_full
            rss_body = rss_content
            pub_date = extract_date_from_rss(rss_content)
            if pub_date:
                result["publication_date"] = pub_date
            notes.append(f"RSS found at {rss_url}, full_text={has_full}")
            break
    else:
        notes.append(f"No valid RSS found at tested paths")

    # 3. Find article URL
    article_url = None
    if rss_body:
        article_url = extract_article_url_from_rss(rss_body)
    if not article_url and hp_body:
        article_url = extract_article_url(hp_body, domain)

    # 4. Fetch article
    if article_url:
        result["test_article_url"] = article_url
        art_code, art_body = fetch(article_url)
        result["can_fetch_article"] = 200 <= art_code < 400 and len(art_body) > 1000
        if result["can_fetch_article"]:
            first, last, para_count = extract_paragraphs(art_body)
            result["first_paragraph"] = first
            result["last_paragraph"] = last
            result["can_get_full_text"] = para_count >= 3
            if not result["publication_date"]:
                result["publication_date"] = extract_date_from_html(art_body)
            notes.append(f"Article: HTTP {art_code}, {para_count} paragraphs extracted")
        else:
            notes.append(f"Article: HTTP {art_code}, {len(art_body)} bytes - insufficient content")
    else:
        notes.append("Could not find article URL from homepage or RSS")

    result["notes"] = "; ".join(notes)
    return result


# ====== GERMANY ======
germany_sources = [
    ("Frankfurter Allgemeine Zeitung (FAZ)", "www.faz.net", "https://www.faz.net", [
        "https://www.faz.net/rss/aktuell",
        "https://www.faz.net/rss/aktuell/",
        "https://www.faz.net/rss",
        "https://www.faz.net/feed",
    ]),
    ("Sueddeutsche Zeitung (SZ)", "www.sueddeutsche.de", "https://www.sueddeutsche.de", [
        "https://rss.sueddeutsche.de/rss/Topthemen",
        "https://rss.sueddeutsche.de/alles",
        "https://www.sueddeutsche.de/rss",
        "https://www.sueddeutsche.de/feed",
        "https://www.sueddeutsche.de/rss.xml",
    ]),
    ("Die Zeit", "www.zeit.de", "https://www.zeit.de", [
        "https://newsfeed.zeit.de/index",
        "https://newsfeed.zeit.de/all",
        "https://www.zeit.de/rss",
        "https://www.zeit.de/feed",
        "https://www.zeit.de/feeds",
    ]),
    ("Handelsblatt", "www.handelsblatt.com", "https://www.handelsblatt.com", [
        "https://www.handelsblatt.com/contentexport/feed/top-themen",
        "https://www.handelsblatt.com/rss",
        "https://www.handelsblatt.com/feed",
        "https://www.handelsblatt.com/rss.xml",
    ]),
    ("WirtschaftsWoche", "www.wiwo.de", "https://www.wiwo.de", [
        "https://www.wiwo.de/rss/feed",
        "https://www.wiwo.de/rss",
        "https://www.wiwo.de/feed",
        "https://www.wiwo.de/rss.xml",
    ]),
    ("Der Spiegel", "www.spiegel.de", "https://www.spiegel.de", [
        "https://www.spiegel.de/schlagzeilen/index.rss",
        "https://www.spiegel.de/politik/index.rss",
        "https://www.spiegel.de/rss",
        "https://www.spiegel.de/feed",
    ]),
    ("Die Welt", "www.welt.de", "https://www.welt.de", [
        "https://www.welt.de/feeds/latest.rss",
        "https://www.welt.de/feeds/topnews.rss",
        "https://www.welt.de/rss",
        "https://www.welt.de/feed",
    ]),
    ("taz (Die Tageszeitung)", "taz.de", "https://taz.de", [
        "https://taz.de/!p4608;rss/",
        "https://taz.de/rss.xml",
        "https://taz.de/feed",
        "https://taz.de/rss",
    ]),
    ("Der Tagesspiegel", "www.tagesspiegel.de", "https://www.tagesspiegel.de", [
        "https://www.tagesspiegel.de/contentexport/feed/home",
        "https://www.tagesspiegel.de/rss",
        "https://www.tagesspiegel.de/feed",
        "https://www.tagesspiegel.de/rss.xml",
    ]),
    ("Politico Europe", "www.politico.eu", "https://www.politico.eu", [
        "https://www.politico.eu/feed/",
        "https://www.politico.eu/rss",
        "https://www.politico.eu/feed",
    ]),
    ("Deutsche Welle (DW)", "www.dw.com", "https://www.dw.com", [
        "https://rss.dw.com/xml/rss-en-all",
        "https://rss.dw.com/rdf/rss-en-all",
        "https://www.dw.com/rss",
        "https://www.dw.com/feed",
    ]),
    ("SWP (Stiftung Wissenschaft und Politik)", "www.swp-berlin.org", "https://www.swp-berlin.org", [
        "https://www.swp-berlin.org/feed",
        "https://www.swp-berlin.org/rss",
        "https://www.swp-berlin.org/rss.xml",
        "https://www.swp-berlin.org/feed.xml",
    ]),
    ("DGAP", "dgap.org", "https://dgap.org", [
        "https://dgap.org/feed",
        "https://dgap.org/rss",
        "https://dgap.org/rss.xml",
        "https://dgap.org/feed.xml",
    ]),
    ("Internationale Politik Quarterly (IPQ)", "internationalepolitik.de", "https://internationalepolitik.de", [
        "https://internationalepolitik.de/feed",
        "https://internationalepolitik.de/rss",
        "https://internationalepolitik.de/rss.xml",
    ]),
    ("Bundesregierung", "www.bundesregierung.de", "https://www.bundesregierung.de", [
        "https://www.bundesregierung.de/breg-de/feed",
        "https://www.bundesregierung.de/rss",
        "https://www.bundesregierung.de/feed",
        "https://www.bundesregierung.de/rss.xml",
    ]),
    ("Auswaertiges Amt", "www.auswaertiges-amt.de", "https://www.auswaertiges-amt.de", [
        "https://www.auswaertiges-amt.de/rss",
        "https://www.auswaertiges-amt.de/feed",
        "https://www.auswaertiges-amt.de/rss.xml",
    ]),
    ("Frankfurter Rundschau", "www.fr.de", "https://www.fr.de", [
        "https://www.fr.de/rssfeed.rdf",
        "https://www.fr.de/rss",
        "https://www.fr.de/feed",
        "https://www.fr.de/rss.xml",
    ]),
    ("n-tv", "www.n-tv.de", "https://www.n-tv.de", [
        "https://www.n-tv.de/rss",
        "https://www.n-tv.de/feed",
        "https://www.n-tv.de/rss.xml",
    ]),
    ("IPG Journal (Friedrich-Ebert-Stiftung)", "www.ipg-journal.de", "https://www.ipg-journal.de", [
        "https://www.ipg-journal.de/feed",
        "https://www.ipg-journal.de/rss",
        "https://www.ipg-journal.de/rss.xml",
        "https://www.ipg-journal.de/feed.xml",
    ]),
]

def run_tests(sources, output_path, country_name):
    results = []
    for i, (name, domain, homepage, rss_urls) in enumerate(sources):
        print(f"  [{i+1}/{len(sources)}] Testing {name}...", file=sys.stderr)
        result = test_source(name, domain, homepage, rss_urls)
        results.append(result)
        hp = "OK" if result["can_fetch_homepage"] else "FAIL"
        art = "OK" if result["can_fetch_article"] else "FAIL"
        ft = "OK" if result["can_get_full_text"] else "FAIL"
        rss = "OK" if result["has_rss"] else "FAIL"
        print(f"    HP={hp} ART={art} FT={ft} RSS={rss}", file=sys.stderr)

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n{country_name}: Wrote {len(results)} results to {output_path}", file=sys.stderr)
    return results

if __name__ == "__main__":
    print("=" * 60, file=sys.stderr)
    print("GERMANY SOURCE ACCESSIBILITY TESTS", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    output_path = "/Users/zen/dev/src/pdb/docs/source_intelligence_maps/tests/germany_accessibility.json"
    results = run_tests(germany_sources, output_path, "Germany")

    # Summary
    print("\n=== SUMMARY ===")
    hp_ok = sum(1 for r in results if r["can_fetch_homepage"])
    art_ok = sum(1 for r in results if r["can_fetch_article"])
    ft_ok = sum(1 for r in results if r["can_get_full_text"])
    rss_ok = sum(1 for r in results if r["has_rss"])
    rss_ft = sum(1 for r in results if r["rss_has_full_text"])
    print(f"\nGERMANY ({len(results)} sources):")
    print(f"  Homepage fetchable:    {hp_ok}/{len(results)}")
    print(f"  Article fetchable:     {art_ok}/{len(results)}")
    print(f"  Full text extractable: {ft_ok}/{len(results)}")
    print(f"  Has RSS:               {rss_ok}/{len(results)}")
    print(f"  RSS has full text:     {rss_ft}/{len(results)}")
