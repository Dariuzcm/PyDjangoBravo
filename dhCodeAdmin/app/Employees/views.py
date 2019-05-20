from django.shortcuts import render
from django.http import HttpResponse
from dhCodeAdmin.app.Employees.models import Employee
# Create your views here.
def index(request):
    return render(request,'Employees/Employees.html')
    
def CreateEmploye(request):
    if request.method=='POST':
        employe = request.POST
        print(employe)
        try:
            Employee(
                nombre = employe.get('nombre'),
                apellido = employe.get('apellido'),
                telefono = employe.get('telefono'),
                email = employe.get('email'),
                fecha_nac = employe.get('fecha_nac'),
                fecha_in = employe.get('fecha_in')
                ).save()
            return HttpResponse('<div class="alert alert-success">Registro Realizado Exitosamente</div>')          
        except ValueError:
            print(ValueError)
            return HttpResponse('<div class="alert alert-danger">No se pudo realizar el registro</div>')

def Employee_ListAll(request):
    pass
    
