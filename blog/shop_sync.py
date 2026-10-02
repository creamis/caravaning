from html.parser import HTMLParser
from urllib.parse import urlparse, parse_qs, unquote
from django.db import transaction
from django.utils.text import slugify


class ProductLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.products = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return

        data = dict(attrs)

        if not data.get("data-shop-name"):
            return

        self.products.append({
            "name": data["data-shop-name"].strip(),
            "url": data.get("href", "").strip(),
            "image": data.get("data-shop-image", "").strip(),
            "category": data.get("data-shop-category", "").strip(),
        })


def amazon_identity(url):
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()

    if host not in ("amazon.es", "www.amazon.es"):
        return None

    parts = parsed.path.split("/")

    if "dp" in parts:
        index = parts.index("dp")
        if len(parts) > index + 1:
            return ("asin", parts[index + 1].upper())

    params = parse_qs(parsed.query)

    if "k" in params:
        query = unquote(params["k"][0])
        return ("search", " ".join(query.lower().split()))

    return None


def sync_post_products(post):
    from shop.models import Product, Category

    if post.status != "PUBLISHED":
        return

    parser = ProductLinkParser()
    parser.feed(post.content or "")

    if not parser.products:
        return

    with transaction.atomic():
        existing = {}

        for product in Product.objects.all():
            identity = amazon_identity(product.affiliate_url or "")
            if identity:
                existing.setdefault(identity, product)

        processed = set()

        for item in parser.products:
            identity = amazon_identity(item["url"])

            if not identity or identity in processed:
                continue

            processed.add(identity)

            # El producto ya existe: no crear duplicados
            if identity in existing:
                post.shop_products.add(existing[identity])
                continue

            # No crear fichas incompletas
            if not all((
                item["name"],
                item["url"],
                item["image"],
                item["category"],
            )):
                continue

            parsed_image = urlparse(item["image"])
            if (
                parsed_image.scheme not in ("http", "https")
                or not parsed_image.hostname
            ):
                continue

            category, _ = Category.objects.get_or_create(
                slug=slugify(item["category"])[:50],
                defaults={"name": item["category"]},
            )

            base_slug = slugify(item["name"])[:65] or "producto"
            slug = base_slug
            suffix = 2

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug[:60]}-{suffix}"
                suffix += 1

            product = Product.objects.create(
                category=category,
                name=item["name"],
                slug=slug,
                merchant_name="Amazon",
                description=item["name"],
                image_url=item["image"],
                affiliate_url=item["url"],
                button_text="Ver en Amazon",
                is_affiliate=True,
                is_active=True,
            )

            existing[identity] = product
            post.shop_products.add(product)
