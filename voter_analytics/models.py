from django.db import models
import csv
from datetime import datetime
import os
from django.conf import settings

class Voter(models.Model):
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
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}"


def load_data(csv_path=None):
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
