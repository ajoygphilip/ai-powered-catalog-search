from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CatalogProductSearchViewset, ProductViewset, TestView

router = DefaultRouter()
router.register(r"", ProductViewset, basename="product")
router.register(r"products", CatalogProductSearchViewset, basename="search")
urlpatterns = [
    path("test", TestView.as_view()),
]
urlpatterns += router.urls
