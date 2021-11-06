from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=256)
    marca = models.CharField(max_length=256)
    precio = models.FloatField()
    descripcion = models.TextField(max_length=2048)
