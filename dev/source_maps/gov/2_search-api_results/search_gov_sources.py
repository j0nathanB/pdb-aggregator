#!/usr/bin/env python3
"""
Search government source domains via SearchAPI (Google) for recent content.

Reads country configs from COUNTRY_CONFIGS below, runs site:-scoped searches
for each domain, and saves structured JSON results to the output directory.

Usage:
    python search_gov_sources.py australia
    python search_gov_sources.py --all
    python search_gov_sources.py australia united_kingdom france

Requires SEARCHAPI_KEY in .env or environment.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SEARCHAPI_BASE = "https://www.searchapi.io/api/v1/search"
ENGINE = "google"
TIME_PERIOD = "last_month"
RESULTS_DIR = Path(__file__).parent

# Each country config: location (capital city), gl code, and list of
# (source_id, domain, search_term) tuples.  Search terms are intentionally
# broad — the goal is to cast a wide net and collect URLs.

COUNTRY_CONFIGS = {
    "australia": {
        "location": "Canberra,Australia",
        "gl": "au",
        "hl": "en",
        "sources": [
            ("au_pm", "pm.gov.au", "budget"),
            ("au_dfat_foreign_minister", "foreignminister.gov.au", "trade"),
            ("au_defence", "defence.gov.au", "security"),
            ("au_treasury", "treasury.gov.au", "spending"),
            ("au_parliament", "aph.gov.au", "defence estimates"),
            ("au_rba", "rba.gov.au", "inflation"),
            ("au_homeaffairs", "homeaffairs.gov.au", "border security"),
            ("au_dfat_sanctions", "dfat.gov.au", "sanctions"),
            ("au_industry", "industry.gov.au", "critical minerals"),
            ("au_legislation", "legislation.gov.au", "regulation"),
            ("au_asio", "asio.gov.au", "threat"),
            ("au_asd", "asd.gov.au", "cyber"),
            ("au_austrade", "austrade.gov.au", "export"),
            ("au_oni", "oni.gov.au", "intelligence"),
            ("au_nationalsecurity", "nationalsecurity.gov.au", "terrorism"),
        ],
    },
    "united_kingdom": {
        "location": "London,England,United Kingdom",
        "gl": "gb",
        "hl": "en",
        "sources": [
            ("uk_pm", "gov.uk", "prime minister statement"),
            ("uk_fcdo", "gov.uk", "foreign commonwealth development office"),
            ("uk_mod", "gov.uk", "ministry defence"),
            ("uk_treasury", "gov.uk", "treasury budget"),
            ("uk_parliament", "parliament.uk", "defence debate"),
            ("uk_boe", "bankofengland.co.uk", "inflation"),
            ("uk_legislation", "legislation.gov.uk", "regulation"),
            ("uk_trade", "gov.uk", "trade policy"),
            ("uk_mi5", "mi5.gov.uk", "threat"),
            ("uk_gchq", "gchq.gov.uk", "cyber"),
        ],
    },
    "france": {
        "location": "Paris,Ile-de-France,France",
        "gl": "fr",
        "hl": "fr",
        "sources": [
            ("fr_elysee", "elysee.fr", "budget"),
            ("fr_diplomatie", "diplomatie.gouv.fr", "sanctions"),
            ("fr_defense", "defense.gouv.fr", "securite"),
            ("fr_economie", "economie.gouv.fr", "depenses"),
            ("fr_assemblee", "assemblee-nationale.fr", "defense"),
            ("fr_senat", "senat.fr", "defense"),
            ("fr_banque", "banque-france.fr", "inflation"),
            ("fr_legifrance", "legifrance.gouv.fr", "decret"),
        ],
    },
    "germany": {
        "location": "Berlin,Germany",
        "gl": "de",
        "hl": "de",
        "sources": [
            ("de_bundeskanzler", "bundeskanzler.de", "Haushalt"),
            ("de_auswaertiges", "auswaertiges-amt.de", "Sanktionen"),
            ("de_bmvg", "bmvg.de", "Sicherheit"),
            ("de_bmf", "bundesfinanzministerium.de", "Ausgaben"),
            ("de_bundestag", "bundestag.de", "Verteidigung"),
            ("de_bundesbank", "bundesbank.de", "Inflation"),
            ("de_gesetze", "gesetze-im-internet.de", "Verordnung"),
        ],
    },
    "japan": {
        "location": "Tokyo,Japan",
        "gl": "jp",
        "hl": "ja",
        "sources": [
            ("jp_kantei", "kantei.go.jp", "予算"),
            ("jp_mofa", "mofa.go.jp", "外交"),
            ("jp_mod", "mod.go.jp", "防衛"),
            ("jp_mof", "mof.go.jp", "財政"),
            ("jp_diet", "sangiin.go.jp", "安全保障"),
            ("jp_boj", "boj.or.jp", "物価"),
        ],
    },
    "india": {
        "location": "New Delhi,India",
        "gl": "in",
        "hl": "en",
        "sources": [
            ("in_pmo", "pmindia.gov.in", "budget"),
            ("in_mea", "mea.gov.in", "bilateral"),
            ("in_mod", "mod.gov.in", "defence"),
            ("in_mof", "finmin.nic.in", "expenditure"),
            ("in_parliament", "sansad.in", "defence"),
            ("in_rbi", "rbi.org.in", "inflation"),
        ],
    },
    "canada": {
        "location": "Ottawa,Ontario,Canada",
        "gl": "ca",
        "hl": "en",
        "sources": [
            ("ca_pm", "pm.gc.ca", "budget"),
            ("ca_gac", "international.gc.ca", "sanctions"),
            ("ca_dnd", "canada.ca", "national defence"),
            ("ca_finance", "canada.ca", "finance budget"),
            ("ca_parliament", "parl.ca", "defence"),
            ("ca_boc", "bankofcanada.ca", "inflation"),
        ],
    },
    "brazil": {
        "location": "Brasilia,Federal District,Brazil",
        "gl": "br",
        "hl": "pt",
        "sources": [
            ("br_planalto", "gov.br/planalto", "orcamento"),
            ("br_mre", "gov.br/mre", "relacoes"),
            ("br_defesa", "gov.br/defesa", "seguranca"),
            ("br_fazenda", "gov.br/fazenda", "despesa"),
            ("br_senado", "senado.leg.br", "defesa"),
            ("br_bcb", "bcb.gov.br", "inflacao"),
        ],
    },
    "south_korea": {
        "location": "Seoul,South Korea",
        "gl": "kr",
        "hl": "ko",
        "sources": [
            ("kr_president", "president.go.kr", "예산"),
            ("kr_mofa", "mofa.go.kr", "외교"),
            ("kr_mnd", "mnd.go.kr", "국방"),
            ("kr_mosf", "moef.go.kr", "재정"),
            ("kr_assembly", "assembly.go.kr", "안보"),
            ("kr_bok", "bok.or.kr", "물가"),
        ],
    },
    "italy": {
        "location": "Rome,Lazio,Italy",
        "gl": "it",
        "hl": "it",
        "sources": [
            ("it_governo", "governo.it", "bilancio"),
            ("it_esteri", "esteri.it", "sanzioni"),
            ("it_difesa", "difesa.it", "sicurezza"),
            ("it_mef", "mef.gov.it", "spesa"),
            ("it_parlamento", "parlamento.it", "difesa"),
            ("it_bankitalia", "bancaditalia.it", "inflazione"),
        ],
    },
    "spain": {
        "location": "Madrid,Spain",
        "gl": "es",
        "hl": "es",
        "sources": [
            ("es_moncloa", "lamoncloa.gob.es", "presupuesto"),
            ("es_exteriores", "exteriores.gob.es", "sanciones"),
            ("es_defensa", "defensa.gob.es", "seguridad"),
            ("es_hacienda", "hacienda.gob.es", "gasto"),
            ("es_congreso", "congreso.es", "defensa"),
            ("es_bde", "bde.es", "inflacion"),
        ],
    },
    "mexico": {
        "location": "Mexico City,Mexico",
        "gl": "mx",
        "hl": "es",
        "sources": [
            ("mx_presidencia", "gob.mx/presidencia", "presupuesto"),
            ("mx_sre", "gob.mx/sre", "relaciones"),
            ("mx_sedena", "gob.mx/sedena", "seguridad"),
            ("mx_shcp", "gob.mx/hacienda", "gasto"),
            ("mx_senado", "senado.gob.mx", "seguridad"),
            ("mx_banxico", "banxico.org.mx", "inflacion"),
        ],
    },
    "chile": {
        "location": "Santiago,Santiago Metropolitan Region,Chile",
        "gl": "cl",
        "hl": "es",
        "sources": [
            ("cl_presidencia", "prensa.presidencia.cl", "presupuesto"),
            ("cl_minrel", "minrel.gob.cl", "relaciones"),
            ("cl_defensa", "defensa.cl", "seguridad"),
            ("cl_hacienda", "hacienda.cl", "gasto"),
            ("cl_senado", "senado.cl", "defensa"),
            ("cl_bcentral", "bcentral.cl", "inflacion"),
        ],
    },
    "turkey": {
        "location": None,  # SearchAPI doesn't recognize Turkish locations
        "gl": "tr",
        "hl": "tr",
        "sources": [
            ("tr_tccb", "tccb.gov.tr", "bütçe"),
            ("tr_mfa", "mfa.gov.tr", "yaptırım"),
            ("tr_msb", "msb.gov.tr", "güvenlik"),
            ("tr_hmb", "hmb.gov.tr", "harcama"),
            ("tr_tbmm", "tbmm.gov.tr", "savunma"),
            ("tr_tcmb", "tcmb.gov.tr", "enflasyon"),
        ],
    },
    "indonesia": {
        "location": "Jakarta,Indonesia",
        "gl": "id",
        "hl": "id",
        "sources": [
            ("id_setkab", "setkab.go.id", "anggaran"),
            ("id_kemlu", "kemlu.go.id", "diplomasi"),
            ("id_kemhan", "kemhan.go.id", "pertahanan"),
            ("id_kemenkeu", "kemenkeu.go.id", "belanja"),
            ("id_dpr", "dpr.go.id", "pertahanan"),
            ("id_bi", "bi.go.id", "inflasi"),
        ],
    },
    "saudi_arabia": {
        "location": "Riyadh,Riyadh Province,Saudi Arabia",
        "gl": "sa",
        "hl": "ar",
        "sources": [
            ("sa_spa", "spa.gov.sa", "ميزانية"),
            ("sa_mofa", "mofa.gov.sa", "دبلوماسية"),
            ("sa_mod", "mod.gov.sa", "دفاع"),
            ("sa_mof", "mof.gov.sa", "إنفاق"),
            ("sa_sama", "sama.gov.sa", "تضخم"),
        ],
    },
    "uae": {
        "location": "Abu Dhabi,United Arab Emirates",
        "gl": "ae",
        "hl": "ar",
        "sources": [
            ("ae_mofa", "mofa.gov.ae", "دبلوماسية"),
            ("ae_mod", "mod.gov.ae", "دفاع"),
            ("ae_mof", "mof.gov.ae", "ميزانية"),
            ("ae_cbuae", "centralbank.ae", "تضخم"),
        ],
    },
    "taiwan": {
        "location": "Taipei City,Taiwan",
        "gl": "tw",
        "hl": "zh-TW",
        "sources": [
            ("tw_president", "president.gov.tw", "預算"),
            ("tw_mofa", "mofa.gov.tw", "外交"),
            ("tw_mnd", "mnd.gov.tw", "國防"),
            ("tw_mof", "mof.gov.tw", "財政"),
            ("tw_ly", "ly.gov.tw", "國防"),
            ("tw_cbc", "cbc.gov.tw", "通膨"),
        ],
    },
    "ukraine": {
        "location": "Kyiv,Kyiv City,Ukraine",
        "gl": "ua",
        "hl": "uk",
        "sources": [
            ("ua_president", "president.gov.ua", "бюджет"),
            ("ua_mfa", "mfa.gov.ua", "дипломатія"),
            ("ua_mod", "mil.gov.ua", "оборона"),
            ("ua_mof", "mof.gov.ua", "видатки"),
            ("ua_rada", "rada.gov.ua", "безпека"),
            ("ua_nbu", "bank.gov.ua", "інфляція"),
        ],
    },
    "poland": {
        "location": "Warsaw,Masovian Voivodeship,Poland",
        "gl": "pl",
        "hl": "pl",
        "sources": [
            ("pl_premier", "premier.gov.pl", "budżet"),
            ("pl_msz", "gov.pl", "dyplomacja sankcje"),
            ("pl_mon", "gov.pl", "obrona narodowa bezpieczeństwo"),
            ("pl_mf", "gov.pl", "finanse wydatki"),
            ("pl_sejm", "sejm.gov.pl", "obronność"),
            ("pl_nbp", "nbp.pl", "inflacja"),
        ],
    },
    "romania": {
        "location": "Bucharest,Romania",
        "gl": "ro",
        "hl": "ro",
        "sources": [
            ("ro_gov", "gov.ro", "buget"),
            ("ro_mae", "mae.ro", "diplomatie"),
            ("ro_mapn", "mapn.ro", "aparare"),
            ("ro_mf", "mfinante.gov.ro", "cheltuieli"),
            ("ro_parlament", "cdep.ro", "aparare"),
            ("ro_bnr", "bnr.ro", "inflatie"),
        ],
    },
    "czech_republic": {
        "location": "Prague,Czechia",
        "gl": "cz",
        "hl": "cs",
        "sources": [
            ("cz_vlada", "vlada.cz", "rozpočet"),
            ("cz_mzv", "mzv.cz", "sankce"),
            ("cz_mo", "army.cz", "bezpečnost"),
            ("cz_mf", "mfcr.cz", "výdaje"),
            ("cz_psp", "psp.cz", "obrana"),
            ("cz_cnb", "cnb.cz", "inflace"),
        ],
    },
    "estonia": {
        "location": "Tallinn,Harju County,Estonia",
        "gl": "ee",
        "hl": "et",
        "sources": [
            ("ee_vv", "valitsus.ee", "eelarve"),
            ("ee_vm", "vm.ee", "sanktsioonid"),
            ("ee_kmin", "kaitseministeerium.ee", "julgeolek"),
            ("ee_rm", "fin.ee", "kulud"),
            ("ee_riigikogu", "riigikogu.ee", "kaitse"),
            ("ee_ep", "eestipank.ee", "inflatsioon"),
        ],
    },
    "latvia": {
        "location": "Riga,Latvia",
        "gl": "lv",
        "hl": "lv",
        "sources": [
            ("lv_mk", "mk.gov.lv", "budžets"),
            ("lv_mfa", "mfa.gov.lv", "sankcijas"),
            ("lv_mod", "mod.gov.lv", "drošība"),
            ("lv_fm", "fm.gov.lv", "izdevumi"),
            ("lv_saeima", "saeima.lv", "aizsardzība"),
            ("lv_lb", "bank.lv", "inflācija"),
        ],
    },
    "lithuania": {
        "location": "Vilnius,Vilnius County,Lithuania",
        "gl": "lt",
        "hl": "lt",
        "sources": [
            ("lt_lrv", "lrv.lt", "biudžetas"),
            ("lt_urm", "urm.lt", "sankcijos"),
            ("lt_kam", "kam.lt", "saugumas"),
            ("lt_fm", "finmin.lrv.lt", "išlaidos"),
            ("lt_seimas", "lrs.lt", "gynyba"),
            ("lt_lb", "lb.lt", "infliacija"),
        ],
    },
    "finland": {
        "location": "Helsinki,Uusimaa,Finland",
        "gl": "fi",
        "hl": "fi",
        "sources": [
            ("fi_vn", "valtioneuvosto.fi", "budjetti"),
            ("fi_um", "um.fi", "pakotteet"),
            ("fi_defmin", "defmin.fi", "turvallisuus"),
            ("fi_vm", "vm.fi", "menot"),
            ("fi_eduskunta", "eduskunta.fi", "puolustus"),
            ("fi_bof", "suomenpankki.fi", "inflaatio"),
        ],
    },
    "sweden": {
        "location": "Stockholm,Stockholm County,Sweden",
        "gl": "se",
        "hl": "sv",
        "sources": [
            ("se_regeringen", "regeringen.se", "budget"),
            ("se_ud", "regeringen.se", "sanktioner"),
            ("se_forsvar", "regeringen.se", "försvar"),
            ("se_fi", "fi.se", "utgifter"),
            ("se_riksdagen", "riksdagen.se", "försvar"),
            ("se_riksbank", "riksbank.se", "inflation"),
        ],
    },
    "norway": {
        "location": "Oslo,Norway",
        "gl": "no",
        "hl": "no",
        "sources": [
            ("no_regjeringen", "regjeringen.no", "budsjett"),
            ("no_ud", "regjeringen.no", "sanksjoner"),
            ("no_fd", "regjeringen.no", "forsvar"),
            ("no_fin", "regjeringen.no", "utgifter"),
            ("no_stortinget", "stortinget.no", "forsvar"),
            ("no_norgesbank", "norges-bank.no", "inflasjon"),
        ],
    },
}


def search_source(api_key: str, source_id: str, domain: str, term: str,
                  location: str, gl: str, hl: str) -> dict:
    """Run a single site:-scoped Google search via SearchAPI."""
    params = {
        "engine": ENGINE,
        "q": f"site:{domain} {term}",
        "gl": gl,
        "hl": hl,
        "time_period": TIME_PERIOD,
        "api_key": api_key,
    }
    if location:
        params["location"] = location
    url = f"{SEARCHAPI_BASE}?{urlencode(params)}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    organic = data.get("organic_results", [])
    total = data.get("search_information", {}).get("total_results", len(organic))

    results = []
    for r in organic:
        results.append({
            "title": r.get("title", ""),
            "url": r.get("link", ""),
            "date": r.get("date", ""),
            "snippet": r.get("snippet", ""),
        })

    return {
        "id": source_id,
        "domain": domain,
        "query": f"site:{domain} {term}",
        "total_results": total,
        "results": results,
    }


def run_country(country: str, api_key: str) -> dict:
    """Search all sources for a given country and return structured output."""
    cfg = COUNTRY_CONFIGS[country]
    location = cfg["location"]
    gl = cfg["gl"]
    hl = cfg["hl"]

    print(f"\n{'='*60}")
    print(f"  {country.upper()} — location={location}, gl={gl}")
    print(f"{'='*60}")

    sources_output = []
    total_urls = 0
    sources_with_results = 0
    sources_without = []

    for source_id, domain, term in cfg["sources"]:
        print(f"  [{source_id}] site:{domain} {term} ... ", end="", flush=True)
        try:
            result = search_source(api_key, source_id, domain, term,
                                   location, gl, hl)
            n = result["total_results"]
            n_urls = len(result["results"])
            total_urls += n_urls
            if n > 0:
                sources_with_results += 1
            else:
                sources_without.append(domain)
            print(f"{n} results ({n_urls} URLs captured)")
            sources_output.append(result)
        except Exception as e:
            print(f"ERROR: {e}")
            sources_output.append({
                "id": source_id,
                "domain": domain,
                "query": f"site:{domain} {term}",
                "total_results": 0,
                "results": [],
                "error": str(e),
            })
            sources_without.append(domain)

        # Respect rate limits — 1 req/sec is safe
        time.sleep(1.0)

    output = {
        "country": country,
        "search_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "location": location,
        "gl": gl,
        "time_period": TIME_PERIOD,
        "sources": sources_output,
        "summary": {
            "total_sources_searched": len(cfg["sources"]),
            "sources_with_results": sources_with_results,
            "sources_without_results": sources_without,
            "total_urls_collected": total_urls,
        },
    }

    # Save to JSON
    out_path = RESULTS_DIR / f"{country}.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n  Saved → {out_path}")
    print(f"  {sources_with_results}/{len(cfg['sources'])} sources returned results, {total_urls} URLs collected")

    return output


def main():
    parser = argparse.ArgumentParser(description="Search government sources via SearchAPI")
    parser.add_argument("countries", nargs="*", help="Country keys to search (e.g. australia france)")
    parser.add_argument("--all", action="store_true", help="Search all configured countries")
    parser.add_argument("--list", action="store_true", help="List available country configs")
    args = parser.parse_args()

    if args.list:
        for k, v in sorted(COUNTRY_CONFIGS.items()):
            print(f"  {k:25s} {v['location']:30s} ({len(v['sources'])} sources)")
        return

    # Load API key
    load_dotenv(Path(__file__).resolve().parents[4] / ".env")
    api_key = os.environ.get("SEARCHAPI_KEY")
    if not api_key:
        print("ERROR: SEARCHAPI_KEY not found in environment or .env", file=sys.stderr)
        sys.exit(1)

    countries = list(COUNTRY_CONFIGS.keys()) if args.all else args.countries
    if not countries:
        parser.print_help()
        sys.exit(1)

    invalid = [c for c in countries if c not in COUNTRY_CONFIGS]
    if invalid:
        print(f"ERROR: Unknown countries: {', '.join(invalid)}", file=sys.stderr)
        print(f"Available: {', '.join(sorted(COUNTRY_CONFIGS.keys()))}", file=sys.stderr)
        sys.exit(1)

    for country in countries:
        run_country(country, api_key)

    print(f"\nDone. {len(countries)} countries searched.")


if __name__ == "__main__":
    main()
