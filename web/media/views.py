from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.conf import settings

from .models import Source, SourceKind, Storage, StorageKind

import subprocess, os

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
def source_insert(request):
    instance = Source.objects.create(
        kind_id = request.POST['kind'],
        name = request.POST['name'],
        description = request.POST['description'],
        origin_path = request.POST['path']
    )
    return HttpResponseRedirect(reverse('media:source_edit', args=(instance.id,)))

@login_required
def source_edit(request, source_id):
    context = {
        'source': Source.objects.get(id=source_id)
    }
    return render(request, 'media/source_edit.html', context)

@login_required
def source_update(request, source_id):
    instance = Source.objects.get(id=source_id)
    instance.kind_id = request.POST['kind']
    instance.name = request.POST['name']
    instance.description = request.POST['description']
    instance.origin_path = request.POST['path']
    instance.save()
    return HttpResponseRedirect(reverse('media:source_edit', args=(instance.id,)))

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
def storage_insert(request):
    instance = Storage.objects.create(
        kind_id = request.POST['kind'],
        name = request.POST['name'],
        description = request.POST['description'],
        path = request.POST['path']
    )
    return HttpResponseRedirect(reverse('media:storage_edit', args=(instance.id,)))

@login_required
def storage_edit(request, storage_id):
    context = {
        'storage': Storage.objects.get(id=storage_id)
    }
    return render(request, 'media/storage_edit.html', context)

@login_required
def storage_update(request, storage_id):
    instance = Storage.objects.get(id=storage_id)
    instance.kind_id = request.POST['kind']
    instance.name = request.POST['name']
    instance.description = request.POST['description']
    instance.path = request.POST['path']
    instance.save()
    return HttpResponseRedirect(reverse('media:storage_edit', args=(instance.id,)))

@login_required
def storage_mount(request, storage_id):
    storage = Storage.objects.get(id=storage_id)
    storage_kind = StorageKind.objects.get(id=storage.kind_id)
    script_path = storage_kind.mount_script_path.replace("<script>",settings.SCRIPT_DIR)
    # TODO How to do this without being root?
    command = f"sudo {script_path} {storage.path} {request.POST['password']}"
    process = subprocess.Popen(command, shell=True, cwd=os.getcwd())
    result = process.wait()
    if result != 0:
        # TODO better client facing error
        print(f"An error occurred when mounting [{storage.path}]")
        import sys
        sys.exit(1)
    return HttpResponseRedirect(reverse('media:storage_edit', args=(storage_id,)))

@login_required
def storage_unmount(request, storage_id):
    storage = Storage.objects.get(id=storage_id)
    storage_kind = StorageKind.objects.get(id=storage.kind_id)
    script_path = storage_kind.unmount_script_path.replace("<script>",settings.SCRIPT_DIR)
    # TODO How to do this without being root?
    command = f"sudo {script_path} {storage.path}"
    print(f"Doing command [{command}]")
    process = subprocess.Popen(command, shell=True, cwd=os.getcwd())
    result = process.wait()
    # TODO maybe show a message if something went wrong. This usually means you unmounted something not mounted
    return HttpResponseRedirect(reverse('media:storage_edit', args=(storage_id,)))
