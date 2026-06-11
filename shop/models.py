from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Categoría de tienda"
        verbose_name_plural = "Categorías de tienda"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Categoría")
    name = models.CharField(max_length=200, verbose_name="Nombre del producto")
    slug = models.SlugField(unique=True, blank=True)
    brand = models.CharField(max_length=100, blank=True, verbose_name="Marca")
    merchant_name = models.CharField(max_length=100, blank=True, default="Amazon", verbose_name="Tienda o proveedor")
    description = models.TextField(verbose_name="Descripción")
    recommendation_reason = models.CharField(max_length=220, blank=True, verbose_name="Por qué lo recomendamos")
    best_for = models.CharField(max_length=160, blank=True, verbose_name="Ideal para")
    image = models.ImageField(upload_to='shop_products/', verbose_name="Imagen Principal", null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL de imagen principal")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio aproximado (€)")
    price_note = models.CharField(max_length=80, blank=True, verbose_name="Nota de precio")
    affiliate_url = models.URLField(max_length=1000, verbose_name="Enlace de afiliado")
    button_text = models.CharField(max_length=50, default="Ver producto", verbose_name="Texto del botón")
    is_affiliate = models.BooleanField(default=True, verbose_name="Enlace afiliado")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_image_url(self):
        """Retorna la imagen principal, priorizando la subida local."""
        if self.image:
            return self.image.url
        return self.image_url

    @property
    def display_merchant(self):
        if self.merchant_name:
            return self.merchant_name
        if "amazon." in self.affiliate_url.lower():
            return "Amazon"
        return "Tienda externa"

    @property
    def cta_text(self):
        if self.display_merchant.lower() == "amazon" or "amazon." in self.affiliate_url.lower():
            return "Ver en Amazon"

        generic_labels = {"Ver oferta en Amazon", "Ver producto"}
        if self.button_text and self.button_text not in generic_labels:
            return self.button_text
        return f"Ver en {self.display_merchant}"

    @property
    def price_display(self):
        if self.price_note:
            return self.price_note
        if "amazon." in self.affiliate_url.lower():
            return f"Consultar en {self.display_merchant}"
        return f"{self.price} € aprox."

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop_products/', verbose_name="Imagen", null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL de imagen externa")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_url(self):
        """Retorna la imagen de galeria, priorizando la subida local."""
        if self.image:
            return self.image.url
        return self.image_url

    def __str__(self):
        return f"Imagen para {self.product.name}"
