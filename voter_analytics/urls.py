"""
urls.py

Defines URL routing patterns for the voter_analytics Django application.

This module maps various URL paths to their corresponding views for displaying:
- The home page.
- A detailed view of individual voters.
- Graphical data visualizations.
- A paginated and filterable list of all voters.

Classes Used:
    - HomeView: Landing page for the application.
    - VoterDetailView: Displays all details about a specific voter.
    - GraphsView: Shows data analysis using graphs.
    - VoterListView: Lists and filters all voters based on various criteria.
"""

from django.urls import path
from .views import VoterListView, VoterDetailView, GraphsView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),
    path('graphs/', GraphsView.as_view(), name='graphs'),
    path('voter_analytics/', VoterListView.as_view(), name='voters'),
]
