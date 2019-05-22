from django import template

register = template.Library()

from media.models import *

from web import settings

CONTENT_SERVER_ROOT = f"http://{settings.CONTENT_SERVER_HOST}:{settings.CONTENT_SERVER_PORT}"

MEDIA_STORAGE=None

@register.simple_tag
def asset(relative_path):
    return f"{CONTENT_SERVER_ROOT}/asset/{relative_path}"

@register.simple_tag
def media(path):
    global MEDIA_STORAGE
    if MEDIA_STORAGE is None:
        MEDIA_STORAGE = Storage.objects.first()
    path = path.replace(MEDIA_STORAGE.path+"/", "")
    return f"{CONTENT_SERVER_ROOT}/media/{path}"
