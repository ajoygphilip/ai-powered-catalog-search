from django_elasticsearch_dsl_drf_alt.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf_alt.viewsets import DocumentViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .documents import CatalogProductDocument
from .models import Style
from .serializers import (
    CatalogProductDocumentSerializer,
    ProductDetailSerializer,
    ProductSerializer,
)

# Create your views here.


class TestView(APIView):
    def get(self, requet, *args, **kwargs):
        return Response("Success")


class ProductViewset(ReadOnlyModelViewSet):
    queryset = Style.objects.all()
    lookup_field = "style_no"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["style_no"]
    search_fields = ["style_no", "name", "brand__name"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductSerializer


class CatalogProductSearchViewset(DocumentViewSet):
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        FacetedSearchFilterBackend,
    ]

    filter_fields = {"style_no": "style_no"}
    search_fields = {"style_no", "name"}
    ordering_fields = {
        "id": "id",
        "name": "name.raw",
        "style_no": "style_no.raw",
    }
    faceted_search_fields = {
        "state_global": {
            "field": "brand.name.raw",
            "enabled": True,
            # "global": True,
        },
    }
    document = CatalogProductDocument
    serializer_class = CatalogProductDocumentSerializer
