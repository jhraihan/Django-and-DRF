from django.urls import path,include
from . import views

urlpatterns = [
    path('show/',views.show,name = "show"),
    path('<str:pk>/', views.index, name='index'),
    
]