"""Migrate country configs from old schema to new schema.

Converts:
- Old `sources` block → `news_discovery` + `government_discovery` references
- Old `search` field names → new `SearchBudget` names
- Creates government domain configs from old `sources.government`
"""

import yaml
from pathlib import Path

CONFIGS_DIR = Path("assets/country_configs/countries")
GOV_DIR = Path("assets/government")
GOV_DIR.mkdir(exist_ok=True)

# Information culture assignments from the spec
INFO_CULTURE = {
    "ca": "transparent", "mx": "managed", "br": "managed", "cl": "transparent",
    "fr": "transparent", "de": "transparent", "gb": "transparent", "it": "transparent",
    "es": "transparent", "no": "transparent", "se": "transparent", "ua": "managed",
    "pl": "transparent", "fi": "transparent", "ee": "transparent", "lt": "transparent",
    "lv": "transparent", "cz": "transparent", "ro": "transparent", "tr": "managed",
    "sa": "managed", "ae": "managed", "in": "managed", "tw": "transparent",
    "jp": "transparent", "kr": "transparent", "au": "transparent", "id": "managed",
}

# Brave search language mapping (ISO 639-1)
LANG_MAP = {
    "au": "en", "ae": "ar", "br": "pt", "ca": "en", "cl": "es", "cz": "cs",
    "de": "de", "ee": "et", "es": "es", "fi": "fi", "fr": "fr", "gb": "en",
    "id": "id", "in": "en", "it": "it", "jp": "ja", "kr": "ko", "lt": "lt",
    "lv": "lv", "mx": "es", "no": "no", "pl": "pl", "ro": "ro", "sa": "ar",
    "se": "sv", "tr": "tr", "tw": "zh", "ua": "uk",
}

# Brave country code (uppercase ISO 3166-1 alpha-2)
BRAVE_COUNTRY = {k: k.upper() for k in INFO_CULTURE}


def migrate_config(code: str):
    path = CONFIGS_DIR / f"{code}.yaml"
    with open(path) as f:
        data = yaml.safe_load(f)

    # Skip if already migrated (has news_discovery)
    if "news_discovery" in data:
        print(f"  {code}: already migrated, skipping")
        return

    old_sources = data.pop("sources", {})
    old_search = data.pop("search", {})

    # Build new news_discovery
    primary_lang = LANG_MAP.get(code, "en")
    data["news_discovery"] = {
        "goggle_file": f"assets/country_goggles/{code}.goggle",
        "extraction_config": "assets/country_configs/extraction_routing.yaml",
        "brave_params": {
            "country": BRAVE_COUNTRY[code],
            "search_lang": primary_lang,
            "freshness": "pw",
        },
    }

    # Build government_discovery reference
    data["government_discovery"] = {
        "config_file": f"assets/government/{code}.yaml",
    }

    # Add interpretive_context_file
    data["interpretive_context_file"] = f"assets/context/{code}_sources.md"

    # Convert search field names
    data["search"] = {
        "triage_queries_max": old_search.get("triage_domestic_max", 3),
        "deep_dive_queries_max": old_search.get("deep_dive_max", 20),
    }

    # Ensure languages is the right structure
    if "languages" not in data or not isinstance(data.get("languages"), dict):
        data["languages"] = {"primary": primary_lang, "additional": [], "metadata": "en"}
    else:
        langs = data["languages"]
        if "primary" not in langs:
            langs["primary"] = primary_lang
        if "metadata" not in langs:
            langs["metadata"] = "en"
        if "additional" not in langs:
            langs["additional"] = []

    # Write updated config
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"  {code}: config migrated")

    # Create government domain config from old sources.government
    gov_sources = old_sources.get("government", [])
    if gov_sources:
        gov_data = {
            "country": data["country"],
            "code": code,
            "information_culture": INFO_CULTURE.get(code, "managed"),
            "domains": [],
            "query_terms": [],
        }
        for src in gov_sources:
            gov_data["domains"].append({
                "domain": src["domain"],
                "institutions": [src.get("name", src["domain"])],
                "priority": "P1" if src.get("tier", 2) == 1 else "P2",
            })

        gov_path = GOV_DIR / f"{code}.yaml"
        with open(gov_path, "w") as f:
            yaml.dump(gov_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"  {code}: government config created")
    else:
        print(f"  {code}: no government sources to migrate")


if __name__ == "__main__":
    print("Migrating country configs...")
    for path in sorted(CONFIGS_DIR.glob("*.yaml")):
        code = path.stem
        migrate_config(code)
    print("Done.")
