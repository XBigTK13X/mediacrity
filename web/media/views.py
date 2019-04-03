from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Source, SourceKind

def index(request):
    return render(request, 'media/index.html', {})

def source_list(request):
    context = {
        'sources': Source.objects.all()
    }
    return render(request, 'media/source_list.html', context)

def source_add(request):
    context = {
        'source_kinds': SourceKind.objects.all()
    }
    return render(request, 'media/source_add.html', context)

def source_edit(request, source_id):
    context = {
        'source': Source.objects.get(id=source_id)
    }
    return render(request, 'media/source_edit.html', context)

def source_upsert(request):
    instance,created = Source.objects.update_or_create(
        kind_id = request.POST['kind'],
        name = request.POST['name'],
        description = request.POST['description'],
        origin_path = request.POST['path']
    )
    return HttpResponseRedirect(reverse('media:source_edit', args=(instance.id)))
