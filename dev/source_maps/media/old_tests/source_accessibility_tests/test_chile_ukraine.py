#!/usr/bin/env python3
"""Test accessibility of Chile and Ukraine news sources for OSINT pipeline."""
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
            capture_output=True, text=True, timeout=max_time+10
        )
        r2 = subprocess.run(
            ["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", str(max_time), "-A", UA, url],
            capture_output=True, text=True, timeout=max_time+10
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
    return True, has_full, body[:5000]

def extract_article_url(body, domain):
    """Try to find an article URL from homepage HTML"""
    patterns = [
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*\d{{4}}[^"]*\.s?html?)"',
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*\d{{4}}/\d{{2}}[^"]*)"',
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*articulos/[^"]*)"',
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*noticias/[^"]*)"',
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*news/[^"]*)"',
        rf'href="(https?://[^"]*{re.escape(domain)}[^"]*texto-diario/[^"]*)"',
        rf'href="(/[^"]*\d{{4}}/\d{{2}}/[^"]*\.s?html?)"',
        rf'href="(/[^"]*\d{{4}}-\d{{2}}-\d{{2}}[^"]*)"',
        rf'href="(/[^"]*\d{{4}}/\d{{2}}/\d{{2}}[^"]*)"',
        rf'href="(/[^"]*articulos/[^"]*)"',
        rf'href="(/[^"]*texto-diario/[^"]*)"',
    ]
    for pat in patterns:
        matches = re.findall(pat, body)
        if matches:
            url = matches[0]
            if url.startswith('/'):
                url = f"https://{domain}{url}"
            # skip CSS/JS/image files
            if any(x in url for x in ['.css', '.js', '.png', '.jpg', '.ico', '.svg']):
                continue
            return url
    # Broader: any internal link that looks article-like
    links = re.findall(rf'href="(https?://[^"]*{re.escape(domain)}/[^"]+)"', body)
    for link in links:
        if any(seg in link for seg in ['/202', '/noticias/', '/news/', '/articulos/', '/publications/', '/commentary/']):
            if not any(x in link for x in ['.css', '.js', '.png', '.jpg', '.ico', '.svg']):
                return link
    return None

def extract_article_url_from_rss(rss_body):
    """Extract first article URL from RSS"""
    links = re.findall(r'<link>(https?://[^<]+)</link>', rss_body)
    if len(links) > 1:
        return links[1]
    guids = re.findall(r'<guid[^>]*>(https?://[^<]+)</guid>', rss_body)
    if guids:
        return guids[0]
    links_atom = re.findall(r'<link[^>]*href="(https?://[^"]+)"[^>]*/>', rss_body)
    if len(links_atom) > 1:
        return links_atom[1]
    return links[0] if links else None

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
    result["can_fetch_homepage"] = hp_code == 200 and len(hp_body) > 500
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
    article_url = None
    if rss_body:
        article_url = extract_article_url_from_rss(rss_body)
    if not article_url and hp_body:
        article_url = extract_article_url(hp_body, domain)
    # Try section pages if still no article
    if not article_url:
        for section in ['/noticias/', '/news/', '/eng/', '/en/', '/noticias/pais/', '/publicaciones/', '/sala-de-prensa/', '/lo-ultimo/']:
            sec_code, sec_body = fetch(f"https://{domain}{section}", max_time=10)
            if sec_code == 200 and sec_body:
                article_url = extract_article_url(sec_body, domain)
                if article_url:
                    break

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
            notes.append(f"Article: HTTP {art_code}, {len(art_body)} bytes, {para_count} paragraphs")
            # extract date from URL or content if not from RSS
            if not result["publication_date"]:
                date_match = re.search(r'20\d{2}[-/]\d{2}[-/]\d{2}', article_url)
                if date_match:
                    result["publication_date"] = date_match.group().replace('/', '-')
        else:
            notes.append(f"Article: HTTP {art_code}, {len(art_body)} bytes - insufficient content")
    else:
        notes.append("Could not find article URL from homepage, RSS, or section pages")

    result["notes"] = "; ".join(notes)
    return result


# ====== CHILE ======
chile_sources = [
    ("La Tercera", "latercera.com", "https://www.latercera.com", [
        "https://www.latercera.com/feed/",
        "https://www.latercera.com/rss/",
        "https://www.latercera.com/rss",
        "https://www.latercera.com/feed",
    ]),
    ("El Mercurio / EMOL", "emol.com", "https://www.emol.com", [
        "https://www.emol.com/rss/",
        "https://www.emol.com/rss.xml",
        "https://www.emol.com/feed/",
        "https://rss.emol.com/",
    ]),
    ("Ex-Ante", "ex-ante.cl", "https://www.ex-ante.cl", [
        "https://www.ex-ante.cl/feed/",
        "https://www.ex-ante.cl/rss/",
        "https://www.ex-ante.cl/rss.xml",
        "https://ex-ante.cl/feed/",
    ]),
    ("El Mostrador", "elmostrador.cl", "https://www.elmostrador.cl", [
        "https://www.elmostrador.cl/feed/",
        "https://www.elmostrador.cl/rss/",
        "https://www.elmostrador.cl/rss.xml",
    ]),
    ("CIPER Chile", "ciperchile.cl", "https://www.ciperchile.cl", [
        "https://www.ciperchile.cl/feed/",
        "https://www.ciperchile.cl/rss/",
        "https://www.ciperchile.cl/rss.xml",
    ]),
    ("Interferencia", "interferencia.cl", "https://interferencia.cl", [
        "https://interferencia.cl/rss.xml",
        "https://interferencia.cl/feed/",
        "https://interferencia.cl/rss/",
    ]),
    ("Diario Financiero", "df.cl", "https://www.df.cl", [
        "https://www.df.cl/feed/",
        "https://www.df.cl/rss/",
        "https://www.df.cl/rss.xml",
    ]),
    ("Radio Cooperativa", "cooperativa.cl", "https://www.cooperativa.cl", [
        "https://www.cooperativa.cl/rss/",
        "https://www.cooperativa.cl/feed/",
        "https://www.cooperativa.cl/rss.xml",
        "https://cooperativa.cl/noticias/site/tax/port/all/rss_1.xml",
    ]),
    ("BioBioChile", "biobiochile.cl", "https://www.biobiochile.cl", [
        "https://www.biobiochile.cl/feed/",
        "https://www.biobiochile.cl/rss/",
        "https://www.biobiochile.cl/feed/rss.xml",
    ]),
    ("Pauta", "pauta.cl", "https://www.pauta.cl", [
        "https://www.pauta.cl/feed/",
        "https://www.pauta.cl/rss/",
        "https://www.pauta.cl/rss.xml",
    ]),
    ("T13", "t13.cl", "https://www.t13.cl", [
        "https://www.t13.cl/rss",
        "https://www.t13.cl/feed/",
        "https://www.t13.cl/rss.xml",
    ]),
    ("Infodefensa Chile", "infodefensa.com", "https://www.infodefensa.com", [
        "https://www.infodefensa.com/rss/",
        "https://www.infodefensa.com/feed/",
        "https://www.infodefensa.com/rss.xml",
    ]),
    ("Cancilleria de Chile", "minrel.gob.cl", "https://www.minrel.gob.cl", [
        "https://www.minrel.gob.cl/rss/",
        "https://www.minrel.gob.cl/feed/",
        "https://www.minrel.gob.cl/rss.xml",
    ]),
    ("SUBREI", "subrei.gob.cl", "https://www.subrei.gob.cl", [
        "https://www.subrei.gob.cl/rss/",
        "https://www.subrei.gob.cl/feed/",
        "https://www.subrei.gob.cl/rss.xml",
    ]),
    ("AthenaLab", "athenalab.org", "https://www.athenalab.org", [
        "https://www.athenalab.org/feed/",
        "https://www.athenalab.org/rss/",
        "https://www.athenalab.org/rss.xml",
    ]),
    ("Americas Quarterly", "americasquarterly.org", "https://www.americasquarterly.org", [
        "https://www.americasquarterly.org/feed/",
        "https://www.americasquarterly.org/rss/",
    ]),
    ("BNamericas", "bnamericas.com", "https://www.bnamericas.com", [
        "https://www.bnamericas.com/rss/",
        "https://www.bnamericas.com/feed/",
        "https://www.bnamericas.com/rss.xml",
    ]),
    ("Reuters", "reuters.com", "https://www.reuters.com", [
        "https://www.reuters.com/rss/",
        "https://www.reuters.com/feed/",
        "https://www.reuters.com/rss.xml",
    ]),
]

# ====== UKRAINE ======
ukraine_sources = [
    ("Ukrainska Pravda", "pravda.com.ua", "https://www.pravda.com.ua", [
        "https://www.pravda.com.ua/rss/",
        "https://www.pravda.com.ua/rss/view_news/",
        "https://www.pravda.com.ua/eng/rss/",
        "https://www.pravda.com.ua/eng/rss/view_news/",
    ]),
    ("Ekonomichna Pravda", "epravda.com.ua", "https://www.epravda.com.ua", [
        "https://www.epravda.com.ua/rss/",
        "https://www.epravda.com.ua/rss/view_news/",
    ]),
    ("Yevropeiska Pravda", "eurointegration.com.ua", "https://www.eurointegration.com.ua", [
        "https://www.eurointegration.com.ua/rss/",
        "https://www.eurointegration.com.ua/rss/view_news/",
        "https://www.eurointegration.com.ua/eng/rss/",
    ]),
    ("Kyiv Independent", "kyivindependent.com", "https://kyivindependent.com", [
        "https://kyivindependent.com/feed/",
        "https://kyivindependent.com/rss/",
        "https://kyivindependent.com/rss.xml",
    ]),
    ("Dzerkalo Tyzhnia / ZN.UA", "zn.ua", "https://zn.ua", [
        "https://zn.ua/rss/",
        "https://zn.ua/feed/",
        "https://zn.ua/rss.xml",
    ]),
    ("Ukrinform", "ukrinform.net", "https://www.ukrinform.net", [
        "https://www.ukrinform.net/rss/",
        "https://www.ukrinform.net/rss/block-lastnews",
        "https://www.ukrinform.net/feed/",
        "https://www.ukrinform.net/rss.xml",
    ]),
    ("Interfax-Ukraine", "en.interfax.com.ua", "https://en.interfax.com.ua", [
        "https://en.interfax.com.ua/rss/",
        "https://en.interfax.com.ua/rss.xml",
        "https://en.interfax.com.ua/feed/",
        "https://interfax.com.ua/rss/",
    ]),
    ("NV / New Voice of Ukraine", "nv.ua", "https://nv.ua", [
        "https://nv.ua/rss/",
        "https://nv.ua/rss.xml",
        "https://nv.ua/feed/",
        "https://english.nv.ua/rss/",
    ]),
    ("Liga.net", "liga.net", "https://www.liga.net", [
        "https://www.liga.net/rss/",
        "https://www.liga.net/feed/",
        "https://www.liga.net/rss.xml",
    ]),
    ("Defense Express", "defence-ua.com", "https://en.defence-ua.com", [
        "https://en.defence-ua.com/rss/",
        "https://en.defence-ua.com/feed/",
        "https://en.defence-ua.com/rss.xml",
        "https://defence-ua.com/rss/",
    ]),
    ("Militarnyi", "militarnyi.com", "https://militarnyi.com/en/", [
        "https://militarnyi.com/feed/",
        "https://militarnyi.com/en/feed/",
        "https://militarnyi.com/rss/",
        "https://militarnyi.com/rss.xml",
    ]),
    ("UNIAN", "unian.ua", "https://www.unian.ua", [
        "https://www.unian.ua/rss/",
        "https://www.unian.info/rss/",
        "https://www.unian.ua/rss.xml",
        "https://rss.unian.net/site/news_ukr.rss",
    ]),
    ("President of Ukraine", "president.gov.ua", "https://www.president.gov.ua/en", [
        "https://www.president.gov.ua/en/rss/",
        "https://www.president.gov.ua/rss/",
        "https://www.president.gov.ua/en/feed/",
    ]),
    ("MFA Ukraine", "mfa.gov.ua", "https://mfa.gov.ua/en", [
        "https://mfa.gov.ua/en/rss/",
        "https://mfa.gov.ua/rss/",
        "https://mfa.gov.ua/en/feed/",
    ]),
    ("Verkhovna Rada", "rada.gov.ua", "https://www.rada.gov.ua/en", [
        "https://www.rada.gov.ua/rss/",
        "https://www.rada.gov.ua/feed/",
        "https://www.rada.gov.ua/rss.xml",
    ]),
    ("Razumkov Centre", "razumkov.org.ua", "https://razumkov.org.ua/en/", [
        "https://razumkov.org.ua/feed/",
        "https://razumkov.org.ua/rss/",
        "https://razumkov.org.ua/rss.xml",
    ]),
    ("Centre for Economic Strategy", "ces.org.ua", "https://ces.org.ua/en/", [
        "https://ces.org.ua/feed/",
        "https://ces.org.ua/en/feed/",
        "https://ces.org.ua/rss/",
    ]),
    ("Texty.org.ua", "texty.org.ua", "https://texty.org.ua", [
        "https://texty.org.ua/rss/",
        "https://texty.org.ua/feed/",
        "https://texty.org.ua/rss.xml",
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
    base = "/Users/zen/dev/src/pdb/docs/source_intelligence_maps/tests"

    print("=" * 60, file=sys.stderr)
    print("CHILE SOURCE ACCESSIBILITY TESTS", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    chile_results = run_tests(chile_sources, f"{base}/chile_accessibility.json", "Chile")

    print("\n" + "=" * 60, file=sys.stderr)
    print("UKRAINE SOURCE ACCESSIBILITY TESTS", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    ukraine_results = run_tests(ukraine_sources, f"{base}/ukraine_accessibility.json", "Ukraine")

    # Final summary
    print("\n\n=== SUMMARY ===")
    for country, results in [("CHILE", chile_results), ("UKRAINE", ukraine_results)]:
        hp_ok = sum(1 for r in results if r["can_fetch_homepage"])
        art_ok = sum(1 for r in results if r["can_fetch_article"])
        ft_ok = sum(1 for r in results if r["can_get_full_text"])
        rss_ok = sum(1 for r in results if r["has_rss"])
        rss_ft = sum(1 for r in results if r["rss_has_full_text"])
        print(f"\n{country} ({len(results)} sources):")
        print(f"  Homepage fetchable:    {hp_ok}/{len(results)}")
        print(f"  Article fetchable:     {art_ok}/{len(results)}")
        print(f"  Full text extractable: {ft_ok}/{len(results)}")
        print(f"  Has RSS:               {rss_ok}/{len(results)}")
        print(f"  RSS has full text:     {rss_ft}/{len(results)}")
