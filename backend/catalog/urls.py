from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductViewset, TestView

router = DefaultRouter()
router.register(r"products", ProductViewset, basename="product")
urlpatterns = [
    path("", TestView.as_view()),
]
urlpatterns += router.urls
