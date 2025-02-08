from django.shortcuts import render

# Create your views here.
import random

def main_page(request):
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
    return render(request, 'quotes/about.html')
        