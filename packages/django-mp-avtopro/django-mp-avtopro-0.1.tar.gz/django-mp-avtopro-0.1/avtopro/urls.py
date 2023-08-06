
from django.urls import path, include

from avtopro import views


app_name = 'avtopro'


urlpatterns = [

    path('export/', views.export_to_avtopro, name='export'),

]


app_urls = [
    path('avtopro/', include((urlpatterns, app_name))),
]
