from datetime import datetime as _community_datetime, time as _community_time
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Prefetch
from django.shortcuts import render
from django.utils import timezone

from .models import (
    Publication,
    PublicationImage,
    CommunityEvent,
)


def community_home(request):
    publicaciones = (
        Publication.objects
        .filter(status="PUBLISHED")
        .select_related("author")
        .prefetch_related(
            Prefetch(
                "images",
                queryset=PublicationImage.objects.order_by("pk"),
            )
        )
        .annotate(
            total_likes=Count("likes", distinct=True),
            total_comments=Count(
                "comments",
                filter=__import__(
                    "django.db.models",
                    fromlist=["Q"]
                ).Q(comments__is_approved=True),
                distinct=True,
            ),
        )
    )

    populares = publicaciones.order_by(
        "-total_likes",
        "-created_at",
    )[:6]

    recientes = publicaciones.order_by(
        "-created_at",
    )[:6]

    proximos_eventos = (
        CommunityEvent.objects
        .filter(
            publication__status="PUBLISHED",
            starts_at__gte=timezone.now(),
        )
        .select_related(
            "publication",
            "publication__author",
        )
        .order_by("starts_at")[:4]
    )

    return render(
        request,
        "community/home.html",
        {
            "populares": populares,
            "recientes": recientes,
            "proximos_eventos": proximos_eventos,
        },
    )


def community_category(request, category):
    from django.db.models import Q
    from django.http import Http404

    categories = {
        "rutas": ("ROUTE", "Rutas favoritas"),
        "vehiculos": ("VEHICLE", "Nuestros vehículos"),
        "experiencias": ("EXPERIENCE", "Experiencias viajeras"),
        "eventos": ("EVENT", "Eventos y quedadas"),
    }

    if category not in categories:
        raise Http404("Categoría no encontrada")

    category_code, category_title = categories[category]

    publications = (
        Publication.objects
        .filter(
            status="PUBLISHED",
            publication_type=category_code,
        )
        .select_related("author")
        .prefetch_related("images")
        .annotate(
            total_likes=Count("likes", distinct=True),
            total_comments=Count(
                "comments",
                filter=Q(comments__is_approved=True),
                distinct=True,
            ),
        )
    )

    if category_code == "EVENT":
        publications = publications.select_related(
            "event_details"
        ).prefetch_related(
            "event_details__registrations"
        )

    order = request.GET.get("orden", "populares")

    if order == "recientes":
        publications = publications.order_by(
            "-created_at"
        )
    else:
        order = "populares"
        publications = publications.order_by(
            "-total_likes",
            "-created_at",
        )

    return render(
        request,
        "community/category.html",
        {
            "publications": publications,
            "category": category,
            "category_title": category_title,
            "current_order": order,
            "now": timezone.now(),
        },
    )


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import PublicationLike, PublicationComment


def publication_detail(request, slug):
    publication = get_object_or_404(
        Publication.objects
        .select_related("author")
        .prefetch_related("images")
        .annotate(
            total_likes=Count("likes", distinct=True),
            total_comments=Count(
                "comments",
                filter=Q(comments__is_approved=True),
                distinct=True,
            ),
        ),
        slug=slug,
        status="PUBLISHED",
    )

    comments = (
        publication.comments
        .filter(is_approved=True)
        .select_related("author")
        .order_by("-created_at")
    )

    has_liked = False

    if request.user.is_authenticated:
        has_liked = publication.likes.filter(
            user=request.user
        ).exists()

    return render(
        request,
        "community/detail.html",
        {
            "publication": publication,
            "comments": comments,
            "has_liked": has_liked,
        },
    )



# community_ajax_v1

@login_required
@require_POST
def publication_like(request, slug):
    from django.http import JsonResponse

    publication = get_object_or_404(
        Publication,
        slug=slug,
        status="PUBLISHED",
    )

    with transaction.atomic():
        like, created = PublicationLike.objects.get_or_create(
            publication=publication,
            user=request.user,
        )

        if not created:
            like.delete()

        liked = created

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "liked": liked,
            "count": publication.likes.count(),
        })

    return redirect(
        "community:detail",
        slug=publication.slug,
    )


@login_required
@require_POST
def publication_comment(request, slug):
    from django.http import JsonResponse

    publication = get_object_or_404(
        Publication,
        slug=slug,
        status="PUBLISHED",
    )

    content = request.POST.get("content", "").strip()
    ajax = (
        request.headers.get("X-Requested-With")
        == "XMLHttpRequest"
    )

    if not content:
        message = "Escribe un comentario antes de enviarlo."
        success = False

    elif len(content) > 2000:
        message = (
            "El comentario no puede superar "
            "los 2000 caracteres."
        )
        success = False

    else:
        PublicationComment.objects.create(
            publication=publication,
            author=request.user,
            content=content,
            is_approved=False,
        )

        message = (
            "¡Comentario recibido! Está pendiente "
            "de aprobación y aparecerá cuando "
            "lo revisemos."
        )
        success = True

    if ajax:
        return JsonResponse(
            {
                "success": success,
                "message": message,
            },
            status=200 if success else 400,
        )

    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)

    return redirect(
        "community:detail",
        slug=publication.slug,
    )


from io import BytesIO
from uuid import uuid4

from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.utils.text import slugify
from PIL import Image, ImageOps

from .forms import PublicationForm


def optimize_community_image(uploaded_file):
    uploaded_file.seek(0)

    with Image.open(uploaded_file) as original:
        image = ImageOps.exif_transpose(original)
        image.thumbnail((1600, 1600))

        if image.mode != "RGB":
            if "A" in image.getbands():
                background = Image.new(
                    "RGB",
                    image.size,
                    (255, 255, 255),
                )
                background.paste(
                    image,
                    mask=image.getchannel("A"),
                )
                image = background
            else:
                image = image.convert("RGB")

        output = BytesIO()

        image.save(
            output,
            format="WEBP",
            quality=82,
            method=6,
        )

        output.seek(0)

        return ContentFile(output.read())


# community-submission-token-v1
def community_submission_token(request):
    """Devuelve el UUID del envío o None si no es válido."""
    from uuid import UUID

    try:
        return UUID(request.POST.get("submission_token", ""))
    except (ValueError, TypeError, AttributeError):
        return None


@login_required
def publication_create(request):

    # Máximo de tres publicaciones diarias para usuarios normales.
    LIMITE_DIARIO_COMUNIDAD = 3

    if request.method == "POST" and not request.user.is_staff:
        from datetime import timedelta

        desde = timezone.now() - timedelta(hours=24)

        publicaciones_recientes = Publication.objects.filter(
            author=request.user,
            created_at__gte=desde,
        ).count()

        if publicaciones_recientes >= LIMITE_DIARIO_COMUNIDAD:
            messages.error(
                request,
                "Has alcanzado el límite de 3 publicaciones "
                "en 24 horas. Podrás compartir otra aventura "
                "cuando haya transcurrido ese plazo.",
            )

            return redirect("community:my_publications")

    if request.method == "POST":
        token = community_submission_token(request)

        if token is None:
            messages.error(
                request,
                "El formulario ha caducado. Vuelve a enviarlo.",
            )
            return redirect("community:create")

        if Publication.objects.filter(
            submission_token=token,
            author=request.user,
        ).exists():
            messages.info(
                request,
                "Esta publicación ya se había recibido.",
            )
            return redirect("community:my_publications")

        form = PublicationForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            publication = form.save(commit=False)

            publication.author = request.user
            publication.status = "PENDING"
            publication.is_official = False

            base_slug = slugify(publication.title)[:170]
            publication.slug = (
                f"{base_slug}-{uuid4().hex[:12]}"
            )

            images = form.cleaned_data["images"]

            with transaction.atomic():

                publication, created = Publication.objects.get_or_create(
                    submission_token=token,
                    defaults={
                        "author": request.user,
                        "publication_type": publication.publication_type,
                        "title": publication.title,
                        "slug": publication.slug,
                        "description": publication.description,
                        "location": publication.location,
                        "status": "PENDING",
                        "is_official": False,
                    },
                )

                if not created:
                    messages.info(
                        request,
                        "Esta publicación ya se había recibido.",
                    )
                    return redirect("community:my_publications")

                for uploaded_file in images:

                    optimized = optimize_community_image(
                        uploaded_file
                    )

                    photo = PublicationImage(
                        publication=publication
                    )

                    photo.image.save(
                        f"{uuid4().hex}.webp",
                        optimized,
                        save=True,
                    )

            messages.success(
                request,
                "¡Tu aventura se ha enviado! "
                "La revisaremos antes de publicarla.",
            )

            return redirect(
                "community:my_publications"
            )

    else:
        form = PublicationForm()

    return render(
        request,
        "community/create.html",
        {
            "form": form,
            "submission_token": (
                request.POST.get("submission_token", "")
                if request.method == "POST"
                else str(uuid4())
            ),
        },
    )


@login_required
def my_publications(request):

    publications = (
        Publication.objects
        .filter(author=request.user)
        .order_by("-created_at")
    )

    return render(
        request,
        "community/my_publications.html",
        {"publications": publications},
    )


# EVENTOS Y QUEDADAS

from django.db import DatabaseError
from django.views.decorators.http import require_POST

from .event_forms import EventProposalForm
from .models import CommunityEvent, EventRegistration


@login_required
def event_create(request):
    if request.method == "POST":
        token = community_submission_token(request)

        if token is None:
            messages.error(
                request,
                "El formulario ha caducado. Vuelve a enviarlo.",
            )
            return redirect("community:event_create")

        if Publication.objects.filter(
            submission_token=token,
            author=request.user,
        ).exists():
            messages.info(
                request,
                "Esta quedada ya se había recibido.",
            )
            return redirect("community:my_publications")

        form = EventProposalForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data

            publication = Publication(
                author=request.user,
                publication_type="EVENT",
                title=data["title"],
                description=data["description"],
                location=data["location"],
                status="PENDING",
                is_official=False,
                slug=(
                    f"{slugify(data['title'])[:170]}"
                    f"-{uuid4().hex[:12]}"
                ),
            )

            with transaction.atomic():
                publication, created = Publication.objects.get_or_create(
                    submission_token=token,
                    defaults={
                        "author": request.user,
                        "publication_type": "EVENT",
                        "title": publication.title,
                        "slug": publication.slug,
                        "description": publication.description,
                        "location": publication.location,
                        "status": "PENDING",
                        "is_official": False,
                    },
                )

                if not created:
                    messages.info(
                        request,
                        "Esta quedada ya se había recibido.",
                    )
                    return redirect("community:my_publications")

                CommunityEvent.objects.create(
                    publication=publication,
                    starts_at=timezone.make_aware(
                        _community_datetime.combine(
                            data["starts_at"],
                            data["start_time"],
                        ),
                        timezone.get_current_timezone(),
                    ),
                    capacity=data["capacity"],
                    is_free=True,
                )

                optimized = optimize_community_image(
                    data["cover_image"]
                )

                photo = PublicationImage(
                    publication=publication
                )

                photo.image.save(
                    f"{uuid4().hex}.webp",
                    optimized,
                    save=True,
                )

            messages.success(
                request,
                "Tu evento se ha enviado correctamente. "
                "Lo revisaremos antes de publicarlo.",
            )

            return redirect("community:my_publications")
    else:
        form = EventProposalForm()

    return render(
        request,
        "community/event_create.html",
        {
            "form": form,
            "submission_token": (
                request.POST.get("submission_token", "")
                if request.method == "POST"
                else str(uuid4())
            ),
        },
    )


def event_detail(request, slug):
    event = get_object_or_404(
        CommunityEvent.objects.select_related(
            "publication",
            "publication__author",
        ),
        publication__slug=slug,
        publication__status="PUBLISHED",
    )

    registered_count = event.registrations.count()

    is_registered = False

    if request.user.is_authenticated:
        is_registered = event.registrations.filter(
            user=request.user
        ).exists()

    registration_open = event.starts_at > timezone.now()

    if event.capacity is not None:
        registration_open = (
            registration_open
            and registered_count < event.capacity
        )

    return render(
        request,
        "community/event_detail.html",
        {
            "event": event,
            "registered_count": registered_count,
            "is_registered": is_registered,
            "registration_open": registration_open,
        },
    )


@login_required
@require_POST
def event_register(request, slug):
    event = get_object_or_404(
        CommunityEvent,
        publication__slug=slug,
        publication__status="PUBLISHED",
    )

    try:
        with transaction.atomic():
            # Bloqueo de fila en bases de datos compatibles.
            event = CommunityEvent.objects.select_for_update().get(
                pk=event.pk
            )

            if event.starts_at <= timezone.now():
                messages.error(
                    request,
                    "Las inscripciones ya están cerradas.",
                )

            elif event.registrations.filter(
                user=request.user
            ).exists():
                messages.info(
                    request,
                    "Ya estás inscrito en este evento.",
                )

            elif (
                event.capacity is not None
                and event.registrations.count() >= event.capacity
            ):
                messages.error(
                    request,
                    "Lo sentimos, no quedan plazas disponibles.",
                )

            else:
                EventRegistration.objects.create(
                    event=event,
                    user=request.user,
                )

                messages.success(
                    request,
                    "¡Te has apuntado a la quedada!",
                )

    except DatabaseError:
        messages.error(
            request,
            "No se ha podido completar la inscripción. "
            "Inténtalo de nuevo.",
        )

    return redirect(
        "community:event_detail",
        slug=slug,
    )


@login_required
@require_POST
def event_unregister(request, slug):
    event = get_object_or_404(
        CommunityEvent,
        publication__slug=slug,
        publication__status="PUBLISHED",
    )

    deleted, _ = EventRegistration.objects.filter(
        event=event,
        user=request.user,
    ).delete()

    if deleted:
        messages.success(
            request,
            "Tu inscripción se ha cancelado.",
        )

    if request.POST.get("next") == "my_registrations":
        return redirect("community:my_registrations")

    return redirect(
        "community:event_detail",
        slug=slug,
    )


@login_required
def my_registrations(request):
    registrations = (
        EventRegistration.objects
        .filter(
            user=request.user,
            event__publication__status="PUBLISHED",
        )
        .select_related(
            "event",
            "event__publication",
        )
        .prefetch_related(
            "event__publication__images",
        )
        .order_by("-event__starts_at")
    )

    return render(
        request,
        "community/my_registrations.html",
        {
            "registrations": registrations,
            "now": timezone.now(),
        },
    )


@login_required
def my_events(request):
    events = (
        CommunityEvent.objects
        .filter(publication__author=request.user)
        .select_related("publication")
        .prefetch_related("publication__images")
        .annotate(
            registered_count=Count("registrations")
        )
        .order_by("-starts_at")
    )

    return render(
        request,
        "community/my_events.html",
        {"events": events},
    )


@login_required
def event_participants(request, slug):
    event = get_object_or_404(
        CommunityEvent.objects.select_related("publication"),
        publication__slug=slug,
    )

    if (
        event.publication.author_id != request.user.pk
        and not request.user.is_staff
    ):
        raise PermissionDenied

    registrations = (
        event.registrations
        .select_related("user")
        .order_by("created_at")
    )

    return render(
        request,
        "community/event_participants.html",
        {
            "event": event,
            "registrations": registrations,
            "registered_count": registrations.count(),
        },
    )


# community-edit-publication-v1
@login_required
def publication_edit(request, slug):
    from django.shortcuts import get_object_or_404
    from django.views.decorators.http import require_http_methods

    publication = get_object_or_404(
        Publication,
        slug=slug,
        publication_type__in=[
            "ROUTE",
            "VEHICLE",
            "EXPERIENCE",
        ],
    )

    if (
        publication.author_id != request.user.pk
        and not request.user.is_superuser
    ):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    if request.method == "POST":
        form = PublicationForm(
            request.POST,
            request.FILES,
            instance=publication,
        )

        if form.is_valid():
            new_images = form.cleaned_data["images"]

            # Fotografías que el usuario ha marcado para eliminar.
            submitted_ids = request.POST.getlist("delete_images")

            try:
                selected_ids = {int(value) for value in submitted_ids}
            except (TypeError, ValueError):
                selected_ids = set()
                form.add_error(
                    None,
                    "La selección de fotografías no es válida.",
                )

            existing_photos = list(publication.images.all())
            existing_ids = {photo.pk for photo in existing_photos}

            if not selected_ids.issubset(existing_ids):
                form.add_error(
                    None,
                    "Una de las fotografías seleccionadas "
                    "no pertenece a esta publicación.",
                )

            remaining_count = (
                len(existing_photos) - len(selected_ids)
            )

            if remaining_count + len(new_images) > 10:
                form.add_error(
                    "images",
                    "Puedes tener un máximo de 10 fotografías. "
                    f"Conservas {remaining_count} y estás "
                    f"intentando añadir {len(new_images)}.",
                )

            if not form.errors:
                # Preparar las imágenes antes de modificar
                # la publicación o eliminar fotografías.
                optimized_images = [
                    optimize_community_image(uploaded_file)
                    for uploaded_file in new_images
                ]

                with transaction.atomic():
                    updated = form.save(commit=False)

                    updated.status = "PENDING"
                    updated.is_official = False
                    updated.save()

                    photos_to_delete = [
                        photo for photo in existing_photos
                        if photo.pk in selected_ids
                    ]

                    # Eliminar los registros seleccionados.
                    for photo in photos_to_delete:
                        photo.delete()

                    # Incorporar las nuevas fotografías.
                    for optimized in optimized_images:
                        photo = PublicationImage(
                            publication=updated
                        )

                        photo.image.save(
                            f"{uuid4().hex}.webp",
                            optimized,
                            save=True,
                        )

                    # Borrar los archivos originales solamente
                    # después de confirmar la transacción.
                    for photo in photos_to_delete:
                        storage = photo.image.storage
                        filename = photo.image.name

                        transaction.on_commit(
                            lambda s=storage, n=filename: s.delete(n)
                        )

                messages.success(
                    request,
                    "Publicación actualizada. "
                    "Volverá a revisarse antes de publicarla.",
                )

                return redirect(
                    "community:my_publications"
                )
    else:
        form = PublicationForm(instance=publication)

    return render(
        request,
        "community/edit.html",
        {
            "form": form,
            "publication": publication,
            "selected_image_ids": (
                selected_ids
                if request.method == "POST" and form.is_bound
                else set()
            ),
        },
    )


# community-delete-publication-v1
@login_required
@require_POST
def publication_delete(request, slug):
    from django.shortcuts import get_object_or_404
    from django.http import JsonResponse

    publication = get_object_or_404(
        Publication,
        slug=slug,
        publication_type__in=[
            "ROUTE",
            "VEHICLE",
            "EXPERIENCE",
        ],
    )

    if (
        publication.author_id != request.user.pk
        and not request.user.is_superuser
    ):
        return JsonResponse(
            {"error": "No tienes permiso para eliminar esta publicación."},
            status=403,
        )

    title = publication.title

    # Conservamos los archivos físicos por ahora.
    # Django elimina la publicación y sus relaciones.
    with transaction.atomic():
        publication.delete()

    return JsonResponse({
        "success": True,
        "message": f'Se ha eliminado "{title}".',
    })
