from django.urls import path
from . import views

urlpatterns = [
    # path('ho', views.main_page, name='main_page'),
    path('main/', views.main, name = 'main'),
    path('order/', views.order, name = 'order'),
    path('confirmation/', views.confirmation, name = 'confirmation'),
]
