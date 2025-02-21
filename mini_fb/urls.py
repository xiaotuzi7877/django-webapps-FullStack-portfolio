from django.urls import path
from .views import ShowAllProfileView, ShowProfilePageView  # Import both views

urlpatterns = [
    path('', ShowAllProfileView.as_view(), name='show_all_profiles'),  # loads all profiles
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),  # loads a single profile
]

