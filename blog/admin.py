from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, PostImage, Comment


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "product_count",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "title",
        "content",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    filter_horizontal = ("shop_products",)

    inlines = [PostImageInline]

    readonly_fields = ("product_links",)

    def get_fields(self, request, obj=None):
        fields = [
            "title",
            "slug",
            "author",
            "content",
            "meta_description",
            "status",
            "shop_products",
        ]

        if obj:
            fields.append("product_links")

        return fields

    @admin.display(description="Productos")
    def product_count(self, obj):
        return obj.shop_products.count()

    @admin.display(description="Editar productos relacionados")
    def product_links(self, obj):
        if not obj.pk:
            return "Guarda primero el artículo."

        products = obj.shop_products.select_related(
            "category"
        ).order_by("name")

        if not products.exists():
            return "Este artículo todavía no tiene productos relacionados."

        links = []

        for product in products:
            url = reverse(
                "admin:shop_product_change",
                args=[product.pk],
            )

            estado = (
                "Publicado"
                if product.is_active
                else "Borrador"
            )

            links.append(
                format_html(
                    '<p><a href="{}" target="_blank">'
                    '{} · {}</a> ({})</p>',
                    url,
                    product.pk,
                    product.name,
                    estado,
                )
            )

        return format_html(
            "{}",
            format_html("").join(links),
        )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "author",
        "created_at",
    )

    search_fields = (
        "content",
        "post__title",
    )
