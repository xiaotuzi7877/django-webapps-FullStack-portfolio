"""
views.py

Defines the core views for the voter_analytics Django application, enabling the
display of voter data, graphical analytics, and filtering functionality.

This module includes:
- VoterListView: Lists and filters registered voters from the database.
- VoterDetailView: Shows detailed information for a single voter.
- GraphsView: Generates interactive visualizations using Plotly.
- HomeView: Renders a static homepage template.
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q, Count
from django.utils.safestring import mark_safe
from django.db import models

from .models import Voter

import datetime
import plotly.express as px
import plotly.graph_objects as go

# Optional for grouping small categories
import pandas as pd


class VoterListView(ListView):
    """
    Displays a paginated and filterable list of all registered voters.

    Users can filter by party affiliation, voter score, year of birth range,
    and participation in specific elections. The results are shown in a
    styled table with pagination.
    """
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        """
        Returns the filtered queryset based on GET parameters.
        """
        queryset = super().get_queryset()
        party = self.request.GET.get('party')
        score = self.request.GET.get('score')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')

        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        selected_elections = [e for e in elections if self.request.GET.get(e)]

        if party:
            queryset = queryset.filter(party_affiliation__iexact=party.strip())

        if score:
            queryset = queryset.filter(voter_score=int(score))

        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))

        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))

        for election in selected_elections:
            filter_kwargs = {election: True}
            queryset = queryset.filter(**filter_kwargs)

        return queryset.order_by('last_name', 'first_name')

    def get_context_data(self, **kwargs):
        """
        Adds a list of years (1900–2024) to the template context for dropdown filters.
        """
        context = super().get_context_data(**kwargs)
        context['years'] = range(1900, 2025)  # for dropdown
        return context


class VoterDetailView(DetailView):
    """
    Displays full details about a specific voter.

    Includes personal information, registration and birth date,
    election participation history, and a Google Maps link to the voter's address.
    """
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class GraphsView(ListView):
    """
    Displays interactive graphs to summarize voter data using Plotly.

    Includes:
    - A histogram of birth years.
    - A pie chart of party affiliations.
    - A bar chart showing participation in five past elections.
    All graphs respond to the same filters used in the voter list.
    """
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        """
        Returns the filtered queryset of voters based on GET parameters,
        for generating graphs.
        """
        queryset = super().get_queryset()
        request = self.request

        party = request.GET.get('party')
        score = request.GET.get('score')
        min_year = request.GET.get('min_year')
        max_year = request.GET.get('max_year')

        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        selected_elections = [e for e in elections if request.GET.get(e)]

        if party:
            queryset = queryset.filter(party_affiliation__iexact=party.strip())

        if score:
            queryset = queryset.filter(voter_score=int(score))

        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))

        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))

        for election in selected_elections:
            filter_kwargs = {election: True}
            queryset = queryset.filter(**filter_kwargs)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Builds Plotly graphs and adds them to the template context.

        Generates:
        - Birth year histogram.
        - Party affiliation pie chart.
        - Election participation bar chart.
        """
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        #
        # 1) Year-of-birth histogram
        #
        yob_counts = voters.values_list('date_of_birth__year', flat=True)
        yob_fig = px.histogram(
            x=yob_counts,
            nbins=125, 
            title=f"Voter Distribution by Year of Birth (n={voters.count()})"
        )
        yob_fig.update_layout(bargap=0.05)
        context['yob_chart'] = mark_safe(yob_fig.to_html(full_html=False))

        #
        # 2) Pie chart by party
        #
        party_qs = voters.values('party_affiliation').annotate(count=Count('id'))
        df = pd.DataFrame(party_qs)

        if not df.empty:
            total_voters = df['count'].sum()
            df['party_affiliation'] = df['party_affiliation'].fillna('').replace('', 'Unknown')
        else:
            total_voters = 0
            df = pd.DataFrame({'party_affiliation': [], 'count': []})

        party_labels = df['party_affiliation']
        party_values = df['count']

    
        party_fig = px.pie(
            values=party_values,
            names=party_labels,
            title=f"Voter Distribution by Party Affiliation (n={total_voters})",
            width=900,      
            height=1200      
        )

        party_fig.update_layout(
            title_x=0.5,
            title_font_size=18,
            margin=dict(l=40, r=150, t=80, b=40),
            legend=dict(
                x=1.2,   
                y=0.5    
            )
        )

        party_fig.update_traces(
            textposition='auto',
            textinfo='label+percent'
        )

        context['party_chart'] = mark_safe(party_fig.to_html(full_html=False))

        #
        # 3) Participation bar chart
        #
        participation_data = [
            ("2020 State",   voters.filter(v20state=True).count()),
            ("2021 Town",    voters.filter(v21town=True).count()),
            ("2021 Primary", voters.filter(v21primary=True).count()),
            ("2022 General", voters.filter(v22general=True).count()),
            ("2023 Town",    voters.filter(v23town=True).count()),
        ]
        election_labels = [label for (label, count) in participation_data]
        voter_counts    = [count for (label, count) in participation_data]

        participation_fig = px.bar(
            x=election_labels,
            y=voter_counts,
            labels={"x": "Election", "y": "Number of Voters"},
            title=f"Vote Count by Election (n={voters.count()})",
            text=voter_counts
        )
        participation_fig.update_traces(textposition='outside')
        max_count = max(voter_counts) if voter_counts else 0
        participation_fig.update_yaxes(range=[0, max_count + 1])
        context['participation_chart'] = mark_safe(participation_fig.to_html(full_html=False))

        context['years'] = range(1900, 2025)
        return context

class HomeView(TemplateView):
    """
    Renders the static homepage of the application.
    """
    template_name = 'voter_analytics/home.html'
