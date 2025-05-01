# Name: Li Ziyang  
# BU Email: miclilzy@bu.edu
# File Description: Defines the database models for the circuits application, 
# including Circuit, Comment, Question, Choice, QuizAttempt, and Answer.

from django.db import models
from django.conf import settings
from django.utils import timezone

# Defines choices for the continent field used in the Circuit model.
CONTINENT_CHOICES = [
    ('AF', 'Africa'),
    ('AS', 'Asia'),
    ('EU', 'Europe'),
    ('NA', 'North America'),
    ('SA', 'South America'),
    ('OC', 'Oceania'),
    ('AN', 'Antarctica'),
]


class Circuit(models.Model):
    """Represents a Formula 1 circuit."""

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    layout_image = models.ImageField(upload_to='circuits/layouts/')
    record_lap_info = models.CharField(
        max_length=200,
        verbose_name='Record Lap Info',
        help_text='e.g. 1:27.097 – Max Verstappen (2020, Red Bull)',
        blank=True,
        default=''
    )
    introduction = models.TextField(
        verbose_name='Introduction',
        help_text='A brief intro or overview of this circuit',
        blank=True,
        default=''
    )
    fun_fact = models.TextField(
        verbose_name='Fun fact',
        help_text='Interesting fact about the circuit'
   )
    
    first_grand_prix = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='First Grand Prix Year',
        help_text='The year of the first Grand Prix held here'
    )
    number_of_laps = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Number of Laps',
        help_text='Total laps in a full race here'
    )
    circuit_length = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name='Circuit Length (km)',
        help_text='Length of one lap, in kilometers'
    )
    race_distance = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name='Race Distance (km)',
        help_text='Total race distance, in kilometers'
    )
    continent = models.CharField(
        max_length=2,
        choices=CONTINENT_CHOICES,
        default='EU',
        help_text='Continent where the circuit is located'
    )

    def __str__(self):
        """Return the circuit name for display purposes."""
        return self.name


class Comment(models.Model):
    """Represents a user comment on a circuit."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='circuit_comments'
    )
    circuit = models.ForeignKey(
        Circuit,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(
        'Rating',
        choices=[(i, f'{i} Stars') for i in range(1, 6)],
        default=5
    )

    def __str__(self):
        """Return a short summary of who commented on which circuit."""
        return f'{self.user.username} on {self.circuit.name}'


class Question(models.Model):
    """Represents a quiz question."""

    text = models.TextField()

    def __str__(self):
        """Return the first 50 characters of the question."""
        return self.text[:50]


class Choice(models.Model):
    """Represents a possible answer choice for a quiz question."""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        """Return the choice text."""
        return self.text


class QuizAttempt(models.Model):
    """Represents a user's attempt at the quiz."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_attempts'
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    score = models.IntegerField()

    def duration(self):
        """Calculate the total time taken for this quiz attempt.

        Returns:
            datetime.timedelta: The difference between end_time and start_time.
        """
        return self.end_time - self.start_time

    def formatted_duration(self):
        """Return duration as a 'MM:SS' formatted string.

        Calculates the total seconds from the duration timedelta and formats
        it into minutes and seconds.

        Returns:
            str: The duration formatted as 'MM:SS'.
        """
        total_seconds = int(self.duration().total_seconds())
        minutes, seconds = divmod(total_seconds, 60)
        return f'{minutes:02d}:{seconds:02d}'

    def __str__(self):
        """Return a summary of the attempt including user and score."""
        return f'{self.user.username} – Score: {self.score}'


class Answer(models.Model):
    """Represents a specific answer given by a user during a quiz attempt."""

    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

    def __str__(self):
        """Return correctness status (✓/✗) along with user and question info."""
        status = '✓' if self.is_correct else '✗'
        # Limit question text for brevity in admin or string representations
        return f'{self.attempt.user.username}: {self.question.text[:30]}... {status}'