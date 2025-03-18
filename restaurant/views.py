"""
File: views.py
Author: Li Ziyang (miclilzy@bu.edu), 03/18/2025
Description: This file defines the view functions for the Restaurant web application.
Each function handles rendering a specific page and managing user interactions.

Features:
- `main(request)`: Renders the main page.
- `order(request)`: Displays the order page and assigns a daily special.
- `confirmation(request)`: Processes the order form, calculates total price, and 
  provides an estimated order ready time.

Usage:
These views are mapped to URLs in `urls.py` and render the corresponding 
HTML templates with dynamically passed context data.
"""

from django.shortcuts import render
import random
import time
from datetime import datetime, timedelta

# Main page view
def main(request):
    """
    View function for the main page.

    Returns:
        HttpResponse: Renders `restaurant/main.html`.
    """
    return render(request, 'restaurant/main.html')

# Order Page view
def order(request):
    """
    View function for the order page.

    - Selects a random daily special from a predefined list.
    - Stores "Today's Special" in the session to persist it across views.
    - Passes the selected daily special to the template.

    Returns:
        HttpResponse: Renders `restaurant/order.html` with the daily special in context.
    
    Context:
        - `daily_special_random` (str): The randomly selected daily special.
    """
    daily_specials = ["Fluffy Cloud Yumberry", "Fluffy Cloud Mango", "Fluffy Cloud Crisp Grape", "Fluffy Cloud Strawberry"]
    daily_special_random = random.choice(daily_specials)

    # Store "Today's Special" in session to persist it across views
    request.session["daily_special"] = daily_special_random  

    context = {"daily_special_random": daily_special_random}
   
    return render(request, "restaurant/order.html", context)

# Confirmation Page view
def confirmation(request):
    """
    View function for the order confirmation page.

    - Processes customer order details submitted via POST request.
    - Retrieves menu items and extras, calculates total price.
    - Generates an estimated ready time for the order.
    - Passes order details to the confirmation template.

    Returns:
        HttpResponse: 
            - Renders `restaurant/confirmation.html` with order details if POST request.
            - Redirects back to `restaurant/order.html` if accessed without POST.

    Context:
        - `name` (str): Customer's name.
        - `email` (str): Customer's email.
        - `menu` (list[str]): Selected menu items.
        - `daily_special` (str): Selected daily special (if chosen).
        - `extras` (list[str]): Selected extras.
        - `total_price` (str): Formatted total price of the order.
        - `ready_time` (str): Estimated time when the order will be ready.
        - `instructions` (str): Special instructions provided by the customer.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        menu = request.POST.getlist("items")  # Ensure correct input name
        instructions = request.POST.get("instructions", "")

        # Retrieve "Today's Special" from session
        daily_special = request.session.get("daily_special", "")

        # Prices dictionary
        prices = {
            "Cloud Matcha Latte": 7.99,
            "Brown Sugar Boba": 7.99,
            "Coco Water Matcha": 7.99,
            "Coco Water Jasmine": 7.99,
            "Match Bobo shake": 7.99,
            "Hot Supreme Matcha Latte": 8.99,
            "Hot Matcha Jasmine Latte": 6.99,
            "Fluffy Cloud Yumberry": 8.99,
            "Fluffy Cloud Mango": 8.99,
            "Fluffy Cloud Crisp Grape": 8.99,
            "Fluffy Cloud Strawberry": 8.99,
        }

        # Ensure "Today's Special" is included if selected
        if daily_special and daily_special in prices and daily_special in menu:
            menu.append(daily_special)

        # Extras prices
        extras = request.POST.getlist("extras")
        extras_prices = {
            "Boba Pearls": 1.00,
            "Grass Jelly": 1.00,
        }

        # Calculate total price
        total_price = sum(prices.get(item, 0) for item in menu) + sum(extras_prices.get(extra, 0) for extra in extras)

        # Order ready time
        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))

        # Store data in context
        context = {
            "name": name,
            "email": email,
            "menu": menu,
            "daily_special": daily_special if daily_special in menu else None,  # Show "Today's Special" only if selected
            "extras": extras,
            "total_price": f"${total_price:.2f}",  # Format price correctly
            "ready_time": ready_time.strftime("%I:%M %p"),
            "instructions": instructions,
        }

        return render(request, "restaurant/confirmation.html", context)
    
    return render(request, "restaurant/order.html")
