from django import forms
from django.utils.html import format_html

from wagtail.images.forms import BaseImageForm


class CloudinaryDirectUploadWidget(forms.Widget):
    """A visible file picker that uploads straight to Cloudinary from the browser,
    paired with a hidden input holding the resulting Cloudinary public_id.

    See home/static/home/js/cloudinary_direct_upload.js for the upload logic and
    home.views.cloudinary_sign_upload for the signing endpoint.
    """

    def use_required_attribute(self, initial):
        # The bound field is a hidden input populated by JS after upload — a
        # "required" hidden input blocks form submission silently in some
        # browsers. Django's own required-field validation still applies.
        return False

    def value_from_datadict(self, data, files, name):
        return data.get(name)

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        field_id = attrs.get("id", f"id_{name}")
        return format_html(
            '<input type="hidden" name="{name}" id="{field_id}" value="{value}">'
            '<input type="file" accept="image/*" class="cloudinary-direct-input" '
            'data-cloudinary-direct="1" data-target="{field_id}">'
            '<div class="cloudinary-direct-status" data-status-for="{field_id}"></div>',
            name=name,
            field_id=field_id,
            value=value or "",
        )


class DirectUploadImageForm(BaseImageForm):
    """Wagtail image upload form whose 'file' field carries a Cloudinary
    public_id (uploaded directly from the browser) instead of raw file bytes.

    Set as WAGTAILIMAGES_IMAGE_FORM_BASE — Wagtail builds both the standalone
    "Add an image" admin page and every image chooser's "Upload" tab from this
    same form, so this one override covers every image field in the project.

    Assigning a plain string to a FileField (rather than a File/UploadedFile
    object) is standard Django behaviour and does not call Storage.save() —
    that only happens via FieldFile.save(), which we never invoke. Wagtail's
    own BaseImageForm.save() still re-derives width/height/file_size/file_hash
    by opening the file, which for Cloudinary-backed storage just fetches the
    already-uploaded asset over HTTP, so no extra metadata handling is needed
    here.
    """

    file = forms.CharField(
        widget=CloudinaryDirectUploadWidget(),
        required=True,
        help_text="Uploads directly to Cloudinary — supports files up to ~9.5MB.",
    )
