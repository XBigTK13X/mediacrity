from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.conf import settings

from ..models import *

@login_required
def view(request, media_id):
    media = Media.objects.select_related().get(id=media_id)
    context = {
        'media': media
    }
    return render(request, 'media/media_view.html', context)
