from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from ..models import *
from django.db.models import Q,Count
from random import randint
from media.service import storage
from django.core.paginator import Paginator

@login_required
def random(request):
    sources = Source.objects.filter(media__source__isnull=False).select_related()
    count = sources.aggregate(count=Count('id'))['count']
    random_index = randint(0, count - 1)
    source =sources.all()[random_index]
    media = Media.objects.filter(source_id=source.id)
    media_count = media.count()
    media_index = randint(0, media_count - 1)
    media = media.all()[media_index]
    return HttpResponseRedirect(reverse('media:media_edit', args=(media.id,)))

@login_required
def edit(request, media_id):
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
    return render(request, 'media/media_edit.html', context)

@login_required
def list(request, kind='all', page=1):
    media_query = Q()
    order_by = '-created'
    if kind != 'all' and kind != None:
        media_query = Q(kind__name=kind)
    media = Media.objects.select_related().filter(media_query).order_by(order_by).all()
    pager = Paginator(media, settings.MEDIA_LIST_PAGE_SIZE)
    context = {
        'media': pager.get_page(page),
        'page': page,
        'kind': kind
    }
    return render(request, 'media/media_list.html', context)

@login_required
def delete(request, media_id):
    if media_id == None:
        raise "A media id must be provided"
    media = Media.objects.select_related().filter(id=media_id).get()
    if media.extract_path != None and os.path.isfile(media.extract_path):
        os.remove(media.extract_path)
    if media.transform_path != None and os.path.isfile(media.transform_path):
        os.remove(media.transform_path)
    if media.origin_path != None and os.path.isfile(media.origin_path):
        os.remove(media.origin_path)
    source = media.source
    media.delete()
    return HttpResponseRedirect(reverse('media:source_edit', args=(source.id,)))
