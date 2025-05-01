# Name: Li Ziyang
# BU Email: miclilzy@bu.edu
# File Description: Defines the view functions and classes for the 'circuits' 
# application, handling HTTP requests and rendering responses.

import json
import random
from datetime import datetime

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

from .models import (
    Circuit,
    Question,
    Choice,
    QuizAttempt,
    Answer,
    Comment,
    CONTINENT_CHOICES,
)
from .forms import CommentForm, SignUpForm


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
        """
        Filters the base queryset based on 'q' (name search) and 'continent' 
        GET parameters.

        Returns:
            QuerySet: The potentially filtered QuerySet of Circuits.
        """
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        continent = self.request.GET.get('continent')
        
        # Apply name filter if 'q' parameter is present
        if q:
            qs = qs.filter(name__icontains=q)
        # Apply continent filter if 'continent' parameter is present
        if continent:
            qs = qs.filter(continent=continent)
            
        return qs

    def get_context_data(self, **kwargs):
        """
        Adds search parameters, continent choices for dropdown, and JSON data 
        for Leaflet map markers to the context.

        Args:
            **kwargs: Additional keyword arguments from the view.

        Returns:
            dict: The context dictionary for rendering the template.
        """
        context = super().get_context_data(**kwargs)
        
        # Pass search/filter parameters back to template for display
        context['q'] = self.request.GET.get('q', '')
        context['selected_continent'] = self.request.GET.get('continent', '')

        # Provide choices for the continent filter dropdown
        context['continent_choices'] = CONTINENT_CHOICES

        # Prepare data structure for Leaflet map markers
        map_data = []
        # Iterate over the filtered circuits included in the current context
        for circuit in context['circuits']: 
            map_data.append({
                'name': circuit.name,
                'lat': circuit.latitude,
                'lng': circuit.longitude,
                'url': reverse('circuits:circuit_detail', args=[circuit.pk]),
            })
        # Convert the list of dictionaries to a JSON string for the template
        context['circuits_data_json'] = json.dumps(map_data)

        return context


class CircuitDetailView(DetailView):
    """Displays detailed information for a single circuit."""
    model = Circuit
    template_name = 'circuits/circuit_detail.html'
    context_object_name = 'circuit'

    def get_context_data(self, **kwargs):
        """
        Adds an empty CommentForm instance to the context for comment submission.

        Args:
            **kwargs: Additional keyword arguments from the view.

        Returns:
            dict: The context dictionary including the comment form.
        """
        context = super().get_context_data(**kwargs)
        # Initialize an empty form for adding new comments
        context['form'] = CommentForm()  
        return context


@login_required
def add_comment(request, pk):
    """
    Handles the submission of a new comment via POST request for a specific circuit.
    Requires user to be logged in.

    Args:
        request: The HttpRequest object.
        pk (int): The primary key of the Circuit being commented on.

    Returns:
        HttpResponseRedirect: Redirects back to the circuit detail page 
                              after processing the comment.
    """
    circuit = get_object_or_404(Circuit, pk=pk)
    # Process submitted form data if request is POST, otherwise create empty form
    form = CommentForm(request.POST or None)  
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False) # Create Comment object but don't save yet
        comment.user = request.user       # Assign the logged-in user
        comment.circuit = circuit       # Assign the relevant circuit
        comment.save()                    # Save the complete comment object
        # Redirect to the same circuit detail page to see the new comment
        return redirect('circuits:circuit_detail', pk=pk) 
    
    # If GET or form invalid, redirect back (or handle differently if needed)
    # Typically, invalid POST would re-render detail with errors, but this
    # simplifies by always redirecting. Consider enhancing error handling.
    return redirect('circuits:circuit_detail', pk=pk)


@login_required
def quiz_view(request):
    """
    Renders the quiz page (GET) or processes the submitted quiz answers (POST).
    Requires user to be logged in.

    On GET: Displays a set of randomly selected questions.
    On POST: Grades the submitted answers, creates QuizAttempt and Answer
             records, and redirects to the leaderboard.

    Args:
        request: The HttpRequest object.

    Returns:
        HttpResponse: Renders the quiz template (GET) or redirects to the 
                      leaderboard (POST).
    """
    if request.method == 'POST':
        # --- Process submitted quiz ---
        # Retrieve start time from hidden form field
        start_time_str = request.POST.get('start_time')
        try:
            start_time = datetime.fromisoformat(start_time_str)
        except (ValueError, TypeError):
            # Handle error: invalid start time format - potentially redirect back with error
            # For simplicity, redirecting to leaderboard for now.
            return redirect('circuits:leaderboard') 
        
        end_time = timezone.now()
        
        # Create the initial attempt record (score will be updated later)
        attempt = QuizAttempt.objects.create(
            user=request.user,
            start_time=start_time,
            end_time=end_time,
            score=0 # Initialize score to 0
        )
        
        score = 0
        # Get the list of question IDs that were presented in the quiz
        question_ids = request.POST.getlist('question_ids')
        questions = Question.objects.filter(id__in=question_ids)
        
        # Iterate through presented questions to grade submitted answers
        for q in questions:
            # Get the selected choice ID for this question from the POST data
            choice_id = request.POST.get(f'question_{q.id}')
            is_correct_answer = False
            selected_choice = None
            
            if choice_id:
                try:
                    # Retrieve the Choice object corresponding to the submitted ID
                    choice = Choice.objects.get(id=int(choice_id))
                    selected_choice = choice
                    # Check if the selected choice belongs to the current question 
                    # and if it's marked as correct
                    if choice.question == q and choice.is_correct:
                        score += 1 # Increment score for correct answer
                        is_correct_answer = True
                except (Choice.DoesNotExist, ValueError):
                    # Handle cases where choice_id is invalid or doesn't exist
                    pass 
            
            # Record the user's answer (or lack thereof) for this question
            Answer.objects.create(
                attempt=attempt,
                question=q,
                selected_choice=selected_choice, # Can be None if no answer submitted
                is_correct=is_correct_answer
            )
            
        # Update the attempt record with the final calculated score
        attempt.score = score
        attempt.save()
        
        # Redirect user to the leaderboard to see their ranking
        return redirect('circuits:leaderboard')

    # --- Handle GET request: Prepare and render the quiz ---
    all_questions = list(Question.objects.all())
    # Randomly select 6 questions, or fewer if not enough questions exist
    num_questions_to_sample = min(len(all_questions), 6) 
    sampled_questions = random.sample(all_questions, num_questions_to_sample)
    
    context = {
        'questions': sampled_questions,
        # Pass question IDs to the template for inclusion in the form
        'question_ids': [q.id for q in sampled_questions], 
         # Pass current time for recording the quiz start time in the form
        'now': timezone.now().isoformat(), 
    }
    return render(request, 'circuits/quiz.html', context)


class LeaderboardView(ListView):
    """Displays top quiz attempts sorted by score descending, time ascending."""
    model = QuizAttempt
    template_name = 'circuits/leaderboard.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        """
        Returns the top 20 QuizAttempts ordered first by score (highest first)
        and then by duration (shortest first - using end_time as proxy).

        Returns:
            QuerySet: The QuerySet of the top 20 QuizAttempts.
        """
        # Order by score descending (-score), then end_time ascending 
        # (assuming attempts started roughly same time, earlier end = faster)
        return QuizAttempt.objects.order_by('-score', 'end_time')[:20]


def test_map_view(request):
    """
    Renders a standalone test map page. 
    (Note: Likely used for development/testing purposes only).

    Args:
        request: The HttpRequest object.

    Returns:
        HttpResponse: Renders the 'test_map.html' template.
    """
    return render(request, 'circuits/test_map.html')


def signup(request):
    """
    Handles user registration (signup).

    On GET: Displays the signup form.
    On POST: Processes the signup form, creates a new user, logs them in,
             and redirects to the circuit list page.

    Args:
        request: The HttpRequest object.

    Returns:
        HttpResponse: Renders the signup template (GET or invalid POST) or
                      redirects to circuit list (successful POST).
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() # Create the new user instance
            auth_login(request, user) # Log the new user in automatically
            return redirect('circuits:circuit_list') # Redirect to main page
    else: # GET request
        form = SignUpForm() # Create an empty form instance
        
    return render(request, 'circuits/signup.html', {'form': form})


class CommentUpdateView(
    LoginRequiredMixin,  # Ensures user is logged in
    UserPassesTestMixin, # Ensures user owns the comment
    UpdateView           # Provides generic update functionality
):
    """
    Allows a logged-in user to update their own existing comment.
    Inherits from UpdateView for standard form handling and object loading.
    Uses mixins for access control.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'circuits/comment_form.html' # Reuse the comment form template

    def get_success_url(self):
        """
        Determines the URL to redirect to after successful comment update.

        Returns:
            str: The URL for the detail page of the circuit the comment belongs to.
        """
        # Redirect back to the detail page of the circuit associated with this comment
        return reverse_lazy(
            'circuits:circuit_detail', args=[self.object.circuit.pk]
        )

    def test_func(self):
        """
        Checks if the currently logged-in user is the author of the comment.
        This method is required by UserPassesTestMixin.

        Returns:
            bool: True if the user is the author, False otherwise.
        """
        # Retrieve the comment object being accessed
        comment = self.get_object() 
        # Check if the request user matches the comment's author
        return self.request.user == comment.user


class CommentDeleteView(
    LoginRequiredMixin,  # Ensures user is logged in
    UserPassesTestMixin, # Ensures user owns the comment
    DeleteView           # Provides generic deletion functionality
):
    """
    Allows a logged-in user to delete their own existing comment.
    Inherits from DeleteView for confirmation page and object deletion.
    Uses mixins for access control.
    """
    model = Comment
    template_name = 'circuits/comment_confirm_delete.html' # Confirmation page

    def get_success_url(self):
        """
        Determines the URL to redirect to after successful comment deletion.

        Returns:
            str: The URL for the detail page of the circuit the comment belonged to.
        """
        # Redirect back to the detail page of the circuit associated with the deleted comment
        # Note: self.object refers to the comment *before* it's deleted
        return reverse_lazy(
            'circuits:circuit_detail', args=[self.object.circuit.pk]
        )

    def test_func(self):
        """
        Checks if the currently logged-in user is the author of the comment.
        This method is required by UserPassesTestMixin.

        Returns:
            bool: True if the user is the author, False otherwise.
        """
        # Retrieve the comment object being accessed
        comment = self.get_object()
        # Check if the request user matches the comment's author
        return self.request.user == comment.user