from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from media.models import Source, SourceKind, Storage, StorageKind
import logging
import message.write

logger = logging.getLogger('debug')

@login_required
def list(request):
    context = {
        'sources': Source.objects.all()
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
    source = Source.objects.get(id=source_id)
    context = {
        'source': source,
        'source_kind': SourceKind.objects.get(id=source.kind_id)
    }
    return render(request, 'media/source_edit.html', context)

@login_required
def update(request, source_id):
    instance = Source.objects.get(id=source_id)
    instance.name = request.POST['name']
    instance.description = request.POST['description']
    instance.origin_path = request.POST['path']
    if 'discussion_path' in request.POST:
        instance.discussion_path = request.POST['discussion_path']
    instance.save()
    return HttpResponseRedirect(reverse('media:source_edit', args=(instance.id,)))

@login_required
def sync(request, source_id):
    job_id = message.write.send(
        source_id=source_id,
        handler='extract_reddit_saves'
    )
    source = Source.objects.get(id=source_id)
    kind = SourceKind.objects.get(id=source.kind_id)
    return HttpResponseRedirect(reverse('media:job_status', args=(job_id,)))
