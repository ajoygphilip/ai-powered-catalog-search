from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Style
from .serializers import ProductDetailSerializer, ProductSerializer

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
