from django.urls import path
from dhCodeAdmin.app.Employees.views import index,CreateEmploye,Search

urlpatterns = [
    path('',index ),
    path('register/',CreateEmploye, name="Create"),
    path('search/',Search,name="Searching"),
]