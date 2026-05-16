from django.shortcuts import render
from .models import AboutPage, ContactPage

def about_view(request):
    page = AboutPage.objects.live().first()
    return render(request, "home/about.html", {"page": page})

def contact_view(request):
    page = ContactPage.objects.live().first()
    return render(request, "home/contact.html", {"page": page})