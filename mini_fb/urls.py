"""
urls.py

Defines URL patterns for the Mini Facebook application, including
the route for creating a new profile.

Author: Li Ziyang (miclilzy@bu.edu)
Date: 02/21/2025
"""

from django.urls import path
from .views import ShowAllProfileView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView# Import both views

# URL patterns for the mini_fb application
urlpatterns = [
    path('', ShowAllProfileView.as_view(), name='show_all_profiles'),  # loads all profiles
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),  # loads a single profile
    path('create_profile/', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name = 'update_profile'),
]

