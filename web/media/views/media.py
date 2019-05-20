from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from ..models import *
from random import randint

@login_required
def random(request):
    count = Media.objects.count()
    media_index = randint(0, count - 1)
    media = Media.objects.all()[media_index]
    return HttpResponseRedirect(reverse('media:media_view', args=(media.id,)))

@login_required
def view(request, media_id):
    media = Media.objects.select_related().get(id=media_id)
    context = {
        'media': media
    }
    return render(request, 'media/media_view.html', context)

@login_required
def list(request):
    media = Media.objects.order_by('-created').all()
    context = {
        'media': media
    }
    return render(request, 'media/media_list.html', context)
