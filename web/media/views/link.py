from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from media.models import *
from django.db.models import Count
import logging
from common import file_cache
from django.core import serializers
import json

logger = logging.getLogger('debug')

@login_required
def list(request, mode="populated"):
    context = {
        'links': WebLink.objects.order_by('name').all()
    }
    return render(request, 'media/link_list.html', context)

@login_required
def edit(request):
    links = WebLink.objects.order_by('name').all()
    links_list = []
    for link in links:
        links_list.append({
            'name': link.name,
            'description': link.description,
            'url': link.url
        })
    links_json = json.dumps(links_list, indent=4)
    context = {
        'links_json': links_json
    }
    return render(request, 'media/link_edit.html', context)

@login_required
def update(request):
    links_json = request.POST['links-json']
    links = json.loads(links_json)
    for link in links:
        web_link = None
        try:
            web_link = WebLink.objects.get(url=link['url'])
        except ObjectDoesNotExist:
            web_link = WebLink.objects.create()
        web_link.url = link['url']
        web_link.name = link['name']
        web_link.description = link['description']
        web_link.save()
    return HttpResponseRedirect(reverse('media:link_list'))
