from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import Source, SourceKind, Storage, StorageKind

@login_required
def source_list(request):
    context = {
        'sources': Source.objects.all()
    }
    return render(request, 'media/source_list.html', context)

@login_required
def source_add(request):
    context = {
        'source_kinds': SourceKind.objects.all()
    }
    return render(request, 'media/source_add.html', context)

@login_required
def source_edit(request, source_id):
    context = {
        'source': Source.objects.get(id=source_id)
    }
    return render(request, 'media/source_edit.html', context)

@login_required
def source_upsert(request):
    instance,created = Source.objects.update_or_create(
        kind_id = request.POST['kind'],
        name = request.POST['name'],
        description = request.POST['description'],
        origin_path = request.POST['path']
    )
    return HttpResponseRedirect(reverse('media:source_edit', args=(instance.id)))

@login_required
def storage_list(request):
    context = {
        'storages': Storage.objects.all()
    }
    return render(request, 'media/storage_list.html', context)

@login_required
def storage_add(request):
    context = {
        'storage_kinds': StorageKind.objects.all()
    }
    return render(request, 'media/storage_add.html', context)

@login_required
def storage_edit(request, storage_id):
    context = {
        'storage': Storage.objects.get(id=storage_id)
    }
    return render(request, 'media/storage_edit.html', context)

@login_required
def storage_upsert(request):
    instance,created = Storage.objects.update_or_create(
        kind_id = request.POST['kind'],
        name = request.POST['name'],
        description = request.POST['description'],
        path = request.POST['path']
    )
    return HttpResponseRedirect(reverse('media:storage_edit', args=(instance.id)))
