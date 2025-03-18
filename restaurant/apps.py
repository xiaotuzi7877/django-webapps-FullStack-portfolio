"""
File: apps.py
Author: Li Ziyang (miclilzy@bu.edu), 03/18/2025
Description: This file defines the Django application configuration for the 
Restaurant web application. It sets the default primary key type for models 
and registers the app with Django.

Features:
- Specifies the default auto field type (`BigAutoField`).
- Defines the name of the application (`restaurant`).

Usage:
This configuration class is automatically loaded when the Django application starts.
"""

from django.apps import AppConfig

class RestaurantConfig(AppConfig):
    """
    Configuration class for the Restaurant application.

    Attributes:
        default_auto_field (str): Defines the default auto field for models.
        name (str): Specifies the name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurant'
