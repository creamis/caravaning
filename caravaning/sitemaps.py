from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post
from destinations.models import Destination
from listings.models import Listing


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return [
            "home",
            "blog:post_list",
            "listings:listing_list",
            "listings:external_rentals",
            "destinations:destination_list",
            "shop:product_list",
            "pages:about",
            "pages:contact",
            "pages:legal",
            "pages:privacy",
            "pages:cookies",
            "pages:affiliates",
        ]

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).order_by("-updated_at")

    def lastmod(self, obj):
        return obj.updated_at


class ListingSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Listing.objects.filter(is_available=True).order_by("-updated_at")

    def lastmod(self, obj):
        return obj.updated_at


class DestinationSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Destination.objects.order_by("-created_at")

    def lastmod(self, obj):
        return obj.created_at


sitemaps = {
    "static": StaticViewSitemap,
    "posts": PostSitemap,
    "listings": ListingSitemap,
    "destinations": DestinationSitemap,
}
