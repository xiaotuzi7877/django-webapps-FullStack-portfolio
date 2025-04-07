"""
models.py

Defines the database schema and data import logic for the voter_analytics Django application.

This module includes:
- Voter: A Django model representing registered voters in Newton, MA.
- load_data: A utility function to import voter records from a CSV file into the database.
"""

from django.db import models
import csv
from datetime import datetime
import os
from django.conf import settings

class Voter(models.Model):
    """
    Represents a registered voter in Newton, Massachusetts.

    This model includes personal information, address details, party affiliation,
    precinct assignment, and historical voting participation in five elections
    (2020–2023). It also includes a computed `voter_score` representing the number
    of elections the voter participated in.

    Attributes:
        last_name (str): Voter's last name.
        first_name (str): Voter's first name.
        street_number (str): House/building number of the residential address.
        street_name (str): Street name of the residential address.
        apartment_number (str, optional): Apartment or unit number.
        zip_code (str): ZIP code of the residential address.
        date_of_birth (date): Voter's birth date.
        registration_date (date): Date the voter registered to vote.
        party_affiliation (str): 1–2 character party code (e.g., 'D', 'R', 'U').
        precinct_number (str): Assigned precinct for the voter.
        v20state (bool): Voted in the 2020 state election.
        v21town (bool): Voted in the 2021 town election.
        v21primary (bool): Voted in the 2021 primary election.
        v22general (bool): Voted in the 2022 general election.
        v23town (bool): Voted in the 2023 town election.
        voter_score (int): Total number of elections voted in (0–5).
    """
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=20, blank=True, null=True)  # you missed this!
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    registration_date = models.DateField()
    party_affiliation = models.CharField(max_length=2, blank=True, null=True)
    precinct_number = models.CharField(max_length=10)

    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    voter_score = models.IntegerField(default=0)

    def __str__(self):
        """
        Returns a readable representation of the voter.
        """
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}"


def load_data(csv_path=None):
    """
    Imports voter data from a CSV file and creates Voter instances in the database.

    Args:
        csv_path (str, optional): Path to the CSV file. If not provided,
                                  defaults to a project-relative path.
    """
    if csv_path is None:
        csv_path = os.path.join(settings.BASE_DIR, 'voter_analytics', 'newton_voter_data.csv')

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Voter.objects.create(
                last_name=row['Last Name'].strip(),
                first_name=row['First Name'].strip(),
                street_number=row['Residential Address - Street Number'],
                street_name=row['Residential Address - Street Name'],
                apartment_number=row.get('Residential Address - Apartment Number') or None,
                zip_code=row['Residential Address - Zip Code'],
                date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                registration_date=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                party_affiliation=row['Party Affiliation'].strip(),
                precinct_number=row['Precinct Number'],
                v20state = row['v20state'].strip().lower() == 'true',
                v21town = row['v21town'].strip().lower() == 'true',
                v21primary = row['v21primary'].strip().lower() == 'true',
                v22general = row['v22general'].strip().lower() == 'true',
                v23town = row['v23town'].strip().lower() == 'true',
                voter_score=int(row['voter_score']),
            )
