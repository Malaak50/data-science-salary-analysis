"""Référentiel pays (code ISO 2 lettres) -> continent.

Utilisé pour réduire la cardinalité de employee_residence et company_location
(étapes 22 et 32). Les codes ont été vérifiés contre les données réelles du
dataset (104 résidences, 97 localisations, 3 codes non-ISO mappés manuellement).
"""

COUNTRY_TO_CONTINENT = {
    # Amérique du Nord
    "US": "North America", "CA": "North America", "MX": "North America",
    "BM": "North America", "PR": "North America",
    # Amérique du Sud et Caraïbes
    "BR": "South America", "AR": "South America", "CL": "South America",
    "CO": "South America", "PE": "South America", "VE": "South America",
    "UY": "South America", "EC": "South America", "BO": "South America",
    "PY": "South America", "CR": "South America", "PA": "South America",
    "DO": "South America", "GT": "South America", "SV": "South America",
    "HN": "South America", "NI": "South America", "CU": "South America",
    "JM": "South America", "TT": "South America", "BB": "South America",
    "BS": "South America", "HT": "South America",
    # Europe
    "GB": "Europe", "DE": "Europe", "FR": "Europe", "NL": "Europe",
    "ES": "Europe", "IT": "Europe", "IE": "Europe", "PT": "Europe",
    "PL": "Europe", "LT": "Europe", "LV": "Europe", "AT": "Europe",
    "SK": "Europe", "FI": "Europe", "SE": "Europe", "NO": "Europe",
    "DK": "Europe", "CH": "Europe", "BE": "Europe", "CZ": "Europe",
    "HU": "Europe", "RO": "Europe", "BG": "Europe", "GR": "Europe",
    "HR": "Europe", "SI": "Europe", "EE": "Europe", "LU": "Europe",
    "IS": "Europe", "MT": "Europe", "CY": "Europe", "RS": "Europe",
    "UA": "Europe", "BY": "Europe", "MD": "Europe", "AL": "Europe",
    "MK": "Europe", "BA": "Europe", "ME": "Europe", "RU": "Europe",
    "AD": "Europe", "MC": "Europe", "SM": "Europe", "LI": "Europe",
    "GI": "Europe", "FO": "Europe", "GL": "Europe",
    # Asie
    "IN": "Asia", "JP": "Asia", "CN": "Asia", "SG": "Asia",
    "HK": "Asia", "KR": "Asia", "TW": "Asia", "MY": "Asia",
    "TH": "Asia", "ID": "Asia", "PH": "Asia", "VN": "Asia",
    "PK": "Asia", "BD": "Asia", "LK": "Asia", "NP": "Asia",
    "KH": "Asia", "MM": "Asia", "KZ": "Asia", "UZ": "Asia",
    "GE": "Asia", "AM": "Asia", "AZ": "Asia", "MN": "Asia",
    "BN": "Asia", "MO": "Asia", "KG": "Asia", "TJ": "Asia",
    "TM": "Asia", "AF": "Asia", "BT": "Asia", "MV": "Asia",
    # Moyen-Orient
    "AE": "Middle East", "SA": "Middle East", "QA": "Middle East",
    "KW": "Middle East", "BH": "Middle East", "OM": "Middle East",
    "JO": "Middle East", "LB": "Middle East", "IL": "Middle East",
    "TR": "Middle East", "IR": "Middle East", "IQ": "Middle East",
    "SY": "Middle East", "YE": "Middle East", "PS": "Middle East",
    # Afrique
    "ZA": "Africa", "EG": "Africa", "NG": "Africa", "KE": "Africa",
    "MA": "Africa", "TN": "Africa", "GH": "Africa", "DZ": "Africa",
    "ET": "Africa", "UG": "Africa", "TZ": "Africa", "RW": "Africa",
    "SN": "Africa", "CI": "Africa", "CM": "Africa", "ZW": "Africa",
    "ZM": "Africa", "MU": "Africa", "MG": "Africa", "AO": "Africa",
    "MZ": "Africa", "BW": "Africa", "NA": "Africa", "MW": "Africa",
    "LY": "Africa", "SD": "Africa", "CD": "Africa", "BF": "Africa",
    "ML": "Africa", "NE": "Africa", "TD": "Africa", "SO": "Africa",
    "ER": "Africa", "DJ": "Africa", "GM": "Africa", "GN": "Africa",
    "SL": "Africa", "LR": "Africa", "TG": "Africa", "BJ": "Africa",
    "GA": "Africa", "CG": "Africa", "CF": "Africa", "BI": "Africa",
    "LS": "Africa", "SZ": "Africa", "SC": "Africa", "CV": "Africa",
    "MR": "Africa", "ST": "Africa", "GQ": "Africa", "KM": "Africa",
    # Océanie
    "AU": "Oceania", "NZ": "Oceania", "FJ": "Oceania", "PG": "Oceania",
    "NC": "Oceania", "PF": "Oceania", "WS": "Oceania", "TO": "Oceania",
    "VU": "Oceania", "SB": "Oceania", "GU": "Oceania",
    # Codes ajoutés après diagnostic des non-mappés (étape 22)
    "AS": "Oceania",       # American Samoa
    "JE": "Europe",        # Jersey
    "XK": "Europe",        # Kosovo (code non ISO, utilisé par le dataset)
}