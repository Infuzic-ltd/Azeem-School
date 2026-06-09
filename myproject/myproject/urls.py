from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from home.views import home_view, about_view, about_view2, contact_view, admissions_view, admissions_view2, academics_view, academics_view2, facilities_view, document_download, facilities_view2, news_view, news_view2, homepage_preview2

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("about/", about_view, name="about"),
    path("about2/", about_view2, name="about2"),
    path("admissions/", admissions_view, name="admissions"),
    path("admissions2/", admissions_view2, name="admissions2"),
    path("academics/", academics_view, name="academics"),
    path("academics2/", academics_view2, name="academics2"),
    path("facilities/", facilities_view, name="facilities"),
    # path("facilitiesv1/", facilities_view2, name="facilities1"),
    path("facilitiesv1/", homepage_preview2, name="homepage_preview2"),
    path("news/", news_view, name="news"),
    path("newsv1/", news_view2, name="news"),
    path("contact/", contact_view, name="contact"),
    path("download/<int:doc_id>/", document_download, name="document_download"),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = urlpatterns + [
    path("", home_view, name="home"),          # CMS homepage — home_page.html
    path("", include(wagtail_urls)),           # Wagtail handles all other page URLs
]
