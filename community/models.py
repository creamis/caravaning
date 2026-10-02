from django.conf import settings
from django.db import models
from django.utils import timezone


class Publication(models.Model):

    TYPES = [
        ("ROUTE", "Ruta"),
        ("VEHICLE", "Vehículo"),
        ("EXPERIENCE", "Experiencia"),
        ("EVENT", "Evento"),
    ]

    STATUS = [
        ("PENDING", "Pendiente de aprobación"),
        ("PUBLISHED", "Publicado"),
        ("REJECTED", "Rechazado"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="community_publications",
    )

    publication_type = models.CharField(
        max_length=20,
        choices=TYPES,
    )

    title = models.CharField(max_length=180)

    slug = models.SlugField(
        max_length=220,
        unique=True,
    )

    description = models.TextField()

    location = models.CharField(
        max_length=180,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="PENDING",
    )

    is_official = models.BooleanField(
        default=False,
        verbose_name="Publicación oficial",
    )

    # Identificador único para impedir envíos duplicados.
    # NULL permite conservar las publicaciones anteriores.
    submission_token = models.UUIDField(
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class PublicationImage(models.Model):

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="community/",
    )

    caption = models.CharField(
        max_length=200,
        blank=True,
    )


class PublicationLike(models.Model):

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["publication", "user"],
                name="unique_community_like",
            )
        ]


class PublicationComment(models.Model):

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    content = models.TextField()

    is_approved = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]


class CommunityEvent(models.Model):

    publication = models.OneToOneField(
        Publication,
        on_delete=models.CASCADE,
        related_name="event_details",
        limit_choices_to={
            "publication_type": "EVENT",
        },
    )

    starts_at = models.DateTimeField()

    ends_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    venue = models.CharField(
        max_length=200,
        blank=True,
    )

    capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Vacío si no hay límite de plazas.",
    )

    is_free = models.BooleanField(
        default=True,
    )

    registration_url = models.URLField(
        blank=True,
        help_text="Para eventos externos.",
    )


class EventRegistration(models.Model):

    event = models.ForeignKey(
        CommunityEvent,
        on_delete=models.CASCADE,
        related_name="registrations",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "user"],
                name="unique_community_registration",
            )
        ]
