"""
File: urls.py
Author: Li Ziyang (miclilzy@bu.edu), 03/18/2025
Description: This file defines the URL patterns for the Quotes web application.
It maps URL routes to their corresponding view functions.

Features:
- Maps the root URL (`'/'`) to `main_page`.
- Provides named URL paths for the main quote page, show-all quotes page, and about page.
- Uses Django's `path()` function to define URL patterns.

Usage:
This file is used by Django's URL dispatcher to route HTTP requests 
to the appropriate views.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('quote/', views.main_page, name='quote'),
    path('show_all/', views.show_all, name='show_all'),
    path('about/', views.about, name='about'),
]
