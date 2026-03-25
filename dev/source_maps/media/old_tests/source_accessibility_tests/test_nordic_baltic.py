#!/usr/bin/env python3
"""Test source accessibility for Sweden, Estonia, Lithuania, Latvia."""
import subprocess
import json
import re
import sys

def curl_status(url, timeout=10):
    try:
        r = subprocess.run(
            ["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", str(timeout),
             "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", url],
            capture_output=True, text=True, timeout=timeout+5
        )
        return int(r.stdout.strip()) if r.stdout.strip().isdigit() else 0
    except Exception:
        return 0

def curl_get(url, timeout=15, max_bytes=200000):
    try:
        r = subprocess.run(
            ["curl", "-sL", "--compressed", "--max-time", str(timeout),
             "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", url],
            capture_output=True, timeout=timeout+5
        )
        content = r.stdout.decode('utf-8', errors='replace')
        return content[:max_bytes] if content else ""
    except Exception:
        return ""

def extract_article_urls(html, domain):
    urls = []
    pattern = rf'href="(https?://(?:www\.)?{re.escape(domain)}[^"]*)"'
    matches = re.findall(pattern, html, re.IGNORECASE)
    for m in matches:
        path = m.split(domain, 1)[-1] if domain in m else ""
        if re.search(r'/\d{4}[-/]', path) or re.search(r'(/[a-z0-9-]+){3,}', path):
            if not any(x in m for x in ['.css', '.js', '.png', '.jpg', '.svg', '#', 'cookie', 'login', 'subscribe', '.woff']):
                urls.append(m)
    if not urls:
        rel_matches = re.findall(r'href="(/[^"]{20,})"', html)
        for m in rel_matches:
            if re.search(r'/\d{4}[-/]', m) or re.search(r'(/[a-z0-9-]+){3,}', m):
                if not any(x in m for x in ['.css', '.js', '.png', '.jpg', '.svg', '#', 'cookie', 'login', '.woff']):
                    urls.append(f"https://{domain}{m}")
    return urls[:5]

def extract_paragraphs(html):
    p_tags = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    paragraphs = []
    for p in p_tags:
        text = re.sub(r'<[^>]+>', '', p).strip()
        text = re.sub(r'\s+', ' ', text)
        if len(text) > 40:
            paragraphs.append(text)
    return paragraphs

def extract_date(html):
    patterns = [
        r'"datePublished"\s*:\s*"([^"]+)"',
        r'content="(\d{4}-\d{2}-\d{2}[T ][^"]*)"[^>]*property="article:published',
        r'property="article:published[^"]*"[^>]*content="([^"]+)"',
        r'"publishedDate"\s*:\s*"([^"]+)"',
        r'datetime="(\d{4}-\d{2}-\d{2}[^"]*)"',
        r'"datePublished":\s*"([^"]+)"',
    ]
    for pat in patterns:
        m = re.search(pat, html)
        if m:
            return m.group(1)[:25]
    return None

def test_rss(domain, extra_rss_paths=None):
    rss_paths = extra_rss_paths or []
    rss_paths = rss_paths + ["/rss", "/feed", "/rss.xml", "/feed.xml", "/atom.xml", "/feeds"]

    # Also check homepage for RSS link tags
    hp = curl_get(f"https://{domain}", timeout=10, max_bytes=50000)
    m = re.search(r'type="application/(rss|atom)\+xml"[^>]*href="([^"]*)"', hp)
    if not m:
        m = re.search(r'href="([^"]*)"[^>]*type="application/(rss|atom)\+xml"', hp)
        if m:
            rurl = m.group(1)
        else:
            rurl = None
    else:
        rurl = m.group(2)
    if rurl:
        if not rurl.startswith('http'):
            rurl = f"https://{domain}{rurl}"
        rss_paths = [rurl] + rss_paths

    for path in rss_paths:
        url = path if path.startswith('http') else f"https://{domain}{path}"
        content = curl_get(url, timeout=10, max_bytes=30000)
        if content and re.search(r'<rss|<feed|<channel|xmlns.*atom', content, re.IGNORECASE):
            if re.search(r'<item|<entry', content, re.IGNORECASE):
                has_full = bool(re.search(r'<(content:encoded|content)[^>]*>.{500,}', content, re.DOTALL))
                if not has_full:
                    descs = re.findall(r'<description[^>]*>(.+?)</description>', content, re.DOTALL)
                    has_full = any(len(d) > 500 for d in descs)
                return True, url, has_full
    return False, None, False

def test_source(name, domain, rss_paths=None, article_hint=None):
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

    # 1. Homepage
    status = curl_status(f"https://{domain}")
    result["can_fetch_homepage"] = 200 <= status < 400
    notes = []

    # 2. Find and fetch article
    if article_hint:
        article_urls = [article_hint]
    else:
        homepage_html = curl_get(f"https://{domain}")
        article_urls = extract_article_urls(homepage_html, domain)

    if article_urls:
        article_url = article_urls[0]
        result["test_article_url"] = article_url
        article_status = curl_status(article_url)
        result["can_fetch_article"] = 200 <= article_status < 400
        if result["can_fetch_article"]:
            article_html = curl_get(article_url)
            paragraphs = extract_paragraphs(article_html)
            if paragraphs:
                result["can_get_full_text"] = len(paragraphs) >= 3
                result["first_paragraph"] = paragraphs[0][:300] if paragraphs else None
                result["last_paragraph"] = paragraphs[-1][:300] if len(paragraphs) > 1 else paragraphs[0][:300]
            else:
                notes.append("No paragraphs extracted - may be JS-rendered or paywalled")
            pub_date = extract_date(article_html)
            result["publication_date"] = pub_date
    else:
        notes.append("No article links found on homepage")

    # 3. RSS
    has_rss, rss_url, rss_full = test_rss(domain, rss_paths)
    result["has_rss"] = has_rss
    result["rss_url"] = rss_url
    result["rss_has_full_text"] = rss_full
    if not has_rss:
        notes.append("No RSS feed found")

    result["notes"] = "; ".join(notes) if notes else "OK"
    return result

output_dir = "/Users/zen/dev/src/pdb/docs/source_intelligence_maps/tests"

# ========== SWEDEN ==========
print("=== SWEDEN ===", file=sys.stderr)
sweden_sources = [
    ("Sveriges Television (SVT)", "svt.se", ["/nyheter/rss.xml"], "https://www.svt.se/nyheter/utrikes/lakare-utan-granser-kravs-mer-an-att-rafah-overgangen-oppnas"),
    ("Sveriges Radio (SR)", "sverigesradio.se", ["https://api.sr.se/api/rss/program/4540"], "https://www.sverigesradio.se/artikel/forsvarsmakten-agerar-efter-dodsfall-i-lumpen"),
    ("Dagens Nyheter (DN)", "dn.se", ["/rss/"], "https://www.dn.se/varlden/vance-bryter-tystnad-om-attacken-vi-har-en-smart-president/"),
    ("Svenska Dagbladet (SvD)", "svd.se", ["/feed/articles.rss"], "https://www.svd.se/a/zOA3GO/israel-i-nya-attacker-mot-beirut"),
    ("Aftonbladet", "aftonbladet.se", ["https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/"], None),
    ("Expressen", "expressen.se", ["/rss/nyheter"], "https://www.expressen.se/nyheter/varlden/skrev-bok-om-makens--dod-doms-for-mordet/"),
    ("Dagens Industri (DI)", "di.se", ["/rss"], None),
    ("Omni", "omni.se", None, None),
    ("Goteborgs-Posten", "gp.se", ["/rss"], None),
    ("Sydsvenskan", "sydsvenskan.se", ["/rss"], None),
    ("Fokus", "fokus.se", None, None),
    ("Kvartal", "kvartal.se", None, None),
    ("Altinget Sverige", "altinget.se", ["/rss"], None),
    ("Riksdag Official", "riksdagen.se", None, None),
    ("Regeringskansliet", "government.se", None, None),
    ("FOI", "foi.se", None, None),
    ("UI", "ui.se", None, None),
]
sweden_results = []
for name, domain, rss, art in sweden_sources:
    sweden_results.append(test_source(name, domain, rss, art))
with open(f"{output_dir}/sweden_accessibility.json", "w") as f:
    json.dump(sweden_results, f, indent=2, ensure_ascii=False)
print(f"Sweden: {len(sweden_results)} sources tested", file=sys.stderr)

# ========== ESTONIA ==========
print("\n=== ESTONIA ===", file=sys.stderr)
estonia_sources = [
    ("ERR", "err.ee", ["https://news.err.ee/rss", "/rss"], None),
    ("Postimees", "postimees.ee", None, None),
    ("Eesti Paevaleht", "epl.delfi.ee", None, None),
    ("Delfi Estonia", "delfi.ee", None, None),
    ("Eesti Ekspress", "ekspress.delfi.ee", None, None),
    ("Aripaev", "aripaev.ee", None, None),
    ("Ohtuleht", "ohtuleht.ee", None, None),
    ("Diplomaatia", "diplomaatia.ee", None, None),
    ("ICDS", "icds.ee", None, None),
    ("Propastop", "propastop.org", None, None),
    ("ERR Russian Service", "rus.err.ee", None, None),
    ("Riigikogu", "riigikogu.ee", None, None),
    ("Ministry of Foreign Affairs", "vm.ee", None, None),
    ("Ministry of Defence", "kaitseministeerium.ee", None, None),
    ("BNS", "bns.ee", None, None),
    ("Maaleht", "maaleht.ee", None, None),
]
estonia_results = []
for name, domain, rss, art in estonia_sources:
    estonia_results.append(test_source(name, domain, rss, art))
with open(f"{output_dir}/estonia_accessibility.json", "w") as f:
    json.dump(estonia_results, f, indent=2, ensure_ascii=False)
print(f"Estonia: {len(estonia_results)} sources tested", file=sys.stderr)

# ========== LITHUANIA ==========
print("\n=== LITHUANIA ===", file=sys.stderr)
lithuania_sources = [
    ("LRT", "lrt.lt", ["/rss", "https://www.lrt.lt/rss"], None),
    ("Delfi.lt", "delfi.lt", None, None),
    ("15min.lt", "15min.lt", None, None),
    ("Lietuvos rytas", "lrytas.lt", None, None),
    ("Verslo zinios", "vz.lt", None, None),
    ("Siena", "siena.lt", None, None),
    ("Laisves TV", "laisves.tv", None, None),
    ("BNS Lithuania", "bns.lt", None, None),
    ("ELTA", "elta.lt", None, None),
    ("Veidas", "veidas.lt", None, None),
    ("IQ.lt", "iq.lt", None, None),
    ("Seimas", "lrs.lt", None, None),
    ("Ministry of National Defence", "kam.lt", None, None),
    ("Ministry of Foreign Affairs", "urm.lt", None, None),
    ("VSD", "vsd.lt", None, None),
    ("The Baltic Times", "baltictimes.com", None, None),
    ("EESC", "eesc.lt", None, None),
]
lithuania_results = []
for name, domain, rss, art in lithuania_sources:
    lithuania_results.append(test_source(name, domain, rss, art))
with open(f"{output_dir}/lithuania_accessibility.json", "w") as f:
    json.dump(lithuania_results, f, indent=2, ensure_ascii=False)
print(f"Lithuania: {len(lithuania_results)} sources tested", file=sys.stderr)

# ========== LATVIA ==========
print("\n=== LATVIA ===", file=sys.stderr)
latvia_sources = [
    ("LSM", "lsm.lv", ["/rss", "https://www.lsm.lv/rss/", "https://eng.lsm.lv/rss/"], None),
    ("Delfi Latvia", "delfi.lv", None, None),
    ("TVNET", "tvnet.lv", None, None),
    ("Diena", "diena.lv", None, None),
    ("NRA", "nra.lv", None, None),
    ("Latvijas Avize", "la.lv", None, None),
    ("IR", "ir.lv", None, None),
    ("Re:Baltica", "rebaltica.lv", None, None),
    ("Dienas Bizness", "db.lv", None, None),
    ("BNS Latvia", "bns.lv", None, None),
    ("Saeima", "saeima.lv", None, None),
    ("Ministry of Defence", "mod.gov.lv", None, None),
    ("Ministry of Foreign Affairs", "mfa.gov.lv", None, None),
    ("VDD", "vdd.gov.lv", None, None),
    ("Providus", "providus.lv", None, None),
    ("LIIA", "liia.lv", None, None),
    ("The Baltic Times", "baltictimes.com", None, None),
]
latvia_results = []
for name, domain, rss, art in latvia_sources:
    latvia_results.append(test_source(name, domain, rss, art))
with open(f"{output_dir}/latvia_accessibility.json", "w") as f:
    json.dump(latvia_results, f, indent=2, ensure_ascii=False)
print(f"Latvia: {len(latvia_results)} sources tested", file=sys.stderr)

# Summary
print("\n=== SUMMARY ===", file=sys.stderr)
for label, results in [("Sweden", sweden_results), ("Estonia", estonia_results), ("Lithuania", lithuania_results), ("Latvia", latvia_results)]:
    hp = sum(1 for r in results if r["can_fetch_homepage"])
    art = sum(1 for r in results if r["can_fetch_article"])
    ft = sum(1 for r in results if r["can_get_full_text"])
    rss = sum(1 for r in results if r["has_rss"])
    print(f"  {label}: {hp}/{len(results)} homepage, {art}/{len(results)} article, {ft}/{len(results)} full-text, {rss}/{len(results)} RSS", file=sys.stderr)

print("\nALL DONE")
