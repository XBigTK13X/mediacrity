from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from common import ioutil

import shutil

@login_required
def write(request):
    directory = request.POST['directory']
    for file in request.FILES.getlist('files'):
        source_path = file.temporary_file_path()
        file_name = file.name
        dest_path = ioutil.path(directory, file_name)
        shutil.move(source_path, dest_path)
    return render(request, 'media/file_upload.html', {})

@login_required
def upload(request):
    directory = '/'
    if 'path' in request.POST:
        directory = request.POST['path']
    dirs = ioutil.list_dirs(directory)
    dirs.insert(0,'../')
    dirs.insert(0,'/')
    context = {
        'paths': dirs,
        'directory': directory
    }
    return render(request, 'media/file_upload.html', context)
