"""
File: views.py
Author: Li Ziyang (miclilzy@bu.edu), 03/18/2025
Description: This file defines the view functions for the Quotes web application.
Each function handles rendering a specific page in the application.

Features:
- `main_page(request)`: Displays a random Ayrton Senna quote and image.
- `show_all(request)`: Displays all available Ayrton Senna quotes and images.
- `about(request)`: Displays the "About" page with background information.

Usage:
These views are mapped to URLs in `urls.py` and render the corresponding 
HTML templates with dynamically passed context data.
"""

from django.shortcuts import render

# Create your views here.
import random

def main_page(request):
    """
    View function for the main page displaying a random Ayrton Senna quote 
    and a random image.

    Returns:
        HttpResponse: Renders `quotes/quote.html` with a randomly selected quote and image.

    Context:
        - `quote` (str): A randomly chosen Ayrton Senna quote.
        - `image_url` (str): A randomly chosen image path.
    """
    quotes = [
        "Racing, competing, it's in my blood. It's part of me, it's part of my life; I have been doing it all my life and it stands out above everything else.",
        "When you are fitted in a racing car and you race to win, second or third place is not enough.",
        "You will never know the feeling of a driver when winning a race. The helmet hides feelings that cannot be understood.",
        "If you have God on your side, everything becomes clear.",
        "You must take the compromise to win, or else nothing. That means: you race or you do not.",
        "I don't know driving in another way which isn't risky. Each one has to improve himself. Each driver has its limit. My limit is a little bit further than other's.",
        "Of course there are moments that you wonder how long you should be doing it because there are other aspects which are not nice, of this lifestyle. But I just love winning."
    ]

    images = [
        "quotes/images/senna1.jpg",
        "quotes/images/senna2.jpg",
        "quotes/images/senna3.jpg",
        "quotes/images/senna4.jpg",
        "quotes/images/senna5.jpg",
        "quotes/images/senna6.jpg"
    ]

    random_quote = random.choice(quotes)
    random_image = random.choice(images)

    return render(request, 'quotes/quote.html',{
        'quote': random_quote,
        'image_url': random_image
    })

def show_all(request):
    """
    View function for displaying all available Ayrton Senna quotes and images.

    Returns:
        HttpResponse: Renders `quotes/show_all.html` with a list of quotes and images.

    Context:
        - `quotes` (list[str]): A list of Ayrton Senna quotes.
        - `images` (list[str]): A list of image paths.
    """
    quotes = [
        "Racing, competing, it's in my blood. It's part of me, it's part of my life; I have been doing it all my life and it stands out above everything else.",
        "When you are fitted in a racing car and you race to win, second or third place is not enough.",
        "You will never know the feeling of a driver when winning a race. The helmet hides feelings that cannot be understood.",
        "If you have God on your side, everything becomes clear.",
        "You must take the compromise to win, or else nothing. That means: you race or you do not.",
        "I don't know driving in another way which isn't risky. Each one has to improve himself. Each driver has its limit. My limit is a little bit further than other's.",
        "Of course there are moments that you wonder how long you should be doing it because there are other aspects which are not nice, of this lifestyle. But I just love winning."
    ]

    images = [
        "quotes/images/senna1.jpg",
        "quotes/images/senna2.jpg",
        "quotes/images/senna3.jpg",
        "quotes/images/senna4.jpg",
        "quotes/images/senna5.jpg",
        "quotes/images/senna6.jpg"
    ]

    return render(request, 'quotes/show_all.html', {'quotes': quotes, 'images': images})

def about(request):
    """
    View function for the "About" page.

    Returns:
        HttpResponse: Renders `quotes/about.html`.
    """
    return render(request, 'quotes/about.html')
        