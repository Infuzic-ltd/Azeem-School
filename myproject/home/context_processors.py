from .models import HomePage


def home_page_context(request):
    try:
        home_page = HomePage.objects.live().first()
    except Exception:
        home_page = None
    return {"home_page": home_page}
