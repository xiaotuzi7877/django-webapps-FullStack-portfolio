"""
File: urls.py
Author: Li Ziyang (miclilzy@bu.edu), 03/18/2025
Description: This file defines the URL patterns for the Restaurant web application.
It maps URL routes to their corresponding view functions.

Features:
- Maps the root URL (`'/'`) and `/main/` to the main page.
- Defines an `order/` route for customers to place orders.
- Defines a `confirmation/` route for order confirmations.

Usage:
This file is used by Django's URL dispatcher to route HTTP requests 
to the appropriate views.
"""

from django.urls import path
from . import views

urlpatterns = [
    # path('ho', views.main_page, name='main_page'),
    path('', views.main, name = 'main'),
    path('main/', views.main, name = 'main'),
    path('order/', views.order, name = 'order'),
    path('confirmation/', views.confirmation, name = 'confirmation'),
]
