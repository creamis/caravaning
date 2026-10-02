"""
RentalSource para el motor inteligente de Caravaning Project.

No modifica modelos ni base de datos.

Selecciona una página REAL y verificada de CamperDays cuando existe
una relación geográfica clara con el destino.

Si no existe una relación suficientemente buena, utiliza CamperDays España.
"""

import unicodedata
from urllib.parse import urlencode, quote


CAMPERDAYS_AWIN_BASE = "https://www.awin1.com/cread.php"
CAMPERDAYS_AWINMID = "52113"
CAMPERDAYS_AFFILIATE_ID = "2917197"

CAMPERDAYS_BASE = "https://www.camperdays.es/autocaravana-espana"


def normalize(text):
    if not text:
        return ""

    text = str(text).lower().strip()

    return "".join(
        char
        for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )


def destination_text(destination):
    return normalize(
        f"{getattr(destination, 'title', '')} "
        f"{getattr(destination, 'location', '')}"
    )


def matches(destination, aliases):
    text = destination_text(destination)

    return any(
        normalize(alias) in text
        for alias in aliases
    )


def build_camperdays_url(target_url, clickref):
    params = {
        "awinmid": CAMPERDAYS_AWINMID,
        "awinaffid": CAMPERDAYS_AFFILIATE_ID,
        "clickref": clickref,
        "ued": target_url,
    }

    return (
        f"{CAMPERDAYS_AWIN_BASE}?"
        f"{urlencode(params, quote_via=quote)}"
    )


CAMPERDAYS_PAGES = {

    "lleida": {
        "url": f"{CAMPERDAYS_BASE}/lleida.html",
        "label": "Lleida",
    },

    "norte_espana": {
        "url": f"{CAMPERDAYS_BASE}/norte-de-espana.html",
        "label": "Norte de España",
        "type": "region",
    },

    "andalucia": {
        "url": f"{CAMPERDAYS_BASE}/andaluca.html",
        "label": "Andalucía",
        "type": "region",
    },

    "torrevieja": {
        "url": f"{CAMPERDAYS_BASE}/torrevieja.html",
        "label": "Torrevieja",
    },

    "alicante": {
        "url": f"{CAMPERDAYS_BASE}/alicante.html",
        "label": "Alicante",
    },

    "valencia": {
        "url": f"{CAMPERDAYS_BASE}/valencia.html",
        "label": "Valencia",
    },

    "tarragona": {
        "url": f"{CAMPERDAYS_BASE}/tarragona.html",
        "label": "Tarragona",
    },

    "a_coruna": {
        "url": f"{CAMPERDAYS_BASE}/a-coruna.html",
        "label": "A Coruña",
    },

    "malaga": {
        "url": f"{CAMPERDAYS_BASE}/malaga.html",
        "label": "Málaga",
    },

    "sevilla": {
        "url": f"{CAMPERDAYS_BASE}/sevilla.html",
        "label": "Sevilla",
    },

    "madrid": {
        "url": f"{CAMPERDAYS_BASE}/madrid.html",
        "label": "Madrid",
    },

    "barcelona": {
        "url": f"{CAMPERDAYS_BASE}/barcelona.html",
        "label": "Barcelona",
    },

    "bilbao": {
        "url": f"{CAMPERDAYS_BASE}/bilbao.html",
        "label": "Bilbao",
    },
}


# Relaciones que consideramos suficientemente claras.
#
# IMPORTANTE:
# No pretendemos encontrar simplemente "la ciudad más cercana".
# Seleccionamos una base de alquiler razonable para comenzar la ruta.

DESTINATION_RENTAL_MAP = [

    {
        "key": "aiguestortes",
        "aliases": [
            "aiguestortes",
            "estany de sant maurici",
            "espot",
            "boi",
            "lleida",
        ],
        "page": "lleida",
    },

    {
        "key": "ordesa",
        "aliases": [
            "ordesa",
            "monte perdido",
            "torla",
        ],
        "page": "norte_espana",
    },

    {
        "key": "covadonga",
        "aliases": [
            "covadonga",
            "cangas de onis",
        ],
        "page": "norte_espana",
    },

    {
        "key": "somiedo",
        "aliases": [
            "somiedo",
        ],
        "page": "norte_espana",
    },

    {
        "key": "cabo_gata",
        "aliases": [
            "cabo de gata",
            "nijar",
            "almeria",
        ],
        "page": "andalucia",
    },

    {
        "key": "torrevieja",
        "aliases": [
            "torrevieja",
            "camper park torrevieja",
        ],
        "page": "torrevieja",
    },

    {
        "key": "delta_ebro",
        "aliases": [
            "delta del ebro",
            "deltebre",
            "sant jaume",
            "tarragona",
        ],
        "page": "tarragona",
    },

    {
        "key": "ribeira_sacra",
        "aliases": [
            "ribeira sacra",
            "lugo",
            "ourense",
        ],
        "page": "a_coruna",
    },
]


def get_destination_image(destination):
    try:
        image = destination.get_image_url()

        if image:
            return image

    except Exception:
        pass

    return (
        "https://images.unsplash.com/"
        "photo-1523987355523-c7b5b0dd90a7"
        "?auto=format&fit=crop&w=900&q=80"
    )


def specific_rental(destination, relation):
    page = CAMPERDAYS_PAGES[relation["page"]]

    short_title = destination.title.split(":")[0]

    if page.get("type") == "region":
        subtitle = (
            f"Encuentra una camper para recorrer {page['label']}"
        )
        pickup_area = None
        route_area = page["label"]
    else:
        subtitle = (
            f"Busca tu camper con recogida desde {page['label']}"
        )
        pickup_area = page["label"]
        route_area = None

    return {
        "provider": "camperdays",
        "title": f"Recorre {short_title} en camper",
        "subtitle": subtitle,
        "image": get_destination_image(destination),
        "url": build_camperdays_url(
            page["url"],
            f"trip_{relation['key']}",
        ),
        "url_name": None,
        "external": True,
        "specific": True,
        "pickup_area": pickup_area,
        "route_area": route_area,
        "source": "destination",
    }


def generic_rental(destination):
    short_title = destination.title.split(":")[0]

    target_url = f"{CAMPERDAYS_BASE}.html"

    return {
        "provider": "camperdays",
        "title": f"Recorre {short_title} en camper",
        "subtitle": "Busca una camper para comenzar tu aventura",
        "image": get_destination_image(destination),
        "url": build_camperdays_url(
            target_url,
            f"trip_spain_{destination.pk}",
        ),
        "url_name": None,
        "external": True,
        "specific": False,
        "pickup_area": None,
        "source": "default",
    }


def get_rental_for_destination(destination):

    for relation in DESTINATION_RENTAL_MAP:

        if matches(destination, relation["aliases"]):
            return specific_rental(destination, relation)

    return generic_rental(destination)
