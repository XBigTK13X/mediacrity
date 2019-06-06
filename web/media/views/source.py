from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from media.models import *
from django.db.models import Count
import logging
import message.write

logger = logging.getLogger('debug')

@login_required
def list(request, mode="populated"):
    sources = None
    if mode == 'all':
        sources = Source.objects
    elif mode == 'empty':
        sources = Source.objects.filter(media__source__isnull=True)
    else:
        sources = Source.objects.filter(media__source__isnull=False)
    context = {
        'sources': sources.select_related().annotate(media_count=Count('id')).order_by('id').all(),
        'mode': mode
    }
    return render(request, 'media/source_list.html', context)

@login_required
def add(request):
    context = {
        'source_kinds': SourceKind.objects.all()
    }
    return render(request, 'media/source_add.html', context)

@login_required
def insert(request):
    instance = Source.objects.create(
        kind_id = request.POST['kind'],
        name = request.POST['name'],
        description = request.POST['description'],
        origin_path = request.POST['path']
    )
    return HttpResponseRedirect(reverse('media:source_edit', args=(instance.id,)))

@login_required
def edit(request, source_id):
    source = Source.objects.select_related().get(id=source_id)
    jobs = Job.objects.select_related().filter(source_id=source).order_by('-created')
    media = Media.objects.filter(source_id=source).order_by('sort_order')
    album = None
    try:
        album = Album.objects.get(generated_by_source_v1_id=source.legacy_v1_id)
    except:
        swallow = True
    context = {
        'source': source,
        'jobs': jobs,
        'media': media,
        'album': album
    }
    return render(request, 'media/source_edit.html', context)

@login_required
def update(request, source_id):
    instance = Source.objects.get(id=source_id)
    instance.name = request.POST['name']
    instance.description = request.POST['description']
    instance.save()
    return HttpResponseRedirect(reverse('media:source_edit', args=(instance.id,)))

@login_required
def sync(request, source_id):
    source = Source.objects.get(id=source_id)
    kind = SourceKind.objects.get(id=source.kind_id)
    handler = None
    if kind.name == "reddit-saves":
        handler = 'extract-reddit-saves'
    elif kind.name == "ripme":
        handler = 'extract-ripme-link'
    elif kind.name == 'imgur':
        handler = 'extract-imgur-link'
    elif kind.name == 'reddit-post':
        handler = 'extract-reddit-post'
    elif kind.name == 'youtube-dl':
        handler = 'extract-youtube-dl-link'
    elif kind.name == 'file-system-root':
        handler = 'extract-file-system-root'
    elif kind.name == 'file-system-directory':
        handler = 'extract-file-system-directory'
    job_id = message.write.send(
        source_id=source_id,
        handler=handler
    )
    return HttpResponseRedirect(reverse('media:job_view', args=(job_id,)))

@login_required
def delete(request, source_id):
    if source_id == None:
        raise "A source id must be provided"
    Source.objects.filter(id=source_id).delete()
    return HttpResponseRedirect(reverse('media:source_list'))
