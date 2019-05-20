from django.urls import path
from dhCodeAdmin.app.Employees.views import index
urlpatterns = [
    path('',index ),
]