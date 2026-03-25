#!/usr/bin/env python3
"""Targeted fixes for India and Indonesia source tests."""
import subprocess, json, re, html as html_mod, sys

def curl_get(url, timeout=15, max_bytes=120000):
    try:
        r = subprocess.run(
            ["curl", "-sL", "--max-time", str(timeout),
             "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
             "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
             url], capture_output=True, text=True, timeout=timeout+5)
        return r.stdout[:max_bytes] if r.stdout else ""
    except:
        return ""

def curl_status(url, timeout=10):
    try:
        r = subprocess.run(
            ["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", str(timeout), url],
            capture_output=True, text=True, timeout=timeout+5)
        return int(r.stdout.strip()) if r.stdout.strip().isdigit() else 0
    except:
        return 0

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
    for pat in [r'"datePublished"\s*:\s*"([^"]+)"',
                r'content="(\d{4}-\d{2}-\d{2}[T ][^"]*)"[^>]*property="article:published',
                r'property="article:published[^"]*"[^>]*content="([^"]+)"',
                r'datetime="(\d{4}-\d{2}-\d{2}[^"]*)"',
                r'"date_published"\s*:\s*"([^"]+)"']:
        m = re.search(pat, html_content)
        if m: return m.group(1)[:25]
    return None

def test_rss(url):
    content = curl_get(url, timeout=10, max_bytes=15000)
    if content and re.search(r'<rss|<feed|<channel', content[:500], re.IGNORECASE):
        has_full = bool(re.search(r'<(content:encoded|content|description)[^>]*>.{500,}', content, re.DOTALL))
        return True, has_full, content
    return False, False, ""

def find_article_from_rss(rss_content, domain):
    links = re.findall(r'<link>([^<]+)</link>', rss_content)
    links += re.findall(r'<link[^>]*href="([^"]+)"', rss_content)
    for link in links:
        link = link.strip()
        if domain in link and link.count('/') >= 4:
            return link
    return None

output_dir = "/Users/zen/dev/src/pdb/docs/source_intelligence_maps/tests"

with open(f"{output_dir}/india_accessibility.json") as f:
    india = json.load(f)
with open(f"{output_dir}/indonesia_accessibility.json") as f:
    indo = json.load(f)

india_by_domain = {r["domain"]: r for r in india}
indo_by_domain = {r["domain"]: r for r in indo}

print("=== Fixing India sources ===", file=sys.stderr)

# Fix MEA
print("  Fixing: MEA", file=sys.stderr)
mea = india_by_domain["mea.gov.in"]
api = curl_get("https://mea.gov.in/Portal/ForeignRelation/PressRelease_new_page_ajax.aspx?flag=true&PageNo=1")
if api and len(api) > 100:
    matches = re.findall(r'href="(press-releases\.htm\?dtl/[^"]*)"', api)
    if matches:
        url = f"https://mea.gov.in/{matches[0]}"
        art = curl_get(url)
        paras = extract_paragraphs(art)
        date = extract_date(art)
        if paras:
            mea["can_fetch_article"] = True
            mea["can_get_full_text"] = len(paras) >= 3
            mea["test_article_url"] = url
            mea["first_paragraph"] = paras[0][:300]
            mea["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
            mea["publication_date"] = date
            mea["notes"] = "Homepage accessible. Press release list is AJAX-loaded (use API endpoint). Individual pages return full text. No RSS."
if not mea.get("can_fetch_article"):
    api2 = curl_get("https://mea.gov.in/Portal/ForeignRelation/SpeechesStatement_new_page_ajax.aspx?flag=true&PageNo=1")
    if api2 and len(api2) > 100:
        matches = re.findall(r'href="(Speeches-Statements\.htm\?dtl/[^"]*)"', api2)
        if matches:
            url = f"https://mea.gov.in/{matches[0]}"
            art = curl_get(url)
            paras = extract_paragraphs(art)
            date = extract_date(art)
            if paras:
                mea["can_fetch_article"] = True
                mea["can_get_full_text"] = len(paras) >= 3
                mea["test_article_url"] = url
                mea["first_paragraph"] = paras[0][:300]
                mea["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
                mea["publication_date"] = date
                mea["notes"] = "Homepage accessible. Speeches/statements list is AJAX-loaded (use API endpoint). Individual pages return full text. No RSS."

# Fix PIB
print("  Fixing: PIB", file=sys.stderr)
pib = india_by_domain["pib.gov.in"]
rss_content = curl_get("https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3", max_bytes=20000)
if rss_content:
    links = re.findall(r'<link>(https://pib\.gov\.in/[^<]*PRID=[^<]*)</link>', rss_content)
    for link in links:
        art = curl_get(link.strip())
        paras = extract_paragraphs(art)
        if paras:
            pib["can_fetch_article"] = True
            pib["can_get_full_text"] = len(paras) >= 3
            pib["test_article_url"] = link.strip()
            pib["first_paragraph"] = paras[0][:300]
            pib["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
            pib["publication_date"] = extract_date(art)
            pib["notes"] = "Homepage accessible. RSS provides release links. Individual pages accessible. RSS titles/descriptions only (no full text). Multiple language feeds available."
            break

# Fix The Hindu
print("  Fixing: The Hindu", file=sys.stderr)
hindu = india_by_domain["thehindu.com"]
rss_content = curl_get("https://www.thehindu.com/feeder/default.rss", max_bytes=30000)
art_url = find_article_from_rss(rss_content, "thehindu.com")
if art_url:
    art = curl_get(art_url)
    paras = extract_paragraphs(art)
    date = extract_date(art)
    hindu["test_article_url"] = art_url
    hindu["publication_date"] = date
    hindu["can_fetch_article"] = True
    if paras:
        hindu["can_get_full_text"] = len(paras) >= 3
        hindu["first_paragraph"] = paras[0][:300]
        hindu["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
        hindu["notes"] = "Article text extractable. Metered paywall (~10 free/month). RSS has descriptions only. India's most analytically rigorous English daily for foreign affairs."
    else:
        hindu["notes"] = "Article pages load but body JS-rendered or paywalled. RSS has descriptions only. Metered paywall."

# Fix Indian Express RSS full text
print("  Fixing: Indian Express RSS", file=sys.stderr)
ie = india_by_domain["indianexpress.com"]
rss_content = curl_get("https://indianexpress.com/feed/", max_bytes=50000)
if rss_content:
    ce_blocks = re.findall(r'<content:encoded><!\[CDATA\[(.*?)\]\]>', rss_content, re.DOTALL)
    if ce_blocks and len(ce_blocks[0]) > 200:
        ie["rss_has_full_text"] = True
        ie["notes"] = "Excellent extractability. Full article text via HTML scraping and RSS content:encoded. Best Indian source for automated extraction."

# Fix The Wire via WP API
print("  Fixing: The Wire", file=sys.stderr)
wire = india_by_domain["thewire.in"]
api = curl_get("https://thewire.in/wp-json/wp/v2/posts?per_page=3")
if api and api.strip().startswith('['):
    try:
        posts = json.loads(api)
        if posts:
            post = posts[0]
            wire["test_article_url"] = post.get("link")
            wire["publication_date"] = post.get("date", "")[:25]
            content_html = post.get("content", {}).get("rendered", "")
            if content_html:
                paras = extract_paragraphs(content_html)
                if paras:
                    wire["can_fetch_article"] = True
                    wire["can_get_full_text"] = len(paras) >= 3
                    wire["first_paragraph"] = paras[0][:300]
                    wire["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
                    wire["has_rss"] = True
                    wire["rss_url"] = "https://thewire.in/wp-json/wp/v2/posts"
                    wire["rss_has_full_text"] = True
                    wire["notes"] = "Homepage is React SPA (JS-rendered). Standard /feed returns HTML. WordPress REST API (/wp-json/wp/v2/posts) returns full article content in JSON. Viable extraction path."
    except json.JSONDecodeError:
        pass

# Fix ET
print("  Fixing: Economic Times", file=sys.stderr)
et = india_by_domain["economictimes.indiatimes.com"]
rss_content = curl_get("https://economictimes.indiatimes.com/rssfeedstopstories.cms", max_bytes=20000)
art_url = find_article_from_rss(rss_content, "economictimes.indiatimes.com")
if art_url:
    art = curl_get(art_url)
    paras = extract_paragraphs(art)
    date = extract_date(art)
    if paras:
        et["test_article_url"] = art_url
        et["first_paragraph"] = paras[0][:300]
        et["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
        et["publication_date"] = date
        et["can_get_full_text"] = len(paras) >= 3
        et["notes"] = "Article text extractable. RSS with titles/descriptions. Metered paywall. Primary business/economic source."

# Fix LiveMint
print("  Fixing: LiveMint", file=sys.stderr)
mint = india_by_domain["livemint.com"]
rss_content = curl_get("https://www.livemint.com/rss/news", max_bytes=20000)
links = re.findall(r'<link><!\[CDATA\[(https://www\.livemint\.com/[^]]+)\]\]></link>', rss_content)
if not links:
    links = re.findall(r'<link>(https://www\.livemint\.com/[^<]+\.html)</link>', rss_content)
if links:
    art = curl_get(links[0])
    paras = extract_paragraphs(art)
    date = extract_date(art)
    if paras:
        mint["test_article_url"] = links[0]
        mint["first_paragraph"] = paras[0][:300]
        mint["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
        mint["publication_date"] = date
        mint["can_get_full_text"] = len(paras) >= 3
    mint["notes"] = f"Homepage accessible. RSS provides article links. Hard paywall - {'some text extractable' if paras else 'body blocked'}. Subscription required."

# Fix ThePrint RSS
print("  Fixing: ThePrint RSS", file=sys.stderr)
tp = india_by_domain["theprint.in"]
for rss_url in ["https://theprint.in/defence/feed/", "https://theprint.in/feed/"]:
    rss_ok, rss_full, _ = test_rss(rss_url)
    if rss_ok:
        tp["has_rss"] = True
        tp["rss_url"] = rss_url
        tp["rss_has_full_text"] = rss_full
        break

# Fix Jagran
print("  Fixing: Jagran", file=sys.stderr)
jagran = india_by_domain["jagran.com"]
html = curl_get("https://www.jagran.com/news/national-news")
matches = re.findall(r'href="(https://www\.jagran\.com/[^"]*\d{5,}\.html)"', html)
if matches:
    art = curl_get(matches[0])
    paras = extract_paragraphs(art)
    date = extract_date(art)
    jagran["test_article_url"] = matches[0]
    jagran["publication_date"] = date
    if paras:
        jagran["can_get_full_text"] = len(paras) >= 3
        jagran["first_paragraph"] = paras[0][:300]
        jagran["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
        jagran["notes"] = "Article text extractable. Hindi content. No RSS. Largest circulation Indian newspaper."

# Fix EPW
print("  Fixing: EPW", file=sys.stderr)
epw = india_by_domain["epw.in"]
epw["notes"] = "Homepage returns 403 (anti-bot). Fully paywalled (JSTOR access). Not viable for automated pipeline without subscription and headless browser."

# Fix Gateway House
print("  Fixing: Gateway House", file=sys.stderr)
gw = india_by_domain["gatewayhouse.in"]
rss_ok, rss_full, rss_content = test_rss("https://www.gatewayhouse.in/feed/")
if not rss_ok:
    rss_ok, rss_full, rss_content = test_rss("https://gatewayhouse.in/feed/")
if rss_ok:
    gw["has_rss"] = True
    gw["rss_url"] = "https://www.gatewayhouse.in/feed/"
    gw["rss_has_full_text"] = rss_full
    art_url = find_article_from_rss(rss_content, "gatewayhouse.in")
    if art_url:
        art = curl_get(art_url)
        paras = extract_paragraphs(art)
        if paras:
            gw["can_fetch_article"] = True
            gw["can_get_full_text"] = len(paras) >= 3
            gw["test_article_url"] = art_url
            gw["first_paragraph"] = paras[0][:300]
            gw["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
    # Even if page doesn't extract, RSS has full text
    if rss_full:
        ce = re.findall(r'<content:encoded><!\[CDATA\[(.*?)\]\]>', rss_content, re.DOTALL)
        if ce:
            rss_paras = extract_paragraphs(ce[0])
            if rss_paras and not gw.get("first_paragraph"):
                gw["can_fetch_article"] = True
                gw["can_get_full_text"] = True
                gw["first_paragraph"] = rss_paras[0][:300]
                gw["last_paragraph"] = rss_paras[-1][:300] if len(rss_paras) > 1 else None
    gw["notes"] = "Homepage behind Sucuri WAF (JS challenge). RSS at /feed/ has full content:encoded. RSS is the viable extraction path - bypasses JS requirement."

print("\n=== Fixing Indonesia sources ===", file=sys.stderr)

# Fix Kompas.id
print("  Fixing: Kompas.id", file=sys.stderr)
kompas = indo_by_domain["kompas.id"]
html = curl_get("https://www.kompas.id/")
matches = re.findall(r'href="(https://www\.kompas\.id/baca/[^"]*)"', html)
if not matches:
    matches = re.findall(r'href="(/baca/[^"]*)"', html)
    matches = [f"https://www.kompas.id{m}" for m in matches]
if matches:
    art = curl_get(matches[0])
    paras = extract_paragraphs(art)
    kompas["test_article_url"] = matches[0]
    kompas["can_fetch_article"] = True
    kompas["publication_date"] = extract_date(art)
    if paras:
        kompas["can_get_full_text"] = len(paras) >= 3
        kompas["first_paragraph"] = paras[0][:300]
        kompas["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
        kompas["notes"] = "Article links discoverable. Paywalled premium - some text accessible. Indonesia's most trusted print brand."
    else:
        kompas["notes"] = "Article links found but body text blocked by paywall. Subscription required for full text."

# Fix Kompas.com
print("  Fixing: Kompas.com", file=sys.stderr)
kcom = indo_by_domain["kompas.com"]
html = curl_get("https://news.kompas.com/")
matches = re.findall(r'href="(https://[a-z]+\.kompas\.com/read/\d{4}/\d{2}/\d{2}/[^"]*)"', html)
if matches:
    art = curl_get(matches[0])
    paras = extract_paragraphs(art)
    kcom["test_article_url"] = matches[0]
    kcom["can_fetch_article"] = True
    kcom["publication_date"] = extract_date(art)
    if paras:
        kcom["can_get_full_text"] = len(paras) >= 3
        kcom["first_paragraph"] = paras[0][:300]
        kcom["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
        kcom["notes"] = "Article text extractable from free portal. Lower quality than kompas.id."

# Fix Tempo
print("  Fixing: Tempo", file=sys.stderr)
tempo = indo_by_domain["tempo.co"]
for section in ["https://nasional.tempo.co/", "https://dunia.tempo.co/", "https://www.tempo.co/"]:
    html = curl_get(section)
    matches = re.findall(r'href="(https://[a-z]+\.tempo\.co/read/[^"]*)"', html)
    if not matches:
        matches = re.findall(r'href="(https://www\.tempo\.co/[a-z]+/[a-z0-9-]+)"', html)
    if matches:
        art = curl_get(matches[0])
        paras = extract_paragraphs(art)
        tempo["test_article_url"] = matches[0]
        tempo["can_fetch_article"] = True
        tempo["publication_date"] = extract_date(art)
        if paras:
            tempo["can_get_full_text"] = len(paras) >= 3
            tempo["first_paragraph"] = paras[0][:300]
            tempo["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
            tempo["notes"] = "Article text extractable. Metered paywall. Indonesia's leading investigative outlet."
        else:
            tempo["notes"] = "Article pages load but body paywalled/JS-rendered. Metered paywall."
        break

# Fix Jakarta Post
print("  Fixing: Jakarta Post", file=sys.stderr)
jp = indo_by_domain["thejakartapost.com"]
html = curl_get("https://www.thejakartapost.com/")
matches = re.findall(r'href="(https://www\.thejakartapost\.com/[a-z]+/\d{4}/\d{2}/\d{2}/[^"]*)"', html)
if not matches:
    matches = re.findall(r'href="(/[a-z]+/\d{4}/\d{2}/\d{2}/[^"]*)"', html)
    matches = [f"https://www.thejakartapost.com{m}" for m in matches]
if matches:
    art = curl_get(matches[0])
    paras = extract_paragraphs(art)
    jp["test_article_url"] = matches[0]
    jp["can_fetch_article"] = True
    jp["publication_date"] = extract_date(art)
    if paras:
        jp["can_get_full_text"] = len(paras) >= 3
        jp["first_paragraph"] = paras[0][:300]
        jp["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
        jp["notes"] = "Article text extractable. Soft paywall. Primary English-language Indonesia source. Op-ed page features diplomats and policy figures."

# Fix Jakarta Globe
print("  Fixing: Jakarta Globe", file=sys.stderr)
jg = indo_by_domain["jakartaglobe.id"]
status = curl_status("https://jakartaglobe.id/")
jg["can_fetch_homepage"] = 200 <= status < 400
html = curl_get("https://jakartaglobe.id/")
matches = re.findall(r'href="(https://jakartaglobe\.id/[a-z]+/[a-z0-9-]+)"', html)
if matches:
    art_status = curl_status(matches[0])
    jg["test_article_url"] = matches[0]
    if 200 <= art_status < 400:
        art = curl_get(matches[0])
        paras = extract_paragraphs(art)
        jg["can_fetch_article"] = True
        jg["publication_date"] = extract_date(art)
        if paras:
            jg["can_get_full_text"] = len(paras) >= 3
            jg["first_paragraph"] = paras[0][:300]
            jg["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
            jg["notes"] = "Article text extractable. Free access, ad-supported. Second English-language perspective."
    else:
        jg["notes"] = f"Homepage {'accessible' if jg['can_fetch_homepage'] else 'blocked'}. Article returns {art_status}. Anti-bot protection. Requires browser."

# Fix Detik
print("  Fixing: Detik", file=sys.stderr)
detik = indo_by_domain["detik.com"]
rss_content = curl_get("https://rss.detik.com/index.php/detikcom", max_bytes=20000)
if '<rss' in rss_content[:500] or '<channel' in rss_content[:500]:
    detik["has_rss"] = True
    detik["rss_url"] = "https://rss.detik.com/index.php/detikcom"
    detik["rss_has_full_text"] = bool(re.search(r'<description>[^<]{500,}', rss_content))
    art_url = find_article_from_rss(rss_content, "detik.com")
    if art_url:
        art = curl_get(art_url)
        paras = extract_paragraphs(art)
        detik["test_article_url"] = art_url
        detik["can_fetch_article"] = True
        detik["publication_date"] = extract_date(art)
        if paras:
            detik["can_get_full_text"] = len(paras) >= 3
            detik["first_paragraph"] = paras[0][:300]
            detik["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
            detik["notes"] = "Article text extractable. RSS at rss.detik.com. #1 news site in Indonesia (~180M daily visits)."

# Fix CNN Indonesia
print("  Fixing: CNN Indonesia", file=sys.stderr)
cnn_id = indo_by_domain["cnnindonesia.com"]
html = curl_get("https://www.cnnindonesia.com/nasional")
matches = re.findall(r'href="(https://www\.cnnindonesia\.com/nasional/\d{14}-[^"]*)"', html)
if matches:
    art = curl_get(matches[0])
    paras = extract_paragraphs(art)
    cnn_id["test_article_url"] = matches[0]
    cnn_id["can_fetch_article"] = True
    cnn_id["publication_date"] = extract_date(art)
    if paras:
        cnn_id["can_get_full_text"] = len(paras) >= 3
        cnn_id["first_paragraph"] = paras[0][:300]
        cnn_id["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
        cnn_id["notes"] = "Article text extractable. RSS at /rss with full descriptions. Free access."

# Fix Tirto
print("  Fixing: Tirto", file=sys.stderr)
tirto = indo_by_domain["tirto.id"]
status = curl_status("https://tirto.id")
tirto["can_fetch_homepage"] = 200 <= status < 400
if status == 403:
    tirto["can_fetch_article"] = False
    tirto["can_get_full_text"] = False
    tirto["first_paragraph"] = None
    tirto["last_paragraph"] = None
    tirto["test_article_url"] = None
    tirto["notes"] = "Returns 403 (Cloudflare anti-bot). Free site but aggressive bot protection. Requires headless browser with Cloudflare bypass."

# Fix Kemlu
print("  Fixing: Kemlu", file=sys.stderr)
kemlu = indo_by_domain["kemlu.go.id"]
html = curl_get("https://kemlu.go.id/portal/id/read/1/berita")
matches = re.findall(r'href="(/portal/id/read/\d+/[^"]*)"', html)
if matches:
    url = f"https://kemlu.go.id{matches[0]}"
    art = curl_get(url)
    paras = extract_paragraphs(art)
    kemlu["test_article_url"] = url
    kemlu["can_fetch_article"] = True
    kemlu["publication_date"] = extract_date(art)
    if paras:
        kemlu["can_get_full_text"] = len(paras) >= 3
        kemlu["first_paragraph"] = paras[0][:300]
        kemlu["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
        kemlu["notes"] = "Press releases accessible. Full text extractable. No RSS. Indonesian with some English translations."

# Fix Setkab
print("  Fixing: Setkab", file=sys.stderr)
setkab = indo_by_domain["setkab.go.id"]
html = curl_get("https://setkab.go.id/")
matches = re.findall(r'href="(https://setkab\.go\.id/[a-z-]{20,}[^"]*)"', html)
if matches:
    art = curl_get(matches[0])
    paras = extract_paragraphs(art)
    setkab["test_article_url"] = matches[0]
    setkab["can_fetch_article"] = True
    setkab["publication_date"] = extract_date(art)
    if paras:
        setkab["can_get_full_text"] = len(paras) >= 3
        setkab["first_paragraph"] = paras[0][:300]
        setkab["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
        setkab["notes"] = "Article text extractable. WordPress-based."
for rss_url in ["https://setkab.go.id/feed/", "https://setkab.go.id/rss"]:
    rss_ok, rss_full, _ = test_rss(rss_url)
    if rss_ok:
        setkab["has_rss"] = True
        setkab["rss_url"] = rss_url
        setkab["rss_has_full_text"] = rss_full
        break

# Fix Antara - get actual article URL
print("  Fixing: Antara", file=sys.stderr)
antara = indo_by_domain["antaranews.com"]
rss_content = curl_get("https://antaranews.com/rss/terkini", max_bytes=20000)
art_url = find_article_from_rss(rss_content, "antaranews.com")
if art_url:
    art = curl_get(art_url)
    paras = extract_paragraphs(art)
    antara["test_article_url"] = art_url
    antara["publication_date"] = extract_date(art)
    if paras:
        antara["first_paragraph"] = paras[0][:300]
        antara["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
        antara["can_get_full_text"] = len(paras) >= 3
        antara["notes"] = "Full text extractable. RSS with full content. State wire service. Free access."

# Fix CNBC Indonesia first paragraph
print("  Fixing: CNBC Indonesia", file=sys.stderr)
cnbc = indo_by_domain["cnbcindonesia.com"]
if cnbc.get("first_paragraph", "").startswith("Search"):
    rss_content = curl_get("https://cnbcindonesia.com/rss", max_bytes=20000)
    art_url = find_article_from_rss(rss_content, "cnbcindonesia.com")
    if art_url:
        art = curl_get(art_url)
        paras = extract_paragraphs(art)
        real_paras = [p for p in paras if not p.startswith("Search") and len(p) > 80]
        if real_paras:
            cnbc["test_article_url"] = art_url
            cnbc["publication_date"] = extract_date(art)
            cnbc["first_paragraph"] = real_paras[0][:300]
            cnbc["last_paragraph"] = real_paras[-1][:300] if len(real_paras) > 1 else None

# Fix CSIS Jakarta
print("  Fixing: CSIS Jakarta", file=sys.stderr)
csis = indo_by_domain["csis.or.id"]
html = curl_get("https://www.csis.or.id/publications")
matches = re.findall(r'href="(https://www\.csis\.or\.id/publications/[^"]*)"', html)
if not matches:
    matches = re.findall(r'href="(/publications/[^"]*)"', html)
    matches = [f"https://www.csis.or.id{m}" for m in matches]
if matches:
    art = curl_get(matches[0])
    paras = extract_paragraphs(art)
    csis["test_article_url"] = matches[0]
    csis["publication_date"] = extract_date(art)
    if paras:
        csis["can_get_full_text"] = len(paras) >= 3
        csis["first_paragraph"] = paras[0][:300]
        csis["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
        csis["notes"] = "Publication text extractable. Premier Indonesian foreign policy think tank. No RSS."

# Fix Kemhan
print("  Fixing: Kemhan", file=sys.stderr)
kemhan = indo_by_domain["kemhan.go.id"]
html = curl_get("https://www.kemhan.go.id/")
matches = re.findall(r'href="(https://www\.kemhan\.go\.id/\d{4}/\d{2}/\d{2}/[^"]*)"', html)
if matches:
    art = curl_get(matches[0])
    paras = extract_paragraphs(art)
    if paras:
        kemhan["test_article_url"] = matches[0]
        kemhan["publication_date"] = extract_date(art)
        kemhan["can_fetch_article"] = True
        kemhan["can_get_full_text"] = len(paras) >= 3
        kemhan["first_paragraph"] = paras[0][:300]
        kemhan["last_paragraph"] = paras[-1][:300] if len(paras) > 1 else None
        kemhan["notes"] = "Article text extractable. RSS at /rss. WordPress-based. Indonesian only. Defense white papers, procurement, exercises."

# Remove non-schema fields
for entry in india + indo:
    entry.pop("homepage_status_code", None)

# Write
with open(f"{output_dir}/india_accessibility.json", "w") as f:
    json.dump(india, f, indent=2, ensure_ascii=False)
with open(f"{output_dir}/indonesia_accessibility.json", "w") as f:
    json.dump(indo, f, indent=2, ensure_ascii=False)

# Summary
print("\n=== UPDATED SUMMARY ===", file=sys.stderr)
for label, results in [("India", india), ("Indonesia", indo)]:
    hp_ok = sum(1 for r in results if r["can_fetch_homepage"])
    art_ok = sum(1 for r in results if r["can_fetch_article"])
    ft_ok = sum(1 for r in results if r["can_get_full_text"])
    rss_ok = sum(1 for r in results if r["has_rss"])
    print(f"\n{label}: {hp_ok}/{len(results)} homepage, {art_ok}/{len(results)} article, {ft_ok}/{len(results)} full-text, {rss_ok}/{len(results)} RSS", file=sys.stderr)
    for r in results:
        status = "OK" if r["can_fetch_article"] else "FAIL"
        rss_s = "RSS" if r["has_rss"] else "no-RSS"
        ft_s = "FT" if r["can_get_full_text"] else "no-FT"
        print(f"  [{status}] [{rss_s}] [{ft_s}] {r['source_name']} ({r['domain']})", file=sys.stderr)

print("\nDONE")
