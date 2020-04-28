from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.conf import settings

from ..models import *

import message.read

from common import debug

@login_required
def list(request):
    context = {
        'albums': Album.objects.all()
    }
    return render(request, 'media/album_list.html', context)

@login_required
def edit(request, album_id):
    # TODO Work in progress raw query for paging, there is probably a way to do this through the django API
    album = Album.objects.get(id=album_id)
    media_query = f"select m.id,m.thumbnail_path,m.content_hash,m.kind_id,m.source_id,m.byte_size from media_album a join media_album_sources as als on a.id = als.album_id join media_media m on m.source_id = als.source_id where a.id={album_id} order by als.source_id,m.sort_order;"
    media = Media.objects.raw(media_query)
    context = {
        'album': album,
        'media': media
    }
    return render(request, 'media/album_edit.html', context)

@login_required
def delete(request, album_id):
    if album_id == None:
        raise "An album id must be provided"
    Album.objects.filter(id=album_id).delete()
    return HttpResponseRedirect(reverse('media:album_list'))
