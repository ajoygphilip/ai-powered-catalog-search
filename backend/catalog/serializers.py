from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Brand, CatalogProductVariant, Style


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class VarientSerializer(ModelSerializer):
    class Meta:
        model = CatalogProductVariant
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Style
        # fields = "__all__"
        exclude = ("created_at", "updated_at")


class ProductDetailSerializer(ProductSerializer):
    variants = VarientSerializer(many=True)
