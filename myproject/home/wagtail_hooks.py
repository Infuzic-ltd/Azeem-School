from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks


@hooks.register("insert_global_admin_js")
def admin_image_compress_js():
    return format_html('<script src="{}"></script>', static("home/js/image_compress.js"))
