# Name: Li Ziyang
# BU Email: miclilzy@bu.edu
# File Description: Defines the URL patterns for the 'circuits' application.
# Maps URL paths to their corresponding view functions or classes.

from django.urls import path
from . import views

# Application namespace for URL reversing (e.g., {% url 'circuits:circuit_list' %})
app_name = 'circuits'

# List of URL patterns routed within the circuits app
urlpatterns = [
    # Circuit Views
    path('', views.CircuitListView.as_view(), name='circuit_list'),         # List all circuits
    path('<int:pk>/', views.CircuitDetailView.as_view(), name='circuit_detail'), # Detail view for a specific circuit

    # Comment CRUD Views
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),      # Add a comment to a circuit
    path(
        'comment/<int:pk>/edit/',                                         # Edit an existing comment
        views.CommentUpdateView.as_view(),
        name='comment_update'
    ),
    path(
        'comment/<int:pk>/delete/',                                       # Delete an existing comment
        views.CommentDeleteView.as_view(),
        name='comment_delete'
    ),

    # Quiz and Leaderboard Views
    path('quiz/', views.quiz_view, name='quiz'),                          # The quiz page
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'), # Quiz leaderboard page

    # Other Views
    path('test-map/', views.test_map_view, name='test-map'),             # Test view for map functionality (if still used)
    path('signup/', views.signup, name='signup'),                         # User registration/signup page
]