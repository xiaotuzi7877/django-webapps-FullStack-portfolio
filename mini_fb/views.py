"""
views.py

This module defines views for handling various pages in the Mini Facebook application, 
including the view to create new profiles.

Author: Li Ziyang (miclilzy@bu.edu)
Date: 02/21/2025
"""
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Profile
from .forms import CreateProfileForm

# Create your views here.
from .models import Profile
# Import generic class-based views
from django.views.generic import ListView
# Import Profile model to use in views
from django.views.generic import DetailView
from .forms import CreateProfileForm

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

def create_profile(request):
    """
    Handles the creation of a new Profile.

    If the request method is POST, validates the form and saves the Profile.
    Otherwise, renders an empty form for user input.

    Args:
        request (HttpRequest): The request object containing form data.

    Returns:
        HttpResponse: Renders the profile creation page or redirects to profile list.
    """
    if request.method == "POST":
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect to all files after saving
            return redirect('show_all_profiles')
    else:
            form = CreateProfileForm()
    return render(request, "mini_fb/create_profile.html", {"form": form})

class CreateProfileView(CreateView):
    """
    A class-based view for creating a new Profile.
    
    This view utilizes Django's generic CreateView to handle profile creation.
    The form used is CreateProfileForm, and the template used is 'mini_fb/create_profile_form.html'.
    """
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"
    success_url = reverse_lazy('show_all_profiles')  