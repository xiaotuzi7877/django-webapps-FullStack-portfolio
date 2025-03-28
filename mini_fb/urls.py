"""
urls.py

Defines URL patterns for the Mini Facebook application, including
the route for creating a new profile.

Author: Li Ziyang (miclilzy@bu.edu)
Date: 02/21/2025
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import AddFriendView, ShowAllProfileView, ShowFriendSuggestionsView, ShowMyProfileView, ShowNewsFeedView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusMessageView, LogoutConfirmationView # Import both views

# URL patterns for the mini_fb application
urlpatterns = [
    # Core profile navigation
    path('', ShowAllProfileView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),

    # NEW: Updated URLs using the logged-in user context
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),
    path('profile/add_friend/<int:pk>/<int:other_pk>/', AddFriendView.as_view(), name='add_friend'),
    path('status/create_status/<int:pk>/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/my/', ShowMyProfileView.as_view(), name='my_profile'),

    # Status message management
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
    
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name='logout_confirmation'),
]

