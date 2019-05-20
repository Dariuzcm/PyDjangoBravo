from django.urls import path
from dhCodeAdmin.app.Employees.views import index,CreateEmploye
urlpatterns = [
    path('',index ),
    path('register/',CreateEmploye, name="Create"),
]