#!/usr/bin/env python3
"""Test accessibility of Mexico news sources for OSINT pipeline."""
import subprocess
import json
import re
import sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def fetch(url, max_time=20):
    """Fetch URL content, return (status_code, body)"""
    try:
        # Use binary mode to avoid encoding issues, then decode with error handling
        r = subprocess.run(
            ["curl", "-sL", "--max-time", str(max_time), "-A", UA, "-w", "\n__HTTP_CODE__%{http_code}", url],
            capture_output=True, timeout=max_time + 30
        )
        output = r.stdout.decode("utf-8", errors="replace")
        code = 0
        body = output
        if "\n__HTTP_CODE__" in output:
            parts = output.rsplit("\n__HTTP_CODE__", 1)
            body = parts[0]
            try:
                code = int(parts[1].strip())
            except:
                code = 0
        elif output.strip().isdigit():
            code = int(output.strip())
            body = ""
        return code, body
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
    has_items = '<item' in body.lower() or '<entry' in body.lower()
    if not has_items:
        return False, False, None
    descs = re.findall(r'<description[^>]*>(.*?)</description>', body, re.DOTALL)
    contents = re.findall(r'<content:encoded[^>]*>(.*?)</content:encoded>', body, re.DOTALL)
    if contents:
        has_full = any(len(c) > 500 for c in contents)
    elif descs:
        has_full = any(len(d) > 500 for d in descs)
    else:
        has_full = False
    return True, has_full, body[:10000]

def extract_article_url(body, domain):
    """Try to find an article URL from homepage HTML"""
    patterns = [
        # Full URLs with date patterns
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*\d{{4}}[^"]*\.html?)"',
        rf'href="(https?://[^"]*{re.escape(domain)}/[a-z]+/[a-z]+-[a-z]+-[^"]+)"',
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*\d{{4}}/\d{{2}}[^"]*)"',
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*news/[^"]*)"',
        rf'href="(https?://[^"]*{re.escape(domain)}/noticia/[^"]*)"',
        # Relative URLs with date patterns
        rf'href="(/[^"]*\d{{4}}/\d{{2}}/[^"]*)"',
        rf'href="(/[^"]*\d{{4}}-\d{{2}}-\d{{2}}[^"]*)"',
        # Relative URLs with .html (common for El Economista etc)
        rf'href="(/[a-z]+/[a-z]+-[^"]*\.html?)"',
        # Relative URLs with /DDMM/ pattern (Aristegui uses /1603/mexico/...)
        rf'href="(/\d{{4}}/[a-z]+/[^"]*)"',
    ]
    skip_re = re.compile(r'\.(css|js|png|jpg|jpeg|svg|gif|ico|woff|ttf|eot|xml|json)|/category/|/tags?/|/autor/|/author/|/page/\d|wp-content|wp-json|/seccion|/buscar|/search|/comments/|/xmlrpc|suscri|newsletter|impreso|/mercados/indices|/mercados/divisas')
    for pat in patterns:
        matches = re.findall(pat, body)
        for url in matches:
            if skip_re.search(url):
                continue
            if url.startswith('/'):
                url = f"https://{domain}{url}"
            return url
    # Broader: any link with slug-like path (full URLs)
    links = re.findall(rf'href="(https?://[^"]*{re.escape(domain)}/[^"]+)"', body)
    for link in links:
        if skip_re.search(link):
            continue
        if re.search(r'/[a-z]+-[a-z]+-[a-z]+-[a-z]+', link) and len(link) > 50:
            return link
    # Broader: relative URLs with slug-like paths
    rel_links = re.findall(r'href="(/[a-z]+/[a-z]+-[a-z]+-[^"]+)"', body)
    for link in rel_links:
        if skip_re.search(link):
            continue
        if len(link) > 20:
            return f"https://{domain}{link}"
    return None

def extract_article_url_from_rss(rss_body):
    """Extract first article URL from RSS"""
    # Prefer guid elements which are usually the actual article URLs
    guids = re.findall(r'<guid[^>]*>(https?://[^<]+)</guid>', rss_body)
    for g in guids:
        g = g.strip()
        # Skip URLs that look like homepages
        if not re.search(r'\.com/?$|\.mx/?$|\.org/?$|\.us/?$', g) and len(g) > 30:
            return g
    # Try link elements within items
    links = re.findall(r'<link>(https?://[^<]+)</link>', rss_body)
    for link in links[1:]:  # skip first which is usually channel link
        link = link.strip()
        if not re.search(r'\.com/?$|\.mx/?$|\.org/?$|\.us/?$', link) and len(link) > 30:
            return link
    # Atom feeds
    links_atom = re.findall(r'<link[^>]*href="(https?://[^"]+)"[^>]*/>', rss_body)
    for link in links_atom[1:]:
        link = link.strip()
        if not re.search(r'\.com/?$|\.mx/?$|\.org/?$|\.us/?$', link) and len(link) > 30:
            return link
    return guids[0] if guids else (links[0] if links else None)

def extract_date(body):
    """Extract publication date from article HTML or RSS"""
    for pat in [
        r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})',
        r'published_time"\s+content="(\d{4}-\d{2}-\d{2})',
        r'datetime="(\d{4}-\d{2}-\d{2})',
        r'<pubDate>([^<]+)</pubDate>',
        r'(\d{4}-\d{2}-\d{2})T\d{2}:\d{2}',
    ]:
        m = re.search(pat, body)
        if m:
            return m.group(1).strip()
    return None

def extract_paragraphs(body):
    """Extract first and last meaningful paragraphs from article HTML"""
    clean = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<nav[^>]*>.*?</nav>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<header[^>]*>.*?</header>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<footer[^>]*>.*?</footer>', '', clean, flags=re.DOTALL)
    paras = re.findall(r'<p[^>]*>(.*?)</p>', clean, re.DOTALL)
    text_paras = []
    for p in paras:
        text = re.sub(r'<[^>]+>', '', p).strip()
        text = re.sub(r'&[a-zA-Z]+;', ' ', text)
        text = re.sub(r'&#\d+;', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 60:
            text_paras.append(text[:500])
    first = text_paras[0] if text_paras else None
    last = text_paras[-1] if text_paras else None
    return first, last, len(text_paras)


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
    result["can_fetch_homepage"] = hp_code == 200 and len(hp_body) > 1000
    notes.append(f"Homepage: HTTP {hp_code}, {len(hp_body)} bytes")

    if 'challenge-platform' in hp_body or 'cf-browser-verification' in hp_body:
        notes.append("Cloudflare challenge detected")

    # 2. Test RSS feeds
    rss_body = None
    for rss_url in rss_urls:
        has_rss, has_full, rss_content = check_rss(rss_url)
        if has_rss:
            result["has_rss"] = True
            result["rss_url"] = rss_url
            result["rss_has_full_text"] = has_full
            rss_body = rss_content
            pub_date = extract_date(rss_content)
            if pub_date:
                result["publication_date"] = pub_date
            notes.append(f"RSS found at {rss_url}, full_text={has_full}")
            break
    else:
        notes.append(f"No valid RSS at tested paths")

    # 3. Find article URL (prefer RSS, fall back to homepage)
    article_url = None
    if rss_body:
        article_url = extract_article_url_from_rss(rss_body)
        if article_url:
            notes.append(f"Article URL from RSS")
    if not article_url and hp_body:
        article_url = extract_article_url(hp_body, domain)
        if article_url:
            notes.append(f"Article URL from homepage HTML")

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
            if not result["publication_date"]:
                result["publication_date"] = extract_date(art_body)
            notes.append(f"Article: HTTP {art_code}, {para_count} paragraphs")
            # Check for paywall indicators
            pw = [k for k in ["paywall", "suscri", "premium-content", "login-wall", "meter-count"] if k in art_body.lower()]
            if pw:
                notes.append(f"Paywall indicators: {', '.join(pw)}")
        else:
            notes.append(f"Article fetch failed: HTTP {art_code}, {len(art_body)} bytes")
    else:
        notes.append("Could not find article URL from homepage or RSS")

    result["notes"] = "; ".join(notes)
    return result


# Mexico source definitions
mexico_sources = [
    ("El Universal", "eluniversal.com.mx", "https://www.eluniversal.com.mx", [
        "https://www.eluniversal.com.mx/rss",
        "https://www.eluniversal.com.mx/feed",
        "https://www.eluniversal.com.mx/rss.xml",
        "https://www.eluniversal.com.mx/feed/",
        "https://www.eluniversal.com.mx/arc/outboundfeeds/rss/",
    ]),
    ("Reforma", "reforma.com", "https://www.reforma.com", [
        "https://www.reforma.com/rss",
        "https://www.reforma.com/feed",
        "https://www.reforma.com/rss.xml",
    ]),
    ("Mexico Today", "mexicotoday.com", "https://mexicotoday.com", [
        "https://mexicotoday.com/feed/",
        "https://mexicotoday.com/rss",
        "https://mexicotoday.com/feed",
    ]),
    ("La Jornada", "jornada.com.mx", "https://www.jornada.com.mx", [
        "https://www.jornada.com.mx/rss/edicion.xml",
        "https://www.jornada.com.mx/rss/",
        "https://www.jornada.com.mx/feed",
        "https://www.jornada.com.mx/rss",
    ]),
    ("Milenio", "milenio.com", "https://www.milenio.com", [
        "https://www.milenio.com/rss",
        "https://www.milenio.com/feed",
        "https://www.milenio.com/rss.xml",
        "https://www.milenio.com/feed/",
        "https://www.milenio.com/arc/outboundfeeds/rss/",
    ]),
    ("El Financiero", "elfinanciero.com.mx", "https://www.elfinanciero.com.mx", [
        "https://www.elfinanciero.com.mx/rss",
        "https://www.elfinanciero.com.mx/feed",
        "https://www.elfinanciero.com.mx/arc/outboundfeeds/rss/",
        "https://elfinanciero.com.mx/rss",
    ]),
    ("El Economista", "eleconomista.com.mx", "https://www.eleconomista.com.mx", [
        "https://www.eleconomista.com.mx/rss",
        "https://www.eleconomista.com.mx/feed",
        "https://www.eleconomista.com.mx/rss.xml",
    ]),
    ("Animal Politico", "animalpolitico.com", "https://animalpolitico.com", [
        "https://animalpolitico.com/feed",
        "https://animalpolitico.com/feed/",
        "https://animalpolitico.com/rss",
        "https://www.animalpolitico.com/feed/",
    ]),
    ("Proceso", "proceso.com.mx", "https://www.proceso.com.mx", [
        "https://www.proceso.com.mx/rss",
        "https://www.proceso.com.mx/feed",
        "https://www.proceso.com.mx/feed/",
        "https://www.proceso.com.mx/rss.xml",
    ]),
    ("Aristegui Noticias", "aristeguinoticias.com", "https://aristeguinoticias.com", [
        "https://aristeguinoticias.com/feed",
        "https://aristeguinoticias.com/feed/",
        "https://aristeguinoticias.com/rss",
    ]),
    ("Latinus", "latinus.us", "https://latinus.us", [
        "https://latinus.us/rss",
        "https://latinus.us/feed",
        "https://latinus.us/feed/",
        "https://latinus.us/rss.xml",
    ]),
    ("Excelsior", "excelsior.com.mx", "https://www.excelsior.com.mx", [
        "https://www.excelsior.com.mx/rss.xml",
        "https://www.excelsior.com.mx/rss",
        "https://excelsior.com.mx/rss",
        "https://excelsior.com.mx/rss.xml",
    ]),
    ("InSight Crime", "insightcrime.org", "https://insightcrime.org", [
        "https://insightcrime.org/feed/",
        "https://insightcrime.org/feed",
        "https://insightcrime.org/rss",
    ]),
    ("Semanario Zeta", "zetatijuana.com", "https://zetatijuana.com", [
        "https://zetatijuana.com/feed/",
        "https://zetatijuana.com/feed",
        "https://zetatijuana.com/rss",
    ]),
    ("Pie de Pagina", "piedepagina.mx", "https://piedepagina.mx", [
        "https://piedepagina.mx/feed/",
        "https://piedepagina.mx/feed",
        "https://piedepagina.mx/rss",
    ]),
    ("Nexos", "nexos.com.mx", "https://www.nexos.com.mx", [
        "https://www.nexos.com.mx/feed/",
        "https://www.nexos.com.mx/feed",
        "https://www.nexos.com.mx/rss",
    ]),
    ("El Pais Mexico", "elpais.com", "https://elpais.com/mexico/", [
        "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/mexico/portada",
        "https://elpais.com/mexico/rss",
        "https://elpais.com/rss/mexico/",
    ]),
    ("Mexico News Daily", "mexiconewsdaily.com", "https://mexiconewsdaily.com", [
        "https://mexiconewsdaily.com/feed/",
        "https://mexiconewsdaily.com/feed",
        "https://mexiconewsdaily.com/rss",
    ]),
    ("Quinto Elemento Lab", "quintoelab.org", "https://quintoelab.org", [
        "https://quintoelab.org/feed/",
        "https://quintoelab.org/feed",
        "https://quintoelab.org/rss",
    ]),
]


def main():
    results = []
    total = len(mexico_sources)
    for i, (name, domain, homepage, rss_urls) in enumerate(mexico_sources):
        print(f"  [{i+1}/{total}] Testing {name}...", file=sys.stderr)
        result = test_source(name, domain, homepage, rss_urls)
        results.append(result)
        hp = "OK" if result["can_fetch_homepage"] else "FAIL"
        art = "OK" if result["can_fetch_article"] else "FAIL"
        ft = "OK" if result["can_get_full_text"] else "FAIL"
        rss = "OK" if result["has_rss"] else "FAIL"
        print(f"    HP={hp} ART={art} FT={ft} RSS={rss}", file=sys.stderr)

    output_path = "/Users/zen/dev/src/pdb/docs/source_intelligence_maps/tests/mexico_accessibility.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nMexico: Wrote {len(results)} results to {output_path}", file=sys.stderr)

    # Summary
    print("\n=== MEXICO SUMMARY ===")
    hp_ok = sum(1 for r in results if r["can_fetch_homepage"])
    art_ok = sum(1 for r in results if r["can_fetch_article"])
    ft_ok = sum(1 for r in results if r["can_get_full_text"])
    rss_ok = sum(1 for r in results if r["has_rss"])
    rss_ft = sum(1 for r in results if r["rss_has_full_text"])
    print(f"  Homepage fetchable:    {hp_ok}/{total}")
    print(f"  Article fetchable:     {art_ok}/{total}")
    print(f"  Full text extractable: {ft_ok}/{total}")
    print(f"  Has RSS:               {rss_ok}/{total}")
    print(f"  RSS has full text:     {rss_ft}/{total}")
    print()
    for r in results:
        hp = "OK  " if r["can_fetch_homepage"] else "FAIL"
        art = "OK  " if r["can_fetch_article"] else "FAIL"
        ft = "OK  " if r["can_get_full_text"] else "FAIL"
        rss = "OK  " if r["has_rss"] else "FAIL"
        print(f"  {r['source_name']:25s} HP:{hp} Art:{art} FT:{ft} RSS:{rss}")


if __name__ == "__main__":
    main()
