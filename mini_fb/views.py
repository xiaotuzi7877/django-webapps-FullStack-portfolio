from django.shortcuts import render

# Create your views here.
from .models import Profile
from django.views.generic import ListView
from django.views.generic import DetailView

class ShowAllProfileView(ListView):
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"