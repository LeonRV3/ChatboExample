from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import templatize
from django.views.generic import TemplateView
from django.http import HttpResponse
from django import http
from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Producto
from .serializers import ProductoSerializer
from django.core import serializers
import json

# Create your views here.
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoByName(TemplateView):
    def get(self, request) -> http.HttpResponse:
        print(request.GET)
        query = Producto.objects.filter(marca__iexact='cocacolacompany')
        return HttpResponse(serializers.serialize('json',[item for item in query]))
        
    def post(self, request) -> http.HttpResponse:
        request_json = json.loads(request.body)
        query = None
        if(request_json['type']=='all'):
            query = Producto.objects.all()
        elif(request_json['type']=='nombre'):
            query = Producto.objects.filter(nombre__icontains=request_json['str'])
        elif(request_json['type']=='marca'):
            query = Producto.objects.filter(marca__icontains=request_json['str'])
        elif(request_json['type']=='precio'):
            query = Producto.objects.filter(precio__gte=float(request_json['str'])*0.9,precio__lte=float(request_json['str'])*1.1)
        elif(request_json['type']=='descripcion'):
            query = Producto.objects.filter(descripcion__icontains=request_json['str'])
        return HttpResponse(serializers.serialize('json',[item for item in query]),content_type="application/json")