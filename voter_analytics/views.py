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
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
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
        context = super().get_context_data(**kwargs)
        context['years'] = range(1900, 2025)  # for dropdown
        return context


class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class GraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
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
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        #
        # 1) Year-of-birth histogram
        #
        yob_counts = voters.values_list('date_of_birth__year', flat=True)
        yob_fig = px.histogram(
            x=yob_counts,
            nbins=40,
            title="Voters by Year of Birth"
        )
        context['yob_chart'] = mark_safe(yob_fig.to_html(full_html=False))

        #
        # 2) Pie chart by party (no 'Other' grouping)
        #
        party_qs = voters.values('party_affiliation').annotate(count=Count('id'))
        df = pd.DataFrame(party_qs)

        if not df.empty:
            total_voters = df['count'].sum()
            # Replace blank or None with something 'Unknown'
            df['party_affiliation'] = df['party_affiliation'].fillna('').replace('', 'Unknown')
            party_labels = df['party_affiliation']
            party_values = df['count']
        else:
            total_voters = 0
            party_labels = []
            party_values = []

        party_fig = px.pie(
            values=party_values,
            names=party_labels,
            title=f"Voter Distribution by Party Affiliation (n={total_voters})"
        )
        party_fig.update_traces(textinfo='percent')
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

        # DEBUG: print to server console
        print("DEBUG participation_data:", participation_data)

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
        # Force y-axis to start at zero
        max_count = max(voter_counts) if voter_counts else 0
        participation_fig.update_yaxes(range=[0, max_count + 1])

        context['participation_chart'] = mark_safe(participation_fig.to_html(full_html=False))

        context['years'] = range(1900, 2025)  # for filter form
        return context



class HomeView(TemplateView):
    template_name = 'voter_analytics/home.html'
