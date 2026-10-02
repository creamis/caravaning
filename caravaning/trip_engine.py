"""
Motor inteligente de escapadas de Caravaning Project - v2

Jerarquía de enriquecimiento:

    DESTINO ESPECÍFICO
            ↓
         REGIÓN
            ↓
     RECURSO GENERAL

Los Destination existentes siguen siendo la fuente de destinos.
Este archivo solo aporta conocimiento adicional.

No modifica modelos ni base de datos.
"""

import random
import unicodedata

from destinations.models import Destination
from caravaning.stay_sources import get_stay_for_destination
from caravaning.rental_sources import get_rental_for_destination


# ============================================================
# UTILIDADES
# ============================================================

def normalize(text):
    if not text:
        return ""

    text = str(text).lower().strip()

    return "".join(
        char for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )


def matches(text, aliases):
    text = normalize(text)

    return any(
        normalize(alias) in text
        for alias in aliases
    )


# ============================================================
# RECURSOS GENERALES
#
# Último fallback.
# Garantizan que cualquier Destination nuevo pueda participar.
# ============================================================

DEFAULT_RESOURCES = {

    "experience": {
        "title": "Experiencias durante tu viaje",
        "subtitle": "Descubre actividades para completar la escapada",
        "image": "/media/experiences/naturaleza-aventura.webp",
        "url": None,
        "pending": True,
    },

    "stay": {
        "title": "Dónde dormir durante la ruta",
        "subtitle": "Busca una parada para completar el viaje",
        "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
        "url_name": "camping",
    },

    "rental": {
        "title": "¿Necesitas una camper?",
        "subtitle": "Compara opciones de alquiler para empezar el viaje",
        "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
        "url_name": "listings:external_rentals",
    },
}


# ============================================================
# CONOCIMIENTO GEOGRÁFICO
#
# Esta capa reconoce automáticamente zonas a partir del título
# y location del Destination.
# No modifica Destination ni la base de datos.
# ============================================================

GEOGRAPHY = {

    "alicante": [
        "alicante",
        "torrevieja",
    ],

    "cadiz": [
        "cadiz",
        "tarifa",
        "bolonia",
    ],

    "leon": [
        "leon",
        "el bierzo",
        "bierzo",
        "las medulas",
    ],

    "lleida": [
        "lleida",
        "espot",
        "boi",
        "aiguestortes",
        "sant maurici",
    ],

    "galicia": [
        "galicia",
        "lugo",
        "ourense",
        "ribeira sacra",
    ],

    "caceres": [
        "caceres",
        "monfrague",
    ],

    "teruel": [
        "teruel",
        "albarracin",
    ],

    "castilla_la_mancha": [
        "castilla-la mancha",
        "castilla la mancha",
        "ciudad real",
        "toledo",
        "cabaneros",
    ],

    "huelva": [
        "huelva",
        "aracena",
        "picos de aroche",
    ],
}


def detect_geography(destination):
    """
    Reconoce una zona geográfica a partir de los datos
    que ya contiene Destination.
    """

    text = destination_text(destination)

    for area, aliases in GEOGRAPHY.items():
        if matches(text, aliases):
            return area

    return None



# ============================================================
# RECURSOS GEOGRÁFICOS
#
# Se utilizan cuando no existe conocimiento específico
# del destino ni una región enriquecida.
# ============================================================

GEOGRAPHY_RESOURCES = {

    "alicante": {
        "experience": {
            "title": "Experiencias en la Costa Blanca",
            "subtitle": "Mar, naturaleza y planes por Alicante",
            "image": "/media/experiences/actividades-acuaticas.webp",
            "url": None,
            "pending": True,
        },
        "stay": {
            "title": "Dónde dormir en Alicante",
            "subtitle": "Busca una parada para completar tu ruta",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },
        "rental": {
            "title": "Recorre Alicante en camper",
            "subtitle": "Busca vehículo para descubrir la Costa Blanca",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },

    "cadiz": {
        "experience": {
            "title": "Experiencias en Cádiz",
            "subtitle": "Costa, naturaleza y actividades junto al Atlántico",
            "image": "/media/experiences/actividades-acuaticas.webp",
            "url": None,
            "pending": True,
        },
        "stay": {
            "title": "Dónde dormir en Cádiz",
            "subtitle": "Prepara una parada cerca de la costa",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },
        "rental": {
            "title": "Descubre Cádiz en camper",
            "subtitle": "Recorre la costa gaditana sobre ruedas",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },

    "leon": {
        "experience": {
            "title": "Experiencias en León y El Bierzo",
            "subtitle": "Paisaje, historia y rutas en plena naturaleza",
            "image": "/media/experiences/naturaleza-aventura.webp",
            "url": None,
            "pending": True,
        },
        "stay": {
            "title": "Dónde dormir en El Bierzo",
            "subtitle": "Encuentra una base para explorar la zona",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },
        "rental": {
            "title": "El Bierzo en camper",
            "subtitle": "Prepara una ruta por León sobre ruedas",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },

    "lleida": {
        "experience": {
            "title": "Experiencias en el Pirineo de Lleida",
            "subtitle": "Lagos, senderismo y alta montaña",
            "image": "/media/experiences/naturaleza-aventura.webp",
            "url": None,
            "pending": True,
        },
        "stay": {
            "title": "Dónde dormir en el Pirineo de Lleida",
            "subtitle": "Busca una base para explorar la montaña",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },
        "rental": {
            "title": "Pirineo de Lleida en camper",
            "subtitle": "Recorre lagos y valles sobre ruedas",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },

    "galicia": {
        "experience": {
            "title": "Experiencias en Galicia",
            "subtitle": "Naturaleza, gastronomía y paisajes únicos",
            "image": "/media/experiences/naturaleza-aventura.webp",
            "url": None,
            "pending": True,
        },
        "stay": {
            "title": "Dónde dormir en Galicia",
            "subtitle": "Encuentra una parada para continuar tu ruta",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },
        "rental": {
            "title": "Descubre Galicia en camper",
            "subtitle": "Prepara una ruta entre costa e interior",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },

    "caceres": {
        "experience": {
            "title": "Experiencias en Cáceres",
            "subtitle": "Naturaleza, aves y paisajes de Extremadura",
            "image": "/media/experiences/naturaleza-aventura.webp",
            "url": None,
            "pending": True,
        },
        "stay": {
            "title": "Dónde dormir en Cáceres",
            "subtitle": "Busca una parada para explorar Extremadura",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },
        "rental": {
            "title": "Extremadura en camper",
            "subtitle": "Descubre Cáceres sobre ruedas",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },

    "teruel": {
        "experience": {
            "title": "Experiencias en la Sierra de Albarracín",
            "subtitle": "Pueblos, bosques y rutas por Teruel",
            "image": "/media/experiences/naturaleza-aventura.webp",
            "url": None,
            "pending": True,
        },
        "stay": {
            "title": "Dónde dormir en Teruel",
            "subtitle": "Busca una base para descubrir la sierra",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },
        "rental": {
            "title": "Descubre Teruel en camper",
            "subtitle": "Carreteras tranquilas, pueblos y naturaleza",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },

    "castilla_la_mancha": {
        "experience": {
            "title": "Experiencias en Castilla-La Mancha",
            "subtitle": "Naturaleza y rutas por el interior",
            "image": "/media/experiences/naturaleza-aventura.webp",
            "url": None,
            "pending": True,
        },
        "stay": {
            "title": "Dónde dormir en Castilla-La Mancha",
            "subtitle": "Encuentra una parada para continuar la ruta",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },
        "rental": {
            "title": "Castilla-La Mancha en camper",
            "subtitle": "Prepara una escapada por el interior",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },

    "huelva": {
        "experience": {
            "title": "Experiencias en la Sierra de Huelva",
            "subtitle": "Dehesas, senderos y pueblos blancos",
            "image": "/media/experiences/naturaleza-aventura.webp",
            "url": None,
            "pending": True,
        },
        "stay": {
            "title": "Dónde dormir en la Sierra de Huelva",
            "subtitle": "Busca una parada rodeada de naturaleza",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },
        "rental": {
            "title": "Sierra de Huelva en camper",
            "subtitle": "Recorre dehesas y pueblos sobre ruedas",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },
}


# ============================================================
# CONOCIMIENTO REGIONAL
# ============================================================

REGIONS = {

    "asturias": {
        "aliases": [
            "asturias",
            "cangas de onis",
            "somiedo",
        ],

        "experience": {
            "title": "Experiencias en Asturias",
            "subtitle": "Montaña, naturaleza y aventura",
            "image": "/media/experiences/naturaleza-aventura.webp",
            "url": None,
            "pending": True,
        },

        "stay": {
            "title": "Dónde dormir en Asturias",
            "subtitle": "Busca una parada para completar la ruta",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },

        "rental": {
            "title": "Recorre Asturias en camper",
            "subtitle": "Compara opciones de alquiler",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },


    "almeria": {
        "aliases": [
            "almeria",
            "cabo de gata",
            "nijar",
        ],

        "experience": {
            "title": "Experiencias en Cabo de Gata",
            "subtitle": "Mar, naturaleza y aventura",
            "image": "/media/experiences/actividades-acuaticas.webp",
            "url": None,
            "pending": True,
        },

        "stay": {
            "title": "Dónde dormir en Cabo de Gata",
            "subtitle": "Encuentra una parada para tu ruta",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },

        "rental": {
            "title": "Explora Almería en camper",
            "subtitle": "Busca vehículo para empezar la ruta",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },


    "navarra": {
        "aliases": [
            "navarra",
            "arguedas",
            "bardenas",
        ],

        "experience": {
            "title": "Experiencias en Navarra",
            "subtitle": "Paisajes, rutas y aventura",
            "image": "/media/experiences/naturaleza-aventura.webp",
            "url": None,
            "pending": True,
        },

        "stay": {
            "title": "Dónde dormir en Navarra",
            "subtitle": "Prepara una parada para la escapada",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },

        "rental": {
            "title": "Descubre Navarra en camper",
            "subtitle": "Compara opciones para tu viaje",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },


    "huesca": {
        "aliases": [
            "huesca",
            "torla",
            "ordesa",
        ],

        "experience": {
            "title": "Experiencias en el Pirineo",
            "subtitle": "Montaña, senderismo y naturaleza",
            "image": "/media/experiences/naturaleza-aventura.webp",
            "url": None,
            "pending": True,
        },

        "stay": {
            "title": "Dónde dormir cerca de Ordesa",
            "subtitle": "Busca una base para explorar la zona",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },

        "rental": {
            "title": "Pirineos sobre ruedas",
            "subtitle": "Busca una camper para tu ruta",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },


    "tarragona": {
        "aliases": [
            "tarragona",
            "deltebre",
            "delta del ebro",
            "sant jaume",
        ],

        "experience": {
            "title": "Experiencias en Tarragona",
            "subtitle": "Naturaleza, costa y actividades",
            "image": "/media/experiences/actividades-acuaticas.webp",
            "url": None,
            "pending": True,
        },

        "stay": {
            "title": "Dónde dormir en Tarragona",
            "subtitle": "Encuentra una parada para continuar la ruta",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },

        "rental": {
            "title": "Recorre Tarragona en camper",
            "subtitle": "Busca vehículo para tu escapada",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },


    "jaen": {
        "aliases": [
            "jaen",
            "cazorla",
        ],

        "experience": {
            "title": "Experiencias en Jaén",
            "subtitle": "Naturaleza, senderos y aventura",
            "image": "/media/experiences/naturaleza-aventura.webp",
            "url": None,
            "pending": True,
        },

        "stay": {
            "title": "Dónde dormir en Jaén",
            "subtitle": "Busca una parada entre naturaleza",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },

        "rental": {
            "title": "Descubre Jaén en camper",
            "subtitle": "Encuentra vehículo para comenzar la ruta",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },
}


# ============================================================
# CONOCIMIENTO ESPECÍFICO DE DESTINOS
#
# Solo añadimos aquí información cuando realmente la conocemos.
# No es obligatorio que un Destination aparezca aquí.
# ============================================================

DESTINATION_KNOWLEDGE = {

    "delta del ebro": {

        "aliases": [
            "delta del ebro",
            "deltebre",
        ],

        "experience": {
            "title": "Vive el Delta del Ebro",
            "subtitle": "Naturaleza y actividades junto al agua",
            "image": "/media/experiences/actividades-acuaticas.webp",
            "url": None,
            "pending": True,
        },

        "stay": {
            "title": "Dónde dormir en el Delta del Ebro",
            "subtitle": "Prepara tu base para explorar el Delta",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },

        "rental": {
            "title": "Recorre el Delta en camper",
            "subtitle": "Empieza aquí tu escapada sobre ruedas",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },


    "cabo de gata": {

        "aliases": [
            "cabo de gata",
            "cabo de gata-nijar",
        ],

        "experience": {
            "title": "Vive Cabo de Gata",
            "subtitle": "Calas, mar y naturaleza volcánica",
            "image": "/media/experiences/actividades-acuaticas.webp",
            "url": None,
            "pending": True,
        },

        "stay": {
            "title": "Dónde dormir en Cabo de Gata",
            "subtitle": "Prepara una parada junto al Mediterráneo",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },

        "rental": {
            "title": "Cabo de Gata en camper",
            "subtitle": "Empieza tu ruta por la costa de Almería",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },


    "ordesa": {

        "aliases": [
            "ordesa",
            "monte perdido",
        ],

        "experience": {
            "title": "Explora Ordesa y Monte Perdido",
            "subtitle": "Senderismo y alta montaña",
            "image": "/media/experiences/naturaleza-aventura.webp",
            "url": None,
            "pending": True,
        },

        "stay": {
            "title": "Dónde dormir cerca de Ordesa",
            "subtitle": "Una base para descubrir el Pirineo",
            "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=900&q=80",
            "url_name": "camping",
        },

        "rental": {
            "title": "Descubre Ordesa en camper",
            "subtitle": "Prepara tu ruta por el Pirineo",
            "image": "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=900&q=80",
            "url_name": "listings:external_rentals",
        },
    },
}


# ============================================================
# FERRIES
# ============================================================

FERRY_REGIONS = {
    "mallorca",
    "menorca",
    "ibiza",
    "formentera",
    "baleares",
    "cerdena",
    "corcega",
    "sicilia",
    "ceuta",
    "melilla",
    "canarias",
}


# ============================================================
# DETECCIÓN
# ============================================================

def destination_text(destination):
    return f"{destination.title} {destination.location}"


def detect_region(destination):
    text = destination_text(destination)

    for region_key, data in REGIONS.items():
        if matches(text, data.get("aliases", [])):
            return region_key

    return None


def detect_destination_knowledge(destination):
    text = destination_text(destination)

    for knowledge_key, data in DESTINATION_KNOWLEDGE.items():
        if matches(text, data.get("aliases", [])):
            return knowledge_key

    return None


def destination_needs_ferry(destination):
    text = normalize(destination_text(destination))

    return any(
        normalize(region) in text
        for region in FERRY_REGIONS
    )


# ============================================================
# RESOLUCIÓN DE RECURSOS
# ============================================================

def resolve_resource(
    resource_name,
    destination_data,
    region_data,
    geography_data,
):
    """
    Prioridad:

    1. Conocimiento específico del destino
    2. Conocimiento regional
    3. Conocimiento geográfico
    4. Recurso general
    """

    if destination_data and destination_data.get(resource_name):
        return {
            **destination_data[resource_name],
            "source": "destination",
        }

    if region_data and region_data.get(resource_name):
        return {
            **region_data[resource_name],
            "source": "region",
        }

    if geography_data and geography_data.get(resource_name):
        return {
            **geography_data[resource_name],
            "source": "geography",
        }

    return {
        **DEFAULT_RESOURCES[resource_name],
        "source": "default",
    }


# ============================================================
# CONSTRUCCIÓN DE VIAJES
# ============================================================

def build_trip(destination):

    region_key = detect_region(destination)
    geography_key = detect_geography(destination)
    knowledge_key = detect_destination_knowledge(destination)

    region_data = REGIONS.get(region_key, {})
    geography_data = GEOGRAPHY_RESOURCES.get(geography_key, {})
    destination_data = DESTINATION_KNOWLEDGE.get(
        knowledge_key,
        {}
    )

    experience = resolve_resource(
        "experience",
        destination_data,
        region_data,
        geography_data,
    )

    stay = get_stay_for_destination(destination)

    # Adaptamos la fuente externa al sistema de enriquecimiento
    # que ya utiliza el motor para calcular la puntuación.
    if stay.get("specific"):
        stay["source"] = "destination"
    else:
        stay["source"] = "default"

    rental = get_rental_for_destination(destination)

    # RentalSource indica si conocemos una relación geográfica
    # específica o si estamos usando CamperDays España.
    if rental.get("specific"):
        rental["source"] = "destination"
    else:
        rental["source"] = "default"

    return {
        "destination": destination,

        "region": region_key,
        "geography": geography_key,
        "knowledge": knowledge_key,

        "experience": experience,
        "stay": stay,
        "rental": rental,

        "ferry_available": destination_needs_ferry(destination),

        "enrichment": {
            "experience": experience["source"],
            "stay": stay["source"],
            "rental": rental["source"],
        },
    }


def get_available_trips():
    """
    TODOS los Destination existentes entran automáticamente.
    """

    return [
        build_trip(destination)
        for destination in Destination.objects.all()
    ]


def trip_score(trip):
    """
    Puntúa la riqueza de la escapada.

    No decide qué destino es mejor.
    Solo mide cuánta información tenemos sobre él.
    """

    points = {
        "destination": 4,
        "region": 3,
        "geography": 2,
        "default": 1,
    }

    enrichment = trip["enrichment"]

    return sum(
        points.get(enrichment[key], 0)
        for key in ("experience", "stay", "rental")
    )


def get_suggested_trip():
    """
    Selección ponderada.

    Todos los destinos pueden aparecer, pero aquellos con
    información más específica tienen mayor probabilidad.
    """

    trips = get_available_trips()

    if not trips:
        return None

    weights = [
        max(trip_score(trip), 1)
        for trip in trips
    ]

    return random.choices(
        trips,
        weights=weights,
        k=1,
    )[0]


# ============================================================
# DIAGNÓSTICO
# ============================================================

def engine_stats():

    trips = get_available_trips()

    destination_level = 0
    region_level = 0
    default_level = 0

    for trip in trips:

        sources = set(trip["enrichment"].values())

        if "destination" in sources:
            destination_level += 1

        elif "region" in sources:
            region_level += 1

        else:
            default_level += 1

    return {
        "destinations": len(trips),
        "destination_level": destination_level,
        "region_level": region_level,
        "default_level": default_level,
    }
