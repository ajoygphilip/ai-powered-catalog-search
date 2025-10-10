from django.db import models
from shared.abstract_models import TimeStampedModel
from treebeard.mp_tree import MP_Node

from .attribute_models import Brand, Color, Size


class ProductStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    ARCHIVED = "archived", "Archived"


class StockStatus(models.TextChoices):
    IN_STOCK = "in_stock", "In Stock"
    LOW_STOCK = "low_stock", "Low Stock"
    OUT_OF_STOCK = "out_of_stock", "Out of Stock"


class ProductCategory(MP_Node, TimeStampedModel):
    _slug_separator = "/"
    _full_name_separator = " > "

    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, db_index=True)
    sort_order = models.IntegerField(default=0)
    is_landing_page = models.BooleanField(default=False)
    category_title = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class Style(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    style_no = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    supplier_code = models.TextField(blank=True)
    brand = models.ForeignKey(
        "Brand", max_length=100, blank=True, null=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.TextField(blank=True, null=True)
    product_status = models.CharField(
        max_length=20, choices=ProductStatus.choices, default=ProductStatus.DRAFT
    )
    stock_status = models.CharField(
        max_length=20, choices=StockStatus.choices, default=StockStatus.IN_STOCK
    )

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class CatalogProductVariant(models.Model):
    style = models.ForeignKey(Style, related_name="variants", on_delete=models.CASCADE)
    sku = models.CharField(max_length=100, unique=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.URLField(blank=True, null=True)
    size = models.ForeignKey("Size", null=True, on_delete=models.SET_NULL)
    color = models.ForeignKey("Color", null=True, on_delete=models.SET_NULL)
    product_status = models.CharField(
        max_length=20, choices=ProductStatus.choices, default=ProductStatus.DRAFT
    )
    stock_status = models.CharField(
        max_length=20, choices=StockStatus.choices, default=StockStatus.IN_STOCK
    )

    def __str__(self):
        return f"{self.style} - {self.sku} - {self.color} {self.size}"


class CategoryProductCategory(models.Model):
    product = models.ForeignKey("Style", on_delete=models.CASCADE)
    category = models.ForeignKey("ProductCategory", on_delete=models.CASCADE)
