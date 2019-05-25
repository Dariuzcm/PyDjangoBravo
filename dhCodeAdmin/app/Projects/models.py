from django.db import models

# Create your models here.
class Project(models.Model):
    proyect_name=models.CharField(max_length=50)
    begin_date =models.DateField()
    end_date =models.DateField()
    manager_name=models.CharField(max_length=50)
    client_name=models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.proyect_name)
