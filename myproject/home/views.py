from django.shortcuts import render, get_object_or_404
from .models import ContactPage

def about_view(request):
    return render(request, "about_page.html")

def contact_view(request):
    page = ContactPage.objects.live().first()
    return render(request, "home/contact.html", {"page": page})