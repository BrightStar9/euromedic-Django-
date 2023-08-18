import os

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def read_any(file_name):
    with open(os.path.join(settings.BASE_DIR, file_name.lstrip("/"))) as f:
        return mark_safe(f.read())
