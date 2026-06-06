from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.mail import EmailMessage
from django.conf import settings
from wagtail.documents import get_document_model
import cloudinary
import cloudinary.utils
from .models import AboutPage, AdmissionsPage, ContactPage, AcademicsPage, FacilitiesPage, NewsPage


def news_view(request):
    page = NewsPage.objects.live().first()
    return render(request, "home/news.html", {"page": page})

def news_view2(request):
    return render(request, "home/newsv1.html")


def about_view(request):
    page = AboutPage.objects.live().first()
    return render(request, "home/about.html", {"page": page})


def contact_view(request):
    page = ContactPage.objects.live().first()
    return render(request, "home/contact.html", {"page": page})


def admissions_view(request):
    page = AdmissionsPage.objects.live().first()
    context = {"page": page, "success": False, "error": None, "form_data": {}, "errors": {}}

    if request.method == "POST":
        data = {
            "first_name":  request.POST.get("first_name",  "").strip(),
            "last_name":   request.POST.get("last_name",   "").strip(),
            "email":       request.POST.get("email",       "").strip(),
            "phone":       request.POST.get("phone",       "").strip(),
            "dob":         request.POST.get("dob",         "").strip(),
            "campus":      request.POST.get("campus",      "").strip(),
            "board":       request.POST.get("board",       "").strip(),
            "class_level": request.POST.get("class_level", "").strip(),
            "message":     request.POST.get("message",     "").strip(),
        }
        context["form_data"] = data

        # ── Validation ────────────────────────
        errors = {}
        if not data["first_name"]:
            errors["first_name"] = "First name is required."
        if not data["last_name"]:
            errors["last_name"] = "Last name is required."
        if not data["email"]:
            errors["email"] = "Email address is required."
        elif "@" not in data["email"]:
            errors["email"] = "Enter a valid email address."
        if not data["phone"]:
            errors["phone"] = "Phone number is required."
        if not data["campus"]:
            errors["campus"] = "Please select a campus."
        if not data["board"]:
            errors["board"] = "Please select a board."
        if not data["class_level"]:
            errors["class_level"] = "Please select a class."

        if errors:
            context["errors"] = errors
        else:
            sales_email = getattr(settings, "ADMISSIONS_SALES_EMAIL", "admissions@educiza.com")
            subject = f"New Admission Application — {data['first_name']} {data['last_name']}"
            body = f"""New admission application received.

Name:        {data['first_name']} {data['last_name']}
Email:       {data['email']}
Phone:       {data['phone']}
DOB:         {data['dob'] or 'Not provided'}
Campus:      {data['campus']}
Board:       {data['board']}
Class:       {data['class_level']}

Message / Goals:
{data['message'] or 'None'}
"""
            try:
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@educiza.com"),
                    to=[sales_email],
                    reply_to=[data["email"]],
                )
                email.send(fail_silently=False)
                context["success"] = True
                context["form_data"] = {}
            except Exception:
                context["error"] = (
                    "Your application could not be sent at this time. "
                    "Please email us directly at admissions@educiza.com."
                )

    return render(request, "home/admissions.html", context)


def academics_view(request):
    page = AcademicsPage.objects.live().first()
    return render(request, "home/academics.html", {"page": page})


def facilities_view(request):
    page = FacilitiesPage.objects.live().first()
    return render(request, "home/facilities.html", {"page": page})
def facilities_view2(request):
    return render(request, "home/new_home_page.html")

def homepage_preview2(request):
    return render(request, "home/new_home_page_2.html")

def academics_view2(request):
    page = AcademicsPage.objects.live().first()
    return render(request, "home/academics_2.html", {"page": page})


def admissions_view2(request):
    page = AdmissionsPage.objects.live().first()
    context = {"page": page, "success": False, "error": None, "form_data": {}, "errors": {}}

    if request.method == "POST":
        data = {
            "first_name":  request.POST.get("first_name",  "").strip(),
            "last_name":   request.POST.get("last_name",   "").strip(),
            "email":       request.POST.get("email",       "").strip(),
            "phone":       request.POST.get("phone",       "").strip(),
            "dob":         request.POST.get("dob",         "").strip(),
            "campus":      request.POST.get("campus",      "").strip(),
            "board":       request.POST.get("board",       "").strip(),
            "class_level": request.POST.get("class_level", "").strip(),
            "education":   request.POST.get("education",   "").strip(),
            "message":     request.POST.get("message",     "").strip(),
        }
        context["form_data"] = data

        errors = {}
        if not data["first_name"]:
            errors["first_name"] = "First name is required."
        if not data["last_name"]:
            errors["last_name"] = "Last name is required."
        if not data["email"]:
            errors["email"] = "Email address is required."
        elif "@" not in data["email"]:
            errors["email"] = "Enter a valid email address."
        if not data["phone"]:
            errors["phone"] = "Phone number is required."
        if not data["campus"]:
            errors["campus"] = "Please select a campus."
        if not data["board"]:
            errors["board"] = "Please select a board."
        if not data["class_level"]:
            errors["class_level"] = "Please select a class."
        if not data["education"]:
            errors["education"] = "Please select your education level."

        if errors:
            context["errors"] = errors
        else:
            sales_email = getattr(settings, "ADMISSIONS_SALES_EMAIL", "admissions@educiza.com")
            subject = f"New Admission Application — {data['first_name']} {data['last_name']}"
            body = f"""New admission application received.

Name:        {data['first_name']} {data['last_name']}
Email:       {data['email']}
Phone:       {data['phone']}
DOB:         {data['dob'] or 'Not provided'}
Campus:      {data['campus']}
Board:       {data['board']}
Class:       {data['class_level']}
Education:   {data['education']}

Message / Goals:
{data['message'] or 'None'}
"""
            try:
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@educiza.com"),
                    to=[sales_email],
                    reply_to=[data["email"]],
                )
                email.send(fail_silently=False)
                context["success"] = True
                context["form_data"] = {}
            except Exception:
                context["error"] = (
                    "Your application could not be sent at this time. "
                    "Please email us directly at admissions@educiza.com."
                )

    return render(request, "home/admissions_2.html", context)


def document_download(request, doc_id):
    from .models import AcademicDownload
    try:
        dl = AcademicDownload.objects.get(pk=doc_id)
    except AcademicDownload.DoesNotExist:
        raise Http404

    if not dl.document:
        raise Http404

    cloudinary.config(
        cloud_name=settings.CLOUDINARY_STORAGE["CLOUD_NAME"],
        api_key=settings.CLOUDINARY_STORAGE["API_KEY"],
        api_secret=settings.CLOUDINARY_STORAGE["API_SECRET"],
        secure=True,
    )
    signed_url = cloudinary.utils.private_download_url(
        dl.document.name,
        "",
        resource_type="raw",
        type="upload",
        attachment=True,
    )
    return HttpResponseRedirect(signed_url)
