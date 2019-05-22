from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.conf import settings

from ..models import *

import message.read

from common import debug

@login_required
def view(request, album_id):
    album = Album.objects.select_related().prefetch_related('sources__media_set').get(id=album_id)
    # TODO This should be doable in Django without needing to sort in Python
    sources = sorted(album.sources.all(), key=lambda x: x.sort_order if x.sort_order != None else 0)
    context = {
        'album': album,
        'sources': sources
    }
    return render(request, 'media/album_view.html', context)
