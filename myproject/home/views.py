from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from wagtail.documents import get_document_model
import cloudinary
import cloudinary.utils
from .models import AboutPage, AdmissionsPage, ContactPage, AcademicsPage, FacilitiesPage, NewsPage, HomePage, AdmissionApplication


def home_view(request):
    page = HomePage.objects.live().first()
    return render(request, "home/home_page.html", {"page": page})


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
            import sys

            # ── 1. Save to database (must succeed) ────────────────────────────
            try:
                application = AdmissionApplication.objects.create(
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    email=data["email"],
                    phone=data["phone"],
                    dob=data["dob"],
                    campus=data["campus"],
                    board=data["board"],
                    class_level=data["class_level"],
                    message=data["message"],
                )
            except Exception as exc:
                print(f"[admissions_view] DB error: {exc}", file=sys.stderr)
                context["error"] = "Your application could not be submitted right now. Please try again or contact us directly."
                return render(request, "home/admissions.html", context)

            # ── 2. Emails (failure is logged but never shown to user) ─────────
            try:
                import traceback
                from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "azeemadmissions@gmail.com")
                submitted_at = application.submitted_at.strftime("%d %b %Y, %I:%M %p")
                email_ctx = {**data, "submitted_at": submitted_at}

                owner_email = (page.form_contact_email if page else None) or \
                              getattr(settings, "ADMISSIONS_SALES_EMAIL", "azeemadmissions@gmail.com")
                owner_html = render_to_string("home/emails/admission_owner.html", email_ctx)
                send_mail(
                    subject=f"New Admission Application — {data['first_name']} {data['last_name']}",
                    message=f"New application from {data['first_name']} {data['last_name']} ({data['email']}) for {data['class_level']}.",
                    from_email=from_email,
                    recipient_list=[owner_email],
                    html_message=owner_html,
                    fail_silently=False,
                )

                applicant_ctx = {
                    **data,
                    "contact_phone":   page.footer_contact_phone if page else "",
                    "contact_email":   page.footer_contact_email if page else "",
                    "contact_address": page.footer_contact_address if page else "",
                }
                applicant_html = render_to_string("home/emails/admission_applicant.html", applicant_ctx)
                send_mail(
                    subject="Application Received — Azeem School",
                    message=(
                        f"Dear {data['first_name']},\n\n"
                        "Thank you for applying to Azeem School. We have received your application "
                        f"for {data['class_level']} and our team will contact you within 24–48 hours.\n\n"
                        "Visit us: https://azeem-school.vercel.app/"
                    ),
                    from_email=from_email,
                    recipient_list=[data["email"]],
                    html_message=applicant_html,
                    fail_silently=False,
                )

            except Exception as exc:
                print(f"[admissions_view] email error: {exc}\n{traceback.format_exc()}", file=sys.stderr)
                context["email_debug"] = str(exc)

            context["success"] = True
            context["form_data"] = {}

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
            import sys

            try:
                application = AdmissionApplication.objects.create(
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    email=data["email"],
                    phone=data["phone"],
                    dob=data["dob"],
                    campus=data["campus"],
                    board=data["board"],
                    class_level=data["class_level"],
                    message=data["message"],
                )
            except Exception as exc:
                print(f"[admissions_view2] DB error: {exc}", file=sys.stderr)
                context["error"] = "Your application could not be submitted right now. Please try again or contact us directly."
                return render(request, "home/admissions_2.html", context)

            try:
                import traceback
                from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "azeemadmissions@gmail.com")
                submitted_at = application.submitted_at.strftime("%d %b %Y, %I:%M %p")
                email_ctx = {**data, "submitted_at": submitted_at}

                owner_email = (page.form_contact_email if page else None) or \
                              getattr(settings, "ADMISSIONS_SALES_EMAIL", "azeemadmissions@gmail.com")
                owner_html = render_to_string("home/emails/admission_owner.html", email_ctx)
                send_mail(
                    subject=f"New Admission Application — {data['first_name']} {data['last_name']}",
                    message=f"New application from {data['first_name']} {data['last_name']} ({data['email']}) for {data['class_level']}.",
                    from_email=from_email,
                    recipient_list=[owner_email],
                    html_message=owner_html,
                    fail_silently=False,
                )

                applicant_ctx = {
                    **data,
                    "contact_phone":   page.footer_contact_phone if page else "",
                    "contact_email":   page.footer_contact_email if page else "",
                    "contact_address": page.footer_contact_address if page else "",
                }
                applicant_html = render_to_string("home/emails/admission_applicant.html", applicant_ctx)
                send_mail(
                    subject="Application Received — Azeem School",
                    message=(
                        f"Dear {data['first_name']},\n\n"
                        "Thank you for applying to Azeem School. We have received your application "
                        f"for {data['class_level']} and our team will contact you within 24–48 hours.\n\n"
                        "Visit us: https://azeem-school.vercel.app/"
                    ),
                    from_email=from_email,
                    recipient_list=[data["email"]],
                    html_message=applicant_html,
                    fail_silently=False,
                )

            except Exception as exc:
                print(f"[admissions_view2] email error: {exc}\n{traceback.format_exc()}", file=sys.stderr)
                context["email_debug"] = str(exc)

            context["success"] = True
            context["form_data"] = {}

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
