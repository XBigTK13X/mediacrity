from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from ..models import Source, SourceKind, Storage, StorageKind

import logging

logger = logging.getLogger('debug')

import subprocess, os

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
    instance.save()
    return HttpResponseRedirect(reverse('media:source_edit', args=(instance.id,)))

@login_required
def sync(request, source_id):
    logger.info("What the eff is going on?")
    instance = Source.objects.get(id=source_id)
    kind = SourceKind.objects.get(id=instance.kind_id)
    logger.info(f"Attempting to sync {kind.name}")
    if(kind.name == "reddit"):
        job_id = 100 #todo make a job
        # Step 1) Grab each reddit save and create a new 'source'
        # Step 2) If this reddit user already has an album, add those sources to it
        # Step 3) If any sources already exist, skip them
        # TODO - Would be cool to try out something like celery here.
        return HttpResponseRedirect(reverse('media:job_status', args=(job_id,)))
    else:
        return HttpResponseRedirect(reverse('media:source_edit', args=(instance.id,)))
