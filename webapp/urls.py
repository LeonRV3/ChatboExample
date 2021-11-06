from django.urls import path
from .views import ProductoByName

urlpatterns=[
    path("product_by_name",ProductoByName.as_view())
]