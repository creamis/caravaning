from django.contrib import admin
from django.db.models import Count
from django.utils import timezone

from .models import (
    Publication,
    PublicationImage,
    PublicationLike,
    PublicationComment,
    CommunityEvent,
    EventRegistration,
)


class PublicationImageInline(admin.TabularInline):
    model = PublicationImage
    extra = 0


class CommunityEventInline(admin.StackedInline):
    model = CommunityEvent
    extra = 0
    max_num = 1
    fields = (
        "starts_at",
        "ends_at",
        "venue",
        "capacity",
        "is_free",
        "registration_url",
    )

    def get_extra(self, request, obj=None, **kwargs):
        return 0


@admin.action(description="Aprobar publicaciones seleccionadas")
def approve_publications(modeladmin, request, queryset):
    total = queryset.update(status="PUBLISHED")
    modeladmin.message_user(
        request,
        f"{total} publicaciones aprobadas."
    )


@admin.action(description="Dejar publicaciones pendientes")
def mark_pending(modeladmin, request, queryset):
    total = queryset.update(status="PENDING")
    modeladmin.message_user(
        request,
        f"{total} publicaciones pendientes de revisión."
    )


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "publication_type",
        "author",
        "status",
        "is_official",
        "total_likes",
        "total_comments",
        "created_at",
    )

    list_filter = (
        "publication_type",
        "status",
        "is_official",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "location",
        "author__username",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    list_select_related = ("author",)

    inlines = [PublicationImageInline]

    actions = [
        approve_publications,
        mark_pending,
    ]

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                likes_count=Count(
                    "likes",
                    distinct=True,
                ),
                comments_count=Count(
                    "comments",
                    distinct=True,
                ),
            )
        )

    @admin.display(
        description="Likes",
        ordering="likes_count",
    )
    def total_likes(self, obj):
        return obj.likes_count

    @admin.display(
        description="Comentarios",
        ordering="comments_count",
    )
    def total_comments(self, obj):
        return obj.comments_count

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user

        if obj.author_id == request.user.pk and request.user.is_staff:
            obj.is_official = True

        super().save_model(request, obj, form, change)


@admin.register(PublicationComment)
class PublicationCommentAdmin(admin.ModelAdmin):
    list_display = (
        "publication",
        "author",
        "is_approved",
        "created_at",
    )

    list_filter = (
        "is_approved",
        "created_at",
    )

    search_fields = (
        "content",
        "publication__title",
        "author__username",
    )

    actions = ["approve_comments"]

    @admin.action(description="Aprobar comentarios seleccionados")
    def approve_comments(self, request, queryset):
        total = queryset.update(is_approved=True)
        self.message_user(
            request,
            f"{total} comentarios aprobados."
        )


@admin.register(PublicationLike)
class PublicationLikeAdmin(admin.ModelAdmin):
    list_display = (
        "publication",
        "user",
        "created_at",
    )

    list_filter = ("created_at",)


@admin.register(CommunityEvent)
class CommunityEventAdmin(admin.ModelAdmin):
    list_display = (
        "publication",
        "starts_at",
        "venue",
        "capacity",
        "is_free",
    )

    list_filter = (
        "is_free",
        "starts_at",
    )

    search_fields = (
        "publication__title",
        "venue",
    )


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "user",
        "created_at",
    )

    search_fields = (
        "event__publication__title",
        "user__username",
    )
