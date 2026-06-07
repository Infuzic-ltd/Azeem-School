from django import template

register = template.Library()


@register.filter
def absolute_url(url):
    """Ensure a URL is site-absolute (starts with /, http://, or https://)."""
    if not url:
        return url
    url = url.strip()
    if url.startswith(('/', 'http://', 'https://', '#', 'mailto:', 'tel:')):
        return url
    return '/' + url
