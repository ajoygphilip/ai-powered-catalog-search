from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    supplier_code = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7, blank=True, null=True)  # e.g. "#FFFFFF"
    swatch_image = models.CharField(max_length=300, unique=True)
    color_group = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=20, unique=True)
    display_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    size_group = models.CharField(max_length=20, default="default")
    sort_order = models.IntegerField(default=0)

    def __str__(self):
        return self.name
