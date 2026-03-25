#!/usr/bin/env python3
"""Test accessibility of UK news sources for OSINT pipeline."""
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
            capture_output=True, text=True, timeout=25
        )
        r2 = subprocess.run(
            ["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", str(max_time), "-A", UA, url],
            capture_output=True, text=True, timeout=25
        )
        code = int(r2.stdout.strip()) if r2.stdout.strip().isdigit() else 0
        return code, r.stdout
    except Exception as e:
        return 0, str(e)

def check_rss(url):
    """Check if URL returns valid RSS. Returns (exists, has_full_text, content)"""
    code, body = fetch(url, max_time=10)
    if code != 200 or not body:
        return False, False, None
    is_rss = '<rss' in body[:500] or '<feed' in body[:500] or '<channel' in body[:2000]
    if not is_rss:
        return False, False, None
    descs = re.findall(r'<description[^>]*>(.*?)</description>', body, re.DOTALL)
    if not descs:
        descs = re.findall(r'<content[^>]*>(.*?)</content>', body, re.DOTALL)
    has_full = any(len(d) > 500 for d in descs) if descs else False
    return True, has_full, body[:20000]

def extract_article_url(body, domain):
    """Try to find an article URL from homepage HTML"""
    patterns = [
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*\d{{4}}[^"]*)"',
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*article[s]?/[^"]*)"',
        rf'href="(/news/articles/[^"]+)"',
        rf'href="(/[^"]*\d{{4}}/\d{{2}}/[^"]*)"',
        rf'href="(/[^"]*\d{{4}}-\d{{2}}-\d{{2}}[^"]*)"',
        rf'href="(/content/[^"]+)"',
        rf'href="(/government/news/[^"]+)"',
        rf'href="(/government/speeches/[^"]+)"',
        rf'href="(/explore-our-research/[^"]+)"',
        rf'href="(/publications/[^"]+)"',
        rf'href="(/online-analysis/[^"]+)"',
    ]
    for pat in patterns:
        matches = re.findall(pat, body)
        if matches:
            url = matches[0]
            if url.startswith('/'):
                url = f"https://{domain}{url}"
            return url
    # Broader: any internal link that looks article-like
    links = re.findall(rf'href="(https?://[^"]*{re.escape(domain)}/[^"]+)"', body)
    for link in links:
        if any(seg in link for seg in ['/202', '/article/', '/commentary/', '/news/', '/publications/']):
            return link
    return None

def extract_article_url_from_rss(rss_body):
    """Extract first article URL from RSS, skipping the channel-level link"""
    # Look for <item><link> pattern - skip the first <link> which is channel link
    # Find links inside <item> blocks
    items = re.findall(r'<item>(.*?)</item>', rss_body, re.DOTALL)
    if items:
        for item in items:
            link_match = re.search(r'<link>\s*(https?://[^<\s]+)\s*</link>', item)
            if link_match:
                return link_match.group(1).strip()
            guid_match = re.search(r'<guid[^>]*>(https?://[^<]+)</guid>', item)
            if guid_match:
                return guid_match.group(1).strip()

    # Atom feeds: look for <entry> blocks
    entries = re.findall(r'<entry>(.*?)</entry>', rss_body, re.DOTALL)
    if entries:
        for entry in entries:
            link_match = re.search(r'<link[^>]*href="(https?://[^"]+)"', entry)
            if link_match:
                return link_match.group(1).strip()
            link_match = re.search(r'<link>\s*(https?://[^<\s]+)\s*</link>', entry)
            if link_match:
                return link_match.group(1).strip()

    # Fallback: find all links and skip first (channel link)
    links = re.findall(r'<link>\s*(https?://[^<\s]+)\s*</link>', rss_body)
    if len(links) > 1:
        return links[1].strip()

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
        text = re.sub(r'&#\d+;', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 60:
            text_paras.append(text[:500])
    first = text_paras[0] if text_paras else None
    last = text_paras[-1] if text_paras else None
    return first, last, len(text_paras)

def test_source(name, domain, homepage_url, rss_urls, article_hint=None):
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
    result["can_fetch_homepage"] = hp_code == 200 and len(hp_body) > 1000
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
        notes.append(f"No valid RSS at: {', '.join(rss_urls)}")

    # 3. Find article URL
    article_url = article_hint
    if not article_url and rss_body:
        article_url = extract_article_url_from_rss(rss_body)
    if not article_url and hp_body:
        article_url = extract_article_url(hp_body, domain)

    # 4. Fetch article
    if article_url:
        result["test_article_url"] = article_url
        art_code, art_body = fetch(article_url)
        result["can_fetch_article"] = art_code == 200 and len(art_body) > 1000
        if result["can_fetch_article"]:
            first, last, para_count = extract_paragraphs(art_body)
            result["first_paragraph"] = first
            result["last_paragraph"] = last
            result["can_get_full_text"] = para_count >= 3
            notes.append(f"Article: HTTP {art_code}, {len(art_body)} bytes, {para_count} paragraphs extracted")
            # Try to get date from article if not from RSS
            if not result["publication_date"]:
                date_match = re.search(r'<time[^>]*datetime="([^"]+)"', art_body)
                if date_match:
                    result["publication_date"] = date_match.group(1)
                else:
                    date_match = re.search(r'"datePublished"\s*:\s*"([^"]+)"', art_body)
                    if date_match:
                        result["publication_date"] = date_match.group(1)
        else:
            notes.append(f"Article: HTTP {art_code}, {len(art_body)} bytes - insufficient content")
    else:
        notes.append("Could not find article URL from homepage or RSS")

    result["notes"] = "; ".join(notes)
    return result


# ====== UNITED KINGDOM ======
uk_sources = [
    ("BBC News", "bbc.co.uk", "https://www.bbc.co.uk/news", [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://feeds.bbci.co.uk/news/world/rss.xml",
    ]),
    ("Financial Times", "ft.com", "https://www.ft.com", [
        "https://www.ft.com/rss/home",
        "https://www.ft.com/rss/home/uk",
    ]),
    ("The Guardian", "theguardian.com", "https://www.theguardian.com", [
        "https://www.theguardian.com/world/rss",
        "https://www.theguardian.com/uk/rss",
    ], "https://www.theguardian.com/world/2026/mar/17/donald-trump-can-take-cuba-oil"),
    ("The Times / The Sunday Times", "thetimes.co.uk", "https://www.thetimes.co.uk", [
        "https://www.thetimes.co.uk/rss",
        "https://www.thetimes.com/rss",
        "https://www.thetimes.co.uk/feed",
        "https://www.thetimes.co.uk/rss.xml",
    ]),
    ("The Telegraph", "telegraph.co.uk", "https://www.telegraph.co.uk", [
        "https://www.telegraph.co.uk/rss.xml",
        "https://www.telegraph.co.uk/news/rss.xml",
        "https://www.telegraph.co.uk/rss",
    ], "https://www.telegraph.co.uk/business/2026/03/15/markets-live-oil-price-kharg-island-iran-war-ftse-100/"),
    ("The Economist", "economist.com", "https://www.economist.com", [
        "https://www.economist.com/rss",
        "https://www.economist.com/feeds/print-sections/all/all.xml",
        "https://www.economist.com/international/rss.xml",
    ]),
    ("RUSI", "rusi.org", "https://rusi.org", [
        "https://rusi.org/rss/latest-commentary.xml",
        "https://rusi.org/rss/latest-publications.xml",
        "https://rusi.org/rss/whats-new.xml",
    ]),
    ("Chatham House", "chathamhouse.org", "https://www.chathamhouse.org", [
        "https://www.chathamhouse.org/rss.xml",
        "https://www.chathamhouse.org/feed",
        "https://www.chathamhouse.org/rss",
    ], "https://www.chathamhouse.org/publications/the-world-today/2026-03/how-irans-forward-defence-became-strategic-boomerang"),
    ("IISS", "iiss.org", "https://www.iiss.org", [
        "https://www.iiss.org/rss",
        "https://www.iiss.org/feed",
        "https://www.iiss.org/rss.xml",
    ], "https://www.iiss.org/online-analysis/online-analysis/2026/03/ukraine-conflict-latest"),
    ("GOV.UK", "gov.uk", "https://www.gov.uk", [
        "https://www.gov.uk/search/news-and-communications.atom",
        "https://www.gov.uk/government/news.atom",
        "https://www.gov.uk/feed",
    ], "https://www.gov.uk/government/news/joint-statement-on-the-escalating-conflict-between-israel-and-hezbollah-16-march-2026"),
    ("Politico Europe", "politico.eu", "https://www.politico.eu", [
        "https://www.politico.eu/feed/",
        "https://www.politico.eu/rss",
    ]),
    ("Janes", "janes.com", "https://www.janes.com", [
        "https://www.janes.com/feed",
        "https://www.janes.com/rss",
        "https://www.janes.com/rss.xml",
        "https://www.janes.com/osint-insights/defence-news",
    ]),
    ("UK Defence Journal", "ukdefencejournal.org.uk", "https://ukdefencejournal.org.uk", [
        "https://ukdefencejournal.org.uk/feed/",
    ], "https://ukdefencejournal.org.uk/uk-workshare-unclear-in-nato-air-defence-project/"),
    ("The Spectator", "spectator.co.uk", "https://www.spectator.co.uk", [
        "https://www.spectator.co.uk/feed/",
        "https://spectator.com/feed/",
        "https://www.spectator.co.uk/rss",
    ], "https://spectator.com/article/25-years-neocons-trump-scott-mcconnell-diary/"),
    ("The New Statesman", "newstatesman.com", "https://www.newstatesman.com", [
        "https://www.newstatesman.com/feed",
        "https://www.newstatesman.com/feed/",
    ], "https://www.newstatesman.com/ideas/2026/03/what-jurgen-habermas-leaves-behind"),
    ("Hansard / Parliamentary Committees", "hansard.parliament.uk", "https://hansard.parliament.uk", [
        "https://hansard.parliament.uk/rss",
        "https://hansard.parliament.uk/feed",
        "https://committees.parliament.uk/rss",
        "https://hansard.parliament.uk/search/Debates?house=commons&date=latest",
    ], "https://hansard.parliament.uk/commons/2026-03-13"),
    ("Reuters", "reuters.com", "https://www.reuters.com", [
        "https://www.reuters.com/arc/outboundfeeds/v3/all/rss.xml",
        "https://www.reuters.com/rssFeed/worldNews",
        "https://www.reuters.com/tools/rss",
    ], "https://www.reuters.com/world/uk/uk-foreign-minister-to-meet-us-secretary-state-rubio-2026-03-15/"),
    ("Declassified UK", "declassifieduk.org", "https://www.declassifieduk.org", [
        "https://www.declassifieduk.org/feed/",
    ], "https://www.declassifieduk.org/uk-military-refuses-to-give-running-commentary-on-iran-civilian-deaths/"),
]


def run_tests(sources, output_path, country_name):
    results = []
    for i, src in enumerate(sources):
        name, domain, homepage, rss_urls = src[0], src[1], src[2], src[3]
        article_hint = src[4] if len(src) > 4 else None
        print(f"  [{i+1}/{len(sources)}] Testing {name}...", file=sys.stderr)
        result = test_source(name, domain, homepage, rss_urls, article_hint)
        results.append(result)
        # Print summary
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
    print("UNITED KINGDOM SOURCE ACCESSIBILITY TESTS", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    uk_results = run_tests(
        uk_sources,
        "/Users/zen/dev/src/pdb/docs/source_intelligence_maps/tests/united_kingdom_accessibility.json",
        "United Kingdom"
    )

    # Final summary
    print("\n\n=== SUMMARY ===")
    hp_ok = sum(1 for r in uk_results if r["can_fetch_homepage"])
    art_ok = sum(1 for r in uk_results if r["can_fetch_article"])
    ft_ok = sum(1 for r in uk_results if r["can_get_full_text"])
    rss_ok = sum(1 for r in uk_results if r["has_rss"])
    rss_ft = sum(1 for r in uk_results if r["rss_has_full_text"])
    print(f"\nUNITED KINGDOM ({len(uk_results)} sources):")
    print(f"  Homepage fetchable:    {hp_ok}/{len(uk_results)}")
    print(f"  Article fetchable:     {art_ok}/{len(uk_results)}")
    print(f"  Full text extractable: {ft_ok}/{len(uk_results)}")
    print(f"  Has RSS:               {rss_ok}/{len(uk_results)}")
    print(f"  RSS has full text:     {rss_ft}/{len(uk_results)}")
