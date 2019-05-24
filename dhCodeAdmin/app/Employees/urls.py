from django.urls import path
from dhCodeAdmin.app.Employees.views import CreateEmploye,Search,Update,Destroy,index

urlpatterns = [
    path('',index ),
    path('register/',CreateEmploye, name="Create"),
    path('search/',Search,name="Searching"),
    path('update/',Update,name="Updating"),
    path('delete/',Destroy,name="Destroying"),
]