from django.conf import settings
from ..models import *
import subprocess, os

def is_locked():
        return Storage.objects.first().locked
