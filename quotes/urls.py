from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('quote/', views.main_page, name='quote'),
    path('show_all/', views.show_all, name='show_all'),
    path('about/', views.about, name='about'),
]
