from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from ..models import *
import subprocess, os

@login_required
def list(request):
    context = {
        'storages': Storage.objects.all()
    }
    return render(request, 'media/storage_list.html', context)

@login_required
def add(request):
    context = {
        'storage_kinds': StorageKind.objects.all()
    }
    return render(request, 'media/storage_add.html', context)

@login_required
def insert(request):
    instance = Storage.objects.create(
        kind_id = request.POST['kind'],
        name = request.POST['name'],
        description = request.POST['description'],
        path = request.POST['path']
    )
    return HttpResponseRedirect(reverse('media:storage_edit', args=(instance.id,)))

@login_required
def edit(request, storage_id):
    storage = Storage.objects.get(id=storage_id)

    context = {
        'storage': storage
    }
    return render(request, 'media/storage_edit.html', context)

@login_required
def update(request, storage_id):
    instance = Storage.objects.get(id=storage_id)
    instance.kind_id = request.POST['kind']
    instance.name = request.POST['name']
    instance.description = request.POST['description']
    instance.path = request.POST['path']
    instance.save()
    return HttpResponseRedirect(reverse('media:storage_edit', args=(instance.id,)))

@login_required
def mount(request, storage_id):
    storage = Storage.objects.get(id=storage_id)
    storage_kind = StorageKind.objects.get(id=storage.kind_id)
    script_path = storage_kind.mount_script_path.replace("<script>", settings.SCRIPT_DIR)
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
def unmount(request, storage_id):
    storage = Storage.objects.get(id=storage_id)
    storage_kind = StorageKind.objects.get(id=storage.kind_id)
    script_path = storage_kind.unmount_script_path.replace("<script>", settings.SCRIPT_DIR)
    # TODO How to do this without being root?
    command = f"sudo {script_path} {storage.path}"
    print(f"Doing command [{command}]")
    process = subprocess.Popen(command, shell=True, cwd=os.getcwd())
    result = process.wait()
    # TODO maybe show a message if something went wrong. This usually means you unmounted something not mounted
    return HttpResponseRedirect(reverse('media:storage_edit', args=(storage_id,)))
