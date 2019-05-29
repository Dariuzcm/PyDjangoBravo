from django.db import models

# Create your models here.
class Payment(models.Model):
    emisor = models.CharField(max_length=50)
    receptor = models.CharField(max_length=50)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2)
    motivo = models.CharField(max_length=100)
    fecha = models.DateField()
    
    def __str__(self):
        return '{}'.format(self.emisor)