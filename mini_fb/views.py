"""
views.py

This module defines views for handling various pages in the Mini Facebook application, 
including the view to create new profiles.

Author: Li Ziyang (miclilzy@bu.edu)
Date: 02/21/2025
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from .models import Profile, StatusMessage, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm

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

    def get_sucess_url(self):
        """
        redirects to the new profile page after creation
        """  
        return reverse("show_profile", kwargs={"pk": self.object.pk})

class CreateStatusMessageView(CreateView):
    """
    View to create a new StatusMessage for a given Profile.
    - Uses the `CreateStatusMessageForm`.
    - Ensures the message is attached to the correct Profile.
    - Redirects back to the profile page after submission.
    """
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        """Inject the profile object into the template context."""
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """Attach the correct Profile to the status message before saving."""
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the Profile page after successfully posting a status."""
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
    def form_valid(self, form):
        """Handles saving the StatusMessage and associated images."""
        # Save the status message object
        sm = form.save(commit=False)

        # Associate with the correct profile
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        sm.profile = profile
        sm.save()

        print(f"StatusMessage created: {sm.message} (ID: {sm.id}) for Profile: {profile.first_name}")

        # Process uploaded files
        files = self.request.FILES.getlist('files')
        print(f"Files uploaded: {files}")  # Debugging: Check if files are being received

        for file in files:
            # Create and save an Image object
            img = Image(profile=profile, image_file=file)
            img.save()
            print(f"Saved Image: {img.image_file.url}")  # Debugging: Print saved image URL

            # Create and save a StatusImage object
            status_image = StatusImage(status_message=sm, image=img)
            status_image.save()
            print(f"Linked Image {img.image_file.url} to Status {sm.message}")

        return super().form_valid(form)


    def get_success_url(self):
        """redirect to the profile page after positing status"""
        return reverse("show_profile", kwargs = {"pk": self.kwargs['pk']})
