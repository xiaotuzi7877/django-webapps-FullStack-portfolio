from django.urls import path
from .views import VoterListView, VoterDetailView, GraphsView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),
    path('graphs/', GraphsView.as_view(), name='graphs'),
    path('voter_analytics/', VoterListView.as_view(), name='voters'),
]
