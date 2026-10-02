"""
Fuentes de alojamiento para el motor de viajes de Caravaning Project.

No modifica modelos ni base de datos.

Prioridad:
1. Camping.co específico cuando conocemos y hemos comprobado el destino.
2. AlohaCamp cuando conocemos que es una alternativa adecuada.
3. Página interna de Campings como fallback seguro.
"""

from copy import deepcopy
from urllib.parse import urlencode, quote

from django.conf import settings


CAMPING_CO_AWIN_BASE = "https://www.awin1.com/cread.php"
CAMPING_CO_AWINMID = "13054"
CAMPING_CO_AFFILIATE_ID = "2917197"

CAMPING_CO_SPAIN = (
    "https://es.camping-and-co.com/vacaciones-camping-en-espana"
)


# Solo incluimos destinos que hemos comprobado realmente.
CAMPING_CO_DESTINATIONS = {
    "delta_ebro": {
        "aliases": [
            "delta del ebro",
            "deltebre",
            "sant jaume d'enveja",
        ],
        "title": "Campings en el Delta del Ebro",
        "subtitle": "Busca campings disponibles para completar tu escapada",
        "target_url": (
            "https://es.camping-and-co.com/"
            "camping-delta-de-l-ebre"
        ),
    },

    "cabo_gata": {
        "aliases": [
            "cabo de gata",
            "cabo de gata-nijar",
            "nijar",
        ],
        "title": "Campings en Cabo de Gata",
        "subtitle": "Busca una base junto al parque natural",
        "target_url": (
            "https://es.camping-and-co.com/"
            "camping-cabo-de-gata"
        ),
    },
}


# Destinos donde hemos comprobado que AlohaCamp
# ofrece una alternativa geográfica útil.
ALOHACAMP_DESTINATIONS = {
    "ordesa": {
        "aliases": [
            "ordesa",
            "monte perdido",
            "torla",
            "torla-ordesa",
        ],
        "title": "Alojamientos cerca de Ordesa",
        "subtitle": "Completa la ruta con una estancia en plena naturaleza",
    },
}


def _normalize(text):
    if not text:
        return ""

    import unicodedata

    text = str(text).lower().strip()

    return "".join(
        char
        for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )


def _destination_text(destination):
    return _normalize(
        f"{getattr(destination, 'title', '')} "
        f"{getattr(destination, 'location', '')}"
    )


def _matches_destination(destination, aliases):
    text = _destination_text(destination)

    return any(
        _normalize(alias) in text
        for alias in aliases
    )


def build_camping_co_affiliate_url(target_url, clickref):
    """
    Construye un deep link de Camping.co manteniendo
    el tracking de afiliado de Caravaning Project.
    """

    params = {
        "awinmid": CAMPING_CO_AWINMID,
        "awinaffid": CAMPING_CO_AFFILIATE_ID,
        "clickref": clickref,
        "ued": target_url,
    }

    return f"{CAMPING_CO_AWIN_BASE}?{urlencode(params, quote_via=quote)}"


def get_destination_image(destination):
    """
    Para una búsqueda de alojamientos usamos la imagen del DESTINO,
    nunca fingimos que es la fotografía de un camping concreto.
    """

    try:
        image = destination.get_image_url()
        if image:
            return image
    except Exception:
        pass

    return (
        "https://images.unsplash.com/"
        "photo-1504280390367-361c6d9f38f4"
        "?auto=format&fit=crop&w=900&q=80"
    )


def get_stay_for_destination(destination):
    """
    Devuelve la mejor fuente de alojamiento conocida.

    Nunca inventa un camping.
    """

    # ------------------------------------------------------------
    # 1. Camping.co específico comprobado
    # ------------------------------------------------------------

    for key, resource in CAMPING_CO_DESTINATIONS.items():

        if _matches_destination(destination, resource["aliases"]):

            return {
                "provider": "camping_co",
                "title": resource["title"],
                "subtitle": resource["subtitle"],
                "image": get_destination_image(destination),
                "url": build_camping_co_affiliate_url(
                    resource["target_url"],
                    f"trip_{key}",
                ),
                "url_name": None,
                "external": True,
                "specific": True,
            }

    # ------------------------------------------------------------
    # 2. AlohaCamp comprobado
    # ------------------------------------------------------------

    for key, resource in ALOHACAMP_DESTINATIONS.items():

        if _matches_destination(destination, resource["aliases"]):

            return {
                "provider": "alohacamp",
                "title": resource["title"],
                "subtitle": resource["subtitle"],
                "image": get_destination_image(destination),
                "url": settings.ALOHACAMP_AFFILIATE_URL,
                "url_name": None,
                "external": True,
                "specific": True,
            }

    # ------------------------------------------------------------
    # 3. Fallback interno seguro
    # ------------------------------------------------------------

    return {
        "provider": "caravaning_project",
        "title": f"Dónde dormir cerca de {destination.title.split(':')[0]}",
        "subtitle": "Explora opciones para completar tu ruta",
        "image": get_destination_image(destination),
        "url": None,
        "url_name": "camping",
        "external": False,
        "specific": False,
    }
