# File: urls.py
# Author: Li Ziyang (miclilzy@bu.edu), 02/21/2025
# Description: Defines URL patterns for the mini_fb application, mapping views to specific URLs.
from django.urls import path
from .views import ShowAllProfileView, ShowProfilePageView  # Import both views

# URL patterns for the mini_fb application
urlpatterns = [
    path('', ShowAllProfileView.as_view(), name='show_all_profiles'),  # loads all profiles
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),  # loads a single profile
]

