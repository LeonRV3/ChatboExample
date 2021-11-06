from .models import Producto
from rest_framework import serializers,viewsets


class ProductoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Producto
        fields = ["id","nombre","marca","precio","descripcion"]
