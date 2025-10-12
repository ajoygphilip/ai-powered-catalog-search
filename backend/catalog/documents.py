from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .elastic_components import (
    description_analyzer,
    sku_edge_ngram_completion_analyzer,
    synonym_analyzer,
)
from .models import CategoryProductCategory, ProductStatus, Style


@registry.register_document
class CatalogProductDocument(Document):
    style_no = fields.TextField(
        fields={
            "raw": fields.KeywordField(),
            "edge_ngram_completion": fields.TextField(
                analyzer=sku_edge_ngram_completion_analyzer
            ),
        }
    )
    brand = fields.ObjectField(
        properties={
            "name": fields.TextField(fields={"raw": fields.KeywordField()}),
            "logo": fields.TextField(index=False),
        }
    )
    name = fields.TextField(analyzer=synonym_analyzer)
    image = fields.TextField(index=False)
    description = fields.TextField(analyzer=description_analyzer)
    categories = fields.ObjectField(
        properties={
            "name": fields.TextField(
                fields={
                    "raw": fields.KeywordField(),
                }
            ),
        }
    )

    varients = fields.NestedField(
        properties={
            "sku": fields.TextField(
                fields={
                    "raw": fields.KeywordField(),
                },
            ),
            "images": fields.TextField(index=False),
            "color": fields.ObjectField(
                properties={
                    "name": fields.TextField(
                        fields={
                            "raw": fields.KeywordField(),
                        }
                    ),
                    "group": fields.TextField(
                        fields={
                            "raw": fields.KeywordField(),
                        }
                    ),
                    "swatch_image": fields.TextField(index=False),
                }
            ),
            "size": fields.ObjectField(
                properties={
                    "display_name": fields.TextField(
                        fields={
                            "raw": fields.KeywordField(),
                        }
                    ),
                    "sort_order": fields.IntegerField(index=False),
                }
            ),
            "product_status": fields.KeywordField(),
            "stock_status": fields.KeywordField(),
            "inventory_total": fields.IntegerField(),
            "price": fields.FloatField(),
        },
    )

    product_status = fields.KeywordField()
    stock_status = fields.KeywordField()

    def prepare_varients(self, instance: Style):
        varients = []
        for varient in instance.variants.all():
            cur = {}
            cur["sku"] = varient.sku
            cur["product_status"] = varient.product_status
            cur["stock_status"] = varient.stock_status
            cur["inventory_total"] = varient.stock
            cur["price"] = varient.price

            size = {
                "name": varient.size.display_name,
                "sort_order": varient.size.sort_order,
            }
            cur["size"] = size

            color = {
                "name": varient.color.name,
                "group": varient.color.color_group,
                "swatch_image": varient.color.swatch_image,
            }
            cur["color"] = color
            cur["image"] = varient.image

            varients.append(cur)
        return varients

    def prepare_categories(self, instance: Style):
        categories = []
        for cp in CategoryProductCategory.objects.filter(
            product=instance, category__depth=3
        ):
            cur = {}
            cur["name"] = cp.category.name
            cur["parent"] = cp.category.get_parent().name
            categories.append(cur)
        return categories

    def get_queryset(self):
        return super().get_queryset().filter(product_status=ProductStatus.ACTIVE)

    class Index:
        name = "catalog_products"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Style
        fields = ["id"]
