# File: views.py
# Author: Li Ziyang (miclilzy@bu.edu), 02/21/2025
# Description: Defines view classes for displaying user profiles in the mini_fb application.

from django.shortcuts import render

# Create your views here.
from .models import Profile
# Import generic class-based views
from django.views.generic import ListView
# Import Profile model to use in views
from django.views.generic import DetailView

class ShowAllProfileView(ListView):
    """
    View to display all user profiles.
    Inherits from Django's generic ListView.
    """
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):
    """
    View to display a single user's profile.
    Inherits from Django's generic DetailView.
    """
    # Specifies the model to use
    model = Profile
    # Path to the template
    template_name = "mini_fb/show_profile.html"
    # Name used to access the specific profile in the template
    context_object_name = "profile"