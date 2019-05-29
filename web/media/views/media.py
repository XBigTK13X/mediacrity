from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from ..models import *
from django.db.models import Q
from random import randint
from media.service import storage

@login_required
def random(request):
    sources = Source.objects.filter(media__source__isnull=False)
    source_count = sources.count()
    source_index = randint(0, source_count -1)
    source = sources.all()[source_index]
    media = Media.objects.filter(source_id=source.id)
    media_count = media.count()
    media_index = randint(0, media_count - 1)
    media = media.all()[media_index]
    return HttpResponseRedirect(reverse('media:media_view', args=(media.id,)))

@login_required
def view(request, media_id):
    media = Media.objects.select_related().get(id=media_id)
    source_media = Media.objects.filter(source_id=media.source_id).order_by('sort_order')
    next_media = None
    prev_media = None
    for index, item in enumerate(source_media):
        if item.id == media.id:
            try:
                next_media = source_media[index + 1]
            except:
                next_media = source_media.first()
            try:
                prev_media = source_media[index - 1]
            except:
                prev_media = source_media.last()
            break
    context = {
        'media': media,
        'next_media': next_media,
        'prev_media': prev_media,
        'storage_locked': storage.is_locked()
    }
    return render(request, 'media/media_view.html', context)

@login_required
def list(request, kind=None):
    media_query = Q()
    if kind != None:
        media_query = Q(kind__name=kind)
    media = Media.objects.select_related().filter(media_query).order_by('-created').all()
    context = {
        'media': media
    }
    return render(request, 'media/media_list.html', context)
