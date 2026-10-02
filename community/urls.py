from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
    path(
        "mis-eventos/",
        views.my_events,
        name="my_events",
    ),

    path(
        "mis-eventos/<slug:slug>/participantes/",
        views.event_participants,
        name="event_participants",
    ),

    path(
        "mis-inscripciones/",
        views.my_registrations,
        name="my_registrations",
    ),

    path(
        "eventos/proponer/",
        views.event_create,
        name="event_create",
    ),
    path(
        "eventos/<slug:slug>/",
        views.event_detail,
        name="event_detail",
    ),
    path(
        "eventos/<slug:slug>/apuntarme/",
        views.event_register,
        name="event_register",
    ),
    path(
        "eventos/<slug:slug>/cancelar/",
        views.event_unregister,
        name="event_unregister",
    ),

    path(
        "publicar/",
        views.publication_create,
        name="create",
    ),
    path(
        "mis-publicaciones/",
        views.my_publications,
        name="my_publications",
    ),

    path(
        "",
        views.community_home,
        name="home",
    ),
    path(
        "publicacion/<slug:slug>/eliminar/",
        views.publication_delete,
        name="delete",
    ),
    path(
        "publicacion/<slug:slug>/editar/",
        views.publication_edit,
        name="edit",
    ),
    path(
        "publicacion/<slug:slug>/",
        views.publication_detail,
        name="detail",
    ),
    path(
        "publicacion/<slug:slug>/like/",
        views.publication_like,
        name="like",
    ),
    path(
        "publicacion/<slug:slug>/comentar/",
        views.publication_comment,
        name="comment",
    ),
    path(
        "<slug:category>/",
        views.community_category,
        name="category",
    ),
]
