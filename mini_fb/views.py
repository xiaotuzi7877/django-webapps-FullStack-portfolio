"""
views.py

This module defines views for handling various pages in the Mini Facebook application, 
including the view to create new profiles.

Author: Li Ziyang (miclilzy@bu.edu)
Date: 02/21/2025
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Friend, Profile, StatusMessage, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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

    def get_context_data(self, **kwargs):
        """
        adds the list of friends to the profile page context
        """
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["friends"] = profile.get_friends()  # Use the get_friends method
        # show at most 4 friends suggestions
        context["suggested_friends_preview"] = profile.get_friend_suggestions()[:4] 
        return context
    
# new view for the logged-in user
class ShowMyProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["friends"] = profile.get_friends()
        context["suggested_friends_preview"] = profile.get_friend_suggestions()[:4]
        return context

    
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

class CreateProfileView(LoginRequiredMixin, CreateView):
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

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
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

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    View to handle updating an existing Profile in the Mini Facebook application.

    This class-based view inherits from Django's generic `UpdateView`, allowing users
    to modify specific profile details, excluding first and last names.

    Attributes:
        model (Profile): The model representing user profiles.
        form_class (UpdateProfileForm): The form used to update profile fields.
        template_name (str): The template used to render the profile update form.
    """
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_context_data(self, **kwargs):
        """Add UserCreationForm to the template context."""
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        """Handle form submission for updating both user and profile."""
        user_form = UserCreationForm(request.POST)
        profile_form = self.form_class(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            login(request, user)

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect("show_profile", pk=profile.pk)

        return render(request, self.template_name, {
            "user_form": user_form,
            "form": profile_form
        })
    

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    """
    View to handle the deletion of a StatusMessage in the Mini Facebook application.

    This class-based view inherits from Django's generic `DeleteView`, providing
    a confirmation page for deleting a status message. Upon successful deletion,
    it redirects the user back to the corresponding profile page.

    Attributes:
        model (StatusMessage): The model representing status messages.
        template_name (str): The template used to confirm the deletion.
        context_object_name (str): The name used to reference the status message object in the template.
    """
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status"

    def get_success_url(self):
        """Redirect back to the profile page after deleting a status message."""
        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    """
    View to handle updating an existing StatusMessage in the Mini Facebook application.

    This class-based view inherits from Django's generic `UpdateView`, allowing users
    to edit only the message content of an existing status message.

    Attributes:
        model (StatusMessage): The model representing status messages.
        fields (list): Specifies that only the `message` field can be updated.
        template_name (str): The template used to render the update form.
    """
    model = StatusMessage
    fields = ["message"]  # Only allow updating the message text
    template_name = "mini_fb/update_status_form.html"

    def get_success_url(self):
        """Redirect back to the profile page after updating a status message."""
        if self.object.profile:  # Ensure profile exists
            return reverse("show_profile", kwargs={"pk": self.object.profile.pk})
        else:
            return reverse("show_all_profiles")  # Fallback in case of error

class AddFriendView(LoginRequiredMixin, View):
    """
    Handles adding a friend based on URL parameters.
    """

    def dispatch(self, request, pk, other_pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)
        other_profile = get_object_or_404(Profile, pk=other_pk)
        profile.add_friend(other_profile)
        return redirect('show_profile', pk=pk)  # Redirect to the profile page
    
class ShowFriendSuggestionsView(DetailView):
    """
    Displays friend suggestions for a given Profile.
    """
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["suggested_friends"] = profile.get_friend_suggestions()
        return context
    
    def get_object(self):
        """Use Logged-in User Instead of pk"""
        if not self.request.user.is_authenticated:
            raise Http404("User must be logged in to view suggestions")
        return get_object_or_404(Profile, user=self.request.user)
    
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    """
    View to display the news feed for a given Profile.

    This view retrieves all StatusMessages posted by the profile itself 
    and its friends (via the `get_news_feed()` method), and renders them 
    in reverse chronological order on the news feed page.

    Attributes:
        model (Profile): The Django model representing the user profile.
        template_name (str): Path to the HTML template used for rendering the view.
        context_object_name (str): The context name to use for the profile object in the template.
    """
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        """
        Injects the news feed (status messages from self and friends) 
        into the template context under 'news_feed'.
        
        Returns:
            dict: The context data passed to the template, including the profile and news_feed.
        """
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["news_feed"] = profile.get_news_feed()
        return context
    
    def get_object(self):
        """Use Logged-in User Instead of pk"""
        return get_object_or_404(Profile, user=self.request.user)

class LogoutConfirmationView(TemplateView):
    """Render the logout confirmation page."""
    template_name = "mini_fb/logged_out.html"

class AddFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        # 获取当前用户的 Profile
        user_profile = get_object_or_404(Profile, user=request.user)
        # 在此处可以添加进一步判断：例如是否允许添加好友等
        
        # 将当前用户的 Profile 放入 self 中，供后续使用
        self.profile = user_profile
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # 从 URL 中获取要添加好友的 Profile 的 ID
        other_pk = kwargs.get('other_pk')
        # 注意：直接用当前用户的 Profile 执行添加好友操作
        # 假设你在 Profile 模型中已经定义了 add_friend 方法
        target_profile = get_object_or_404(Profile, pk=other_pk)
        self.profile.add_friend(target_profile)
        return redirect('show_profile')