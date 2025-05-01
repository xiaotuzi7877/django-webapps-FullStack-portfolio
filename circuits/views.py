# Name: Li Ziyang
# BU Email: miclilzy@bu.edu
# File Description: Defines the view functions and classes for the 'circuits'
# application, handling HTTP requests and rendering responses.

import json
import random
from datetime import datetime
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login as auth_login
from django.contrib import messages

# --- Model and Form Imports ---
# Consolidate imports and add User
from django.contrib.auth.models import User
from .models import (
    Circuit, Comment, LapTimeEntry, Profile, # Added Profile
    Question, Choice, QuizAttempt, Answer,
    CONTINENT_CHOICES,
)
# *** Import ProfileForm ***
from .forms import CommentForm, LapTimeForm, SignUpForm, ProfileForm # <-- Added ProfileForm

# ==============================================
# Circuit List and Detail Views
# ==============================================

class CircuitListView(ListView):
    """
    Displays a list of F1 circuits. Supports filtering by name via a 'q'
    query parameter and by continent via a 'continent' query parameter.
    Also prepares JSON data for the map display.
    """
    model = Circuit
    template_name = 'circuits/circuit_list.html'
    context_object_name = 'circuits'

    def get_queryset(self):
        """Optionally filter circuits and annotate with average rating."""
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        continent = self.request.GET.get('continent')
        if q:
            qs = qs.filter(name__icontains=q)
        if continent:
            qs = qs.filter(continent=continent)

        # Annotate each circuit with its average comment rating
        qs = qs.annotate(average_rating=Avg('comments__rating'))

        return qs

    def get_context_data(self, **kwargs):
        """
        Adds search parameters, continent choices for dropdown, and JSON data
        for Leaflet map markers to the context.
        """
        context = super().get_context_data(**kwargs)

        # Pass search/filter parameters back to template for display
        context['q'] = self.request.GET.get('q', '')
        context['selected_continent'] = self.request.GET.get('continent', '')

        # Provide choices for the continent filter dropdown
        context['continent_choices'] = CONTINENT_CHOICES

        # Prepare data structure for Leaflet map markers
        map_data = []
        for circuit in context['circuits']:
            map_data.append({
                'name': circuit.name,
                'lat': circuit.latitude,
                'lng': circuit.longitude,
                'url': reverse('circuits:circuit_detail', args=[circuit.pk]),
            })
        context['circuits_data_json'] = json.dumps(map_data)

        return context

# Using Function-Based View for detail as it handles more complex context
def circuit_detail(request, pk):
    """Displays detailed information and forms for a circuit. (FBV version)"""
    circuit = get_object_or_404(Circuit, pk=pk)
    comments = circuit.comments.all().order_by('-created_at') # Fetch comments
    lap_times = circuit.lap_times.all().order_by('lap_time')   # Fetch lap times

    # Initialize forms for display on the detail page
    comment_form = CommentForm()
    lap_time_form = LapTimeForm()

    context = {
        'circuit': circuit,
        'comment_form': comment_form, # Form for adding comments
        'lap_time_form': lap_time_form, # Form for adding lap times
        'lap_times': lap_times,         # Existing lap times list
        'comments': comments,           # Existing comments list
    }
    return render(request, 'circuits/circuit_detail.html', context)


# ==============================================
# Comment Views
# ==============================================

@login_required
def add_comment(request, pk):
    """Handles adding a new comment to a specific circuit via POST."""
    circuit = get_object_or_404(Circuit, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.circuit = circuit
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('circuits:circuit_detail', pk=pk)
        else:
            # Re-render detail page showing comment form errors
            messages.error(request, 'Error adding comment. Please check the form.')
            # Fetch other context needed for detail page
            lap_times = circuit.lap_times.all().order_by('lap_time')
            lap_time_form = LapTimeForm()
            comments = circuit.comments.all().order_by('-created_at')
            context = {
                'circuit': circuit,
                'comment_form': form, # Pass the invalid form back
                'lap_time_form': lap_time_form,
                'lap_times': lap_times,
                'comments': comments,
            }
            return render(request, 'circuits/circuit_detail.html', context)
    else:
        # If GET request, redirect back to detail page (form is shown there)
        return redirect('circuits:circuit_detail', pk=pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows a logged-in user to update their own existing comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'circuits/comment_form.html' # Template for editing

    def get_success_url(self):
        """Redirects to the circuit detail page after successful update."""
        messages.success(self.request, 'Comment updated successfully!')
        return reverse_lazy('circuits:circuit_detail', args=[self.object.circuit.pk])

    def test_func(self):
        """Ensures only the comment author can edit."""
        comment = self.get_object()
        return self.request.user == comment.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows a logged-in user to delete their own existing comment."""
    model = Comment
    template_name = 'circuits/comment_confirm_delete.html' # Confirmation page

    def get_success_url(self):
        """Redirects to the circuit detail page after successful deletion."""
        messages.success(self.request, 'Comment deleted successfully!')
        return reverse_lazy('circuits:circuit_detail', args=[self.object.circuit.pk])

    def test_func(self):
        """Ensures only the comment author can delete."""
        comment = self.get_object()
        return self.request.user == comment.user


# ==============================================
# Lap Time Views
# ==============================================

@login_required
def add_lap_time(request, circuit_pk):
    """Handles adding a new lap time entry for a specific circuit via POST."""
    circuit = get_object_or_404(Circuit, pk=circuit_pk)
    lap_time_form = LapTimeForm(request.POST or None) # Initialize form

    if request.method == 'POST':
        if lap_time_form.is_valid():
            try:
                lap_time_entry = lap_time_form.save(commit=False)
                lap_time_entry.user = request.user
                lap_time_entry.circuit = circuit
                lap_time_entry.save()
                messages.success(request, 'Your lap time has been added!')
                return redirect('circuits:circuit_detail', pk=circuit_pk)
            except Exception as e: # Catch potential integrity errors etc.
                messages.error(request, f'Error saving lap time: {e}')
                # Fall through to re-render the page with the error
        else:
            # Form is invalid, add error message
            messages.error(request, 'Invalid lap time data. Please check your input.')
            # Fall through to re-render the page with the invalid form

    # --- Re-render detail page on GET or failed POST ---
    comments = circuit.comments.all().order_by('-created_at')
    lap_times = circuit.lap_times.all().order_by('lap_time')
    comment_form = CommentForm() # Need a fresh comment form

    # lap_time_form will be empty on GET, or contain errors on failed POST
    context = {
        'circuit': circuit,
        'comment_form': comment_form,
        'lap_time_form': lap_time_form, # Pass the potentially invalid form back
        'lap_times': lap_times,
        'comments': comments,
    }
    return render(request, 'circuits/circuit_detail.html', context)


# ==============================================
# Quiz Views
# ==============================================

@login_required
def quiz_view(request):
    """Renders the quiz page (GET) or processes submitted answers (POST)."""
    if request.method == 'POST':
        # --- Process submitted quiz ---
        start_time_str = request.POST.get('start_time')
        try:
            start_time = datetime.fromisoformat(start_time_str)
        except (ValueError, TypeError):
            messages.error(request, "Invalid quiz start time.")
            return redirect('circuits:quiz') # Redirect back to quiz start

        end_time = timezone.now()

        attempt = QuizAttempt.objects.create(
            user=request.user, start_time=start_time, end_time=end_time, score=0
        )

        score = 0
        question_ids = request.POST.getlist('question_ids')
        # Ensure questions exist and handle potential errors
        questions = Question.objects.filter(id__in=question_ids)
        if len(question_ids) != questions.count():
             messages.error(request, "Error processing quiz questions.")
             attempt.delete() # Clean up incomplete attempt
             return redirect('circuits:quiz')

        for q in questions:
            choice_id = request.POST.get(f'question_{q.id}')
            is_correct_answer = False
            selected_choice = None

            if choice_id:
                try:
                    choice = Choice.objects.select_related('question').get(id=int(choice_id))
                    # Verify choice belongs to the question being processed
                    if choice.question == q:
                        selected_choice = choice
                        if choice.is_correct:
                            score += 1
                            is_correct_answer = True
                    else:
                        # Handle case where submitted choice_id doesn't match question
                         messages.warning(request, f"Submitted choice for question '{q.text}' was invalid.")
                except (Choice.DoesNotExist, ValueError):
                     messages.warning(request, f"Invalid choice submitted for question '{q.text}'.")

            # Record the answer
            Answer.objects.create(
                attempt=attempt, question=q,
                selected_choice=selected_choice, is_correct=is_correct_answer
            )

        attempt.score = score
        attempt.save()
        messages.success(request, f"Quiz submitted! Your score: {score}")
        return redirect('circuits:leaderboard')

    # --- Handle GET request: Prepare and render the quiz ---
    all_questions = list(Question.objects.all())
    num_questions_to_sample = min(len(all_questions), 6)
    if num_questions_to_sample < 1:
         messages.warning(request, "No quiz questions available.")
         # Maybe redirect somewhere else or render template with message
         return render(request, 'circuits/quiz.html', {'questions': []})

    sampled_questions = random.sample(all_questions, num_questions_to_sample)

    context = {
        'questions': sampled_questions,
        'question_ids': [q.id for q in sampled_questions],
        'now': timezone.now().isoformat(),
    }
    return render(request, 'circuits/quiz.html', context)


class LeaderboardView(ListView):
    """Displays top quiz attempts sorted by score and time."""
    model = QuizAttempt
    template_name = 'circuits/leaderboard.html'
    context_object_name = 'attempts'
    paginate_by = 20 # Optional: Add pagination

    def get_queryset(self):
        """Returns top attempts ordered by score (desc) and duration (asc)."""
        # Select related user for efficiency in template
        return QuizAttempt.objects.select_related('user').order_by('-score', 'end_time')


# ==============================================
# Authentication and User Profile Views
# ==============================================

def signup(request):
    """Handles user registration."""
    if request.user.is_authenticated:
        return redirect('circuits:circuit_list') # Redirect if already logged in

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # Log in the new user
            messages.success(request, 'Signup successful! Welcome.')
            # Redirect to circuit list or perhaps their new (empty) profile?
            return redirect('circuits:circuit_list')
            # Alternatively, redirect to edit profile page after signup:
            # return redirect('circuits:edit_profile')
        else:
             messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()

    return render(request, 'circuits/signup.html', {'form': form})


@login_required # Ensure user is logged in to edit profile
def edit_profile(request):
    """
    Handles editing the logged-in user's profile (e.g., avatar).
    """
    # Get the Profile instance associated with the current user.
    # Creates one if it doesn't exist (robustness for edge cases).
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Populate the form with submitted data AND files, bound to the user's profile instance
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save() # Save the changes to the profile (including avatar)
            messages.success(request, 'Your profile has been updated successfully!')
            # Redirect to the user's public profile view
            return redirect('circuits:user_profile', username=request.user.username)
        else:
            # Form is invalid, display errors
            messages.error(request, 'Please correct the errors below.')
            # The invalid form (with errors) will be rendered below
    else: # GET request
        # Create a form instance pre-filled with the user's current profile data
        form = ProfileForm(instance=profile)

    # Render the edit profile template with the form
    return render(request, 'circuits/edit_profile.html', {'form': form})


def community_view(request):
    """Displays a list of all registered users with their avatars."""
    # Fetch users, optimize by prefetching related Profile using the correct related_name
    # Order users alphabetically by username
    users_list = User.objects.select_related('circuits_profile').all().order_by('username')

    context = {
        'users': users_list, # Pass the user list to the template
    }
    return render(request, 'circuits/community.html', context)


def user_profile_view(request, username):
    """Displays the profile page for a specific user, showing their posts."""
    # Fetch the target user, optimize by prefetching related Profile
    # Use get_object_or_404 to handle cases where the user doesn't exist
    target_user = get_object_or_404(
        User.objects.select_related('circuits_profile'),
        username=username
    )

    # Fetch comments made by this user, optimize by prefetching related Circuit
    user_comments = Comment.objects.filter(user=target_user).select_related('circuit').order_by('-created_at')

    # Fetch lap times submitted by this user, optimize by prefetching related Circuit
    user_lap_times = LapTimeEntry.objects.filter(user=target_user).select_related('circuit').order_by('circuit__name', 'lap_time')

    # --- NEW: Get user's highest quiz score ---
    highest_quiz_attempt = QuizAttempt.objects.filter(user=target_user).order_by('-score').first()
    # If the user has attempts, get the score, otherwise set to None or a placeholder like 'N/A'
    highest_score = highest_quiz_attempt.score if highest_quiz_attempt else None

    context = {
        'target_user': target_user,      # The user whose profile is being viewed
        'comments': user_comments,       # List of comments by this user
        'lap_times': user_lap_times,    # List of lap times by this user
        'is_own_profile': request.user == target_user, # Add flag to check if viewing own profile
        'highest_quiz_score': highest_score,
    }
    return render(request, 'circuits/user_profile.html', context)


# --- NEW: Lap Time Update View ---
class LapTimeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows the owner of a lap time entry to update it."""
    model = LapTimeEntry
    form_class = LapTimeForm # Reuse the form used for adding
    template_name = 'circuits/laptime_form.html' # We need to create this template
    context_object_name = 'laptime' # Optional: name in template context

    def get_success_url(self):
        """Redirect to the circuit detail page after successful update."""
        messages.success(self.request, 'Lap time updated successfully!')
        # Redirect back to the detail page of the circuit this lap time belongs to
        return reverse_lazy('circuits:circuit_detail', args=[self.object.circuit.pk])

    def test_func(self):
        """Check if the current user is the owner of the lap time entry."""
        laptime = self.get_object()
        return self.request.user == laptime.user

# --- NEW: Lap Time Delete View ---
class LapTimeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows the owner of a lap time entry to delete it after confirmation."""
    model = LapTimeEntry
    template_name = 'circuits/laptime_confirm_delete.html' # We need to create this template
    context_object_name = 'laptime' # Optional: name in template context

    def get_success_url(self):
        """Redirect to the circuit detail page after successful deletion."""
        messages.success(self.request, 'Lap time deleted successfully!')
        # Redirect back to the detail page of the circuit this lap time belonged to
        return reverse_lazy('circuits:circuit_detail', args=[self.object.circuit.pk])

    def test_func(self):
        """Check if the current user is the owner of the lap time entry."""
        laptime = self.get_object()
        return self.request.user == laptime.user

# ==============================================
# Other/Test Views
# ==============================================

def test_map_view(request):
    """Renders a standalone test map page (likely for development)."""
    # Consider removing or securing this if not needed in production
    return render(request, 'circuits/test_map.html')

# --- End of views.py ---