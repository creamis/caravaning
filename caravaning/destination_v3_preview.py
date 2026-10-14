"""Laboratorio aislado Destination V3.

No altera la vista Destination V2 ni las fichas públicas.
La URL se incorporará solo después de sincronizar el código de PythonAnywhere.
"""
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from destinations.models import Destination


def destino_v3_preview(request, destino_slug="torrevieja"):
    destination_ids = {"torrevieja": 22}
    destination_id = destination_ids.get(destino_slug)
    if destination_id is None:
        raise Http404("Destino no disponible en V3")

    destination = get_object_or_404(
        Destination,
        pk=destination_id,
        place_type=Destination.TYPE_DESTINATION,
    )
    response = render(
        request,
        "preview/destino_v3.html",
        {"destination": destination},
    )
    response["X-Robots-Tag"] = "noindex, nofollow"
    return response
