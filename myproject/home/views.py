from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from .models import AboutPage, AdmissionsPage, ContactPage


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
            "first_name": request.POST.get("first_name", "").strip(),
            "last_name":  request.POST.get("last_name",  "").strip(),
            "email":      request.POST.get("email",      "").strip(),
            "phone":      request.POST.get("phone",      "").strip(),
            "dob":        request.POST.get("dob",        "").strip(),
            "country":    request.POST.get("country",    "").strip(),
            "program":    request.POST.get("program",    "").strip(),
            "education":  request.POST.get("education",  "").strip(),
            "message":    request.POST.get("message",    "").strip(),
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
        if not data["program"]:
            errors["program"] = "Please select a program."
        if not data["education"]:
            errors["education"] = "Please select your education level."

        if errors:
            context["errors"] = errors
        else:
            # ── Send email to sales / admissions team ──
            sales_email = getattr(settings, "ADMISSIONS_SALES_EMAIL", "admissions@educiza.com")
            subject = f"New Admission Application — {data['first_name']} {data['last_name']}"
            body = f"""New admission application received.

Name:       {data['first_name']} {data['last_name']}
Email:      {data['email']}
Phone:      {data['phone']}
DOB:        {data['dob'] or 'Not provided'}
Country:    {data['country'] or 'Not provided'}
Program:    {data['program']}
Education:  {data['education']}

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
                context["form_data"] = {}  # clear form on success
            except Exception as exc:
                context["error"] = (
                    "Your application could not be sent at this time. "
                    "Please email us directly at admissions@educiza.com."
                )

    return render(request, "home/admissions.html", context)


def admissions_view2(request):
    page = AdmissionsPage.objects.live().first()
    context = {"page": page, "success": False, "error": None, "form_data": {}, "errors": {}}

    if request.method == "POST":
        data = {
            "first_name": request.POST.get("first_name", "").strip(),
            "last_name":  request.POST.get("last_name",  "").strip(),
            "email":      request.POST.get("email",      "").strip(),
            "phone":      request.POST.get("phone",      "").strip(),
            "dob":        request.POST.get("dob",        "").strip(),
            "country":    request.POST.get("country",    "").strip(),
            "program":    request.POST.get("program",    "").strip(),
            "education":  request.POST.get("education",  "").strip(),
            "message":    request.POST.get("message",    "").strip(),
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
        if not data["program"]:
            errors["program"] = "Please select a program."
        if not data["education"]:
            errors["education"] = "Please select your education level."

        if errors:
            context["errors"] = errors
        else:
            # ── Send email to sales / admissions team ──
            sales_email = getattr(settings, "ADMISSIONS_SALES_EMAIL", "admissions@educiza.com")
            subject = f"New Admission Application — {data['first_name']} {data['last_name']}"
            body = f"""New admission application received.

Name:       {data['first_name']} {data['last_name']}
Email:      {data['email']}
Phone:      {data['phone']}
DOB:        {data['dob'] or 'Not provided'}
Country:    {data['country'] or 'Not provided'}
Program:    {data['program']}
Education:  {data['education']}

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
                context["form_data"] = {}  # clear form on success
            except Exception as exc:
                context["error"] = (
                    "Your application could not be sent at this time. "
                    "Please email us directly at admissions@educiza.com."
                )

    return render(request, "home/admissions_2.html", context)