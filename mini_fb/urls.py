"""
urls.py

Defines URL patterns for the Mini Facebook application, including
the route for creating a new profile.

Author: Li Ziyang (miclilzy@bu.edu)
Date: 02/21/2025
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import AddFriendView, ShowAllProfileView, ShowFriendSuggestionsView, ShowNewsFeedView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusMessageView # Import both views

# URL patterns for the mini_fb application
urlpatterns = [
    path('', ShowAllProfileView.as_view(), name='show_all_profiles'),  # loads all profiles
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),  # loads a single profile
    path('create_profile/', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name = 'update_profile'),
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/<int:pk>/add_friend/<int:other_pk>/', AddFriendView.as_view(), name='add_friend'),
    path('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),
    path('login/', auth_views.LoginView.as_view(template_name = 'mini_fb/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
]

