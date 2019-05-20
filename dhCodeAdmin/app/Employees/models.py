from django.db import models

# Create your models here.
class Employee(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    fecha_nac = models.DateField()
    fecha_in = models.DateField()
    
