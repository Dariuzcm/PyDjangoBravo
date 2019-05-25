from django.urls import path
from dhCodeAdmin.app.Projects.views import Create,Search,Update,Destroy,index

urlpatterns = [
    path('',index ),
    path('register/',Create, name="Create"),
    path('search/',Search,name="Searching"),
    path('update/',Update,name="Updating"),
    path('delete/',Destroy,name="Destroying"),
]