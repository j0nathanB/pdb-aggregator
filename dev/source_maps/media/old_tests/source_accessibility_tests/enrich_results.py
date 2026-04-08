#!/usr/bin/env python3
"""Enrich Taiwan and Japan accessibility results with targeted follow-up tests."""
import subprocess
import json
import re
import sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def curl_status(url, timeout=10):
    try:
        r = subprocess.run(
            ["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", str(timeout), "-A", UA, url],
            capture_output=True, text=True, timeout=timeout+5
        )
        return int(r.stdout.strip()) if r.stdout.strip().isdigit() else 0
    except:
        return 0

def curl_get(url, timeout=15, max_bytes=100000):
    try:
        r = subprocess.run(
            ["curl", "-sL", "--max-time", str(timeout), "-A", UA, url],
            capture_output=True, text=True, timeout=timeout+5
        )
        return r.stdout[:max_bytes] if r.stdout else ""
    except:
        return ""

def extract_paragraphs(body):
    clean = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    paras = re.findall(r'<p[^>]*>(.*?)</p>', clean, re.DOTALL)
    text_paras = []
    for p in paras:
        text = re.sub(r'<[^>]+>', '', p).strip()
        text = re.sub(r'&[a-z]+;', ' ', text)
        text = re.sub(r'&#\d+;', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 40:
            text_paras.append(text[:500])
    return text_paras

def extract_date(html):
    patterns = [
        r'"datePublished"\s*:\s*"([^"]+)"',
        r'content="(\d{4}-\d{2}-\d{2}[T ][^"]*)"[^>]*property="article:published',
        r'property="article:published[^"]*"[^>]*content="([^"]+)"',
        r'datetime="(\d{4}-\d{2}-\d{2}[^"]*)"',
        r'<meta[^>]*name="pubdate"[^>]*content="([^"]+)"',
    ]
    for pat in patterns:
        m = re.search(pat, html)
        if m:
            return m.group(1)[:30]
    return None

def extract_meta_description(html):
    m = re.search(r'<meta[^>]*(?:property="og:description"|name="description")[^>]*content="([^"]+)"', html, re.IGNORECASE)
    if m:
        desc = m.group(1).strip()
        if len(desc) > 30:
            return desc[:500]
    return None

def check_rss(url):
    body = curl_get(url, timeout=10, max_bytes=10000)
    if not body:
        return False, False
    is_rss = bool(re.search(r'<rss|<feed|<channel|xmlns.*atom', body[:2000], re.IGNORECASE))
    if not is_rss:
        return False, False
    has_full = bool(re.search(r'<(content:encoded|content|description)[^>]*>.{500,}', body, re.DOTALL))
    return True, has_full

def extract_rss_article(rss_url):
    body = curl_get(rss_url, timeout=10, max_bytes=20000)
    if not body:
        return None, None
    links = re.findall(r'<link>(https?://[^<]+)</link>', body)
    if len(links) > 1:
        return links[1], body
    guids = re.findall(r'<guid[^>]*>(https?://[^<]+)</guid>', body)
    if guids:
        return guids[0], body
    links_atom = re.findall(r'<link[^>]*href="(https?://[^"]+)"', body)
    for l in links_atom:
        if '/feed' not in l and '/rss' not in l and l.count('/') > 3:
            return l, body
    return None, body

def extract_rss_date(rss_body):
    dates = re.findall(r'<pubDate>([^<]+)</pubDate>', rss_body)
    if dates:
        return dates[0].strip()
    dates = re.findall(r'<updated>([^<]+)</updated>', rss_body)
    if dates:
        return dates[0].strip()
    return None

# ===== KNOWN RSS PATHS AND ARTICLE URL PATTERNS =====

taiwan_known_rss = {
    "focustaiwan.tw": ["https://focustaiwan.tw/rss/aall"],
    "ltn.com.tw": ["https://news.ltn.com.tw/rss/all.xml", "https://news.ltn.com.tw/rss/politics.xml"],
    "taipeitimes.com": ["https://www.taipeitimes.com/xml/index.rss"],
    "udn.com": ["https://udn.com/rssfeed/news/2/6638", "https://udn.com/rssfeed/news/1/2"],
    "chinatimes.com": ["https://www.chinatimes.com/rss/realtimenews.xml", "https://www.chinatimes.com/rss/newspapers.xml"],
    "news.tvbs.com.tw": ["https://news.tvbs.com.tw/rss/realtime.xml", "https://news.tvbs.com.tw/rss"],
    "setn.com": ["https://setn.com/rss.xml"],
    "twreporter.org": ["https://www.twreporter.org/a/rss2.xml"],
    "thenewslens.com": ["https://www.thenewslens.com/rss"],
    "storm.mg": ["https://www.storm.mg/feeds/rss/all"],
    "taiwannews.com.tw": ["https://www.taiwannews.com.tw/en/rss"],
    "ketagalanmedia.com": ["https://ketagalanmedia.com/feed/"],
    "newbloommag.net": ["https://newbloommag.net/feed/"],
}

japan_known_rss = {
    "english.kyodonews.net": ["https://english.kyodonews.net/rss/all.xml"],
    "www.japantimes.co.jp": ["https://www.japantimes.co.jp/feed/"],
    "www.asahi.com/ajw": ["https://www.asahi.com/ajw/rss/index.rdf"],
    "japan-forward.com": ["https://japan-forward.com/feed/"],
    "www.nippon.com/en": ["https://www.nippon.com/en/feed/"],
    "asia.nikkei.com": ["https://asia.nikkei.com/rss"],
    "www3.nhk.or.jp/nhkworld": ["https://www3.nhk.or.jp/nhkworld/rss/top_stories.xml"],
}

taiwan_known_articles = {
    "focustaiwan.tw": "https://focustaiwan.tw/business/202603170005",
    "ltn.com.tw": "https://news.ltn.com.tw/news/politics",
    "udn.com": "https://udn.com/news/story/6656",
    "chinatimes.com": "https://www.chinatimes.com/newspapers",
    "storm.mg": "https://www.storm.mg/articles",
    "indsr.org.tw": "https://indsr.org.tw/en/respublicationcon?uid=12&resid=2704",
    "en.mofa.gov.tw": "https://en.mofa.gov.tw/theme.aspx?n=2239&s=86",
}

japan_known_articles = {
    "jen.jiji.com": "https://jen.jiji.com/jc/eng?g=eco",
    "www3.nhk.or.jp/nhkworld": "https://www3.nhk.or.jp/nhkworld/en/news/",
    "asia.nikkei.com": "https://asia.nikkei.com/Politics",
    "japan.kantei.go.jp": "https://japan.kantei.go.jp/101_ishiba/statement.html",
    "www.mofa.go.jp": "https://www.mofa.go.jp/press/release/index.html",
    "www.mod.go.jp": "https://www.mod.go.jp/en/",
    "www.jiia.or.jp/en": "https://www.jiia.or.jp/en/research-report/",
    "www.spf.org/en": "https://www.spf.org/en/global-data/",
}

output_dir = "/Users/zen/dev/src/pdb/docs/source_intelligence_maps/tests"

def enrich_results(results, known_rss, known_articles, country):
    print(f"\n=== Enriching {country} results ===", file=sys.stderr)
    for r in results:
        domain = r["domain"]
        print(f"  Enriching: {r['source_name']} ({domain})", file=sys.stderr)
        notes = [r.get("notes", "")]

        # Try known RSS if not found
        if not r["has_rss"] and domain in known_rss:
            for rss_url in known_rss[domain]:
                is_rss, has_full = check_rss(rss_url)
                if is_rss:
                    r["has_rss"] = True
                    r["rss_url"] = rss_url
                    r["rss_has_full_text"] = has_full
                    notes.append(f"RSS found at known path: {rss_url}")

                    # Try to get article from RSS
                    if not r["can_fetch_article"]:
                        art_url, rss_body = extract_rss_article(rss_url)
                        if art_url:
                            r["test_article_url"] = art_url
                            art_status = curl_status(art_url)
                            if 200 <= art_status < 400:
                                r["can_fetch_article"] = True
                                art_html = curl_get(art_url)
                                paras = extract_paragraphs(art_html)
                                if paras:
                                    r["first_paragraph"] = paras[0]
                                    r["last_paragraph"] = paras[-1]
                                    r["can_get_full_text"] = len(paras) >= 3
                                else:
                                    # Try meta description
                                    desc = extract_meta_description(art_html)
                                    if desc:
                                        r["first_paragraph"] = desc
                                        r["can_fetch_article"] = True
                                        notes.append("Full text JS-rendered; extracted meta description only")
                                date = extract_date(art_html)
                                if date:
                                    r["publication_date"] = date
                        if not r.get("publication_date") and rss_body:
                            rss_date = extract_rss_date(rss_body)
                            if rss_date:
                                r["publication_date"] = rss_date
                    break

        # Try known article URLs
        if not r["can_fetch_article"] and domain in known_articles:
            art_url = known_articles[domain]
            art_status = curl_status(art_url)
            if 200 <= art_status < 400:
                r["test_article_url"] = art_url
                r["can_fetch_article"] = True
                art_html = curl_get(art_url)
                paras = extract_paragraphs(art_html)
                if paras:
                    r["first_paragraph"] = paras[0]
                    r["last_paragraph"] = paras[-1]
                    r["can_get_full_text"] = len(paras) >= 3
                else:
                    desc = extract_meta_description(art_html)
                    if desc:
                        r["first_paragraph"] = desc
                        notes.append("Full text JS-rendered; extracted meta description only")
                date = extract_date(art_html)
                if date:
                    r["publication_date"] = date
                notes.append(f"Article found at known path: {art_url}")

        # For JS-rendered sites with article URL but no text, try meta description
        if r["test_article_url"] and not r["first_paragraph"]:
            art_html = curl_get(r["test_article_url"])
            desc = extract_meta_description(art_html)
            if desc:
                r["first_paragraph"] = desc
                r["can_fetch_article"] = True
                notes.append("Extracted meta description from JS-rendered page")

        # Fix homepage status for sites that need User-Agent
        if not r["can_fetch_homepage"]:
            url = f"https://{domain}"
            code = curl_status(url)
            if 200 <= code < 400:
                r["homepage_status_code"] = code
                r["can_fetch_homepage"] = True
                notes.append(f"Homepage accessible with browser UA (HTTP {code})")

        # Consolidate notes
        all_notes = [n for n in notes if n and n != "OK"]
        r["notes"] = "; ".join(all_notes) if all_notes else "OK"

    return results

# Load and enrich Taiwan
with open(f"{output_dir}/taiwan_accessibility.json") as f:
    taiwan = json.load(f)
taiwan = enrich_results(taiwan, taiwan_known_rss, taiwan_known_articles, "Taiwan")
with open(f"{output_dir}/taiwan_accessibility.json", "w") as f:
    json.dump(taiwan, f, indent=2, ensure_ascii=False)

# Load and enrich Japan
with open(f"{output_dir}/japan_accessibility.json") as f:
    japan = json.load(f)
japan = enrich_results(japan, japan_known_rss, japan_known_articles, "Japan")
with open(f"{output_dir}/japan_accessibility.json", "w") as f:
    json.dump(japan, f, indent=2, ensure_ascii=False)

# Summary
print("\n=== ENRICHED SUMMARY ===", file=sys.stderr)
for label, results in [("Taiwan", taiwan), ("Japan", japan)]:
    hp_ok = sum(1 for r in results if r["can_fetch_homepage"])
    art_ok = sum(1 for r in results if r["can_fetch_article"])
    ft_ok = sum(1 for r in results if r["can_get_full_text"])
    rss_ok = sum(1 for r in results if r["has_rss"])
    rss_ft = sum(1 for r in results if r["rss_has_full_text"])
    first_p = sum(1 for r in results if r["first_paragraph"])
    print(f"\n{label} ({len(results)} sources):", file=sys.stderr)
    print(f"  Homepage fetchable:    {hp_ok}/{len(results)}", file=sys.stderr)
    print(f"  Article fetchable:     {art_ok}/{len(results)}", file=sys.stderr)
    print(f"  Full text extractable: {ft_ok}/{len(results)}", file=sys.stderr)
    print(f"  Has first paragraph:   {first_p}/{len(results)}", file=sys.stderr)
    print(f"  Has RSS:               {rss_ok}/{len(results)}", file=sys.stderr)
    print(f"  RSS has full text:     {rss_ft}/{len(results)}", file=sys.stderr)

print("\nDONE")
