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
    description = models.TextField(verbose_name="Descripción")
    image = models.ImageField(upload_to='shop_products/', verbose_name="Imagen Principal", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio aproximado (€)")
    affiliate_url = models.URLField(max_length=1000, verbose_name="Enlace de afiliado")
    button_text = models.CharField(max_length=50, default="Ver oferta en Amazon", verbose_name="Texto del botón")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop_products/', verbose_name="Imagen")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen para {self.product.name}"
