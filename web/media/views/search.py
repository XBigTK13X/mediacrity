from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.db.models import Q

from ..models import *

import message.read

@login_required
def find(request):
    return HttpResponseRedirect(reverse('media:search_results', args=(request.POST['query'],)))

@login_required
def results(request, query):
    terms = None
    if query == None or query == "":
        return render(request, 'media/search_results.html',{})
    terms = query.split(' ')
    source_query = Q()
    media_query = Q()
    job_query = Q()
    for term in terms:
        if isinstance(term, int):
            source_query = source_query | Q(id=term) | Q(legacy_v1_id=term)
            media_query = media_query | Q(id=term) | Q(content_hash=term)
            job_query = job_query | Q(id=term) | Q(source_id=term) | Q(media_id=term)
        else:
            source_query = source_query | Q(legacy_v1_id=term) | Q(name__icontains=term) | Q(description__icontains=term) | Q(origin_path__icontains=term)
            media_query = media_query | Q(content_hash=term) | Q(extract_path__icontains=term)
            job_query = job_query | Q(logs__icontains=term)

    sources = Source.objects.filter(source_query).order_by('id').all()
    media = Media.objects.filter(media_query).order_by('id').all()
    jobs = Job.objects.filter(job_query).order_by('-id').all()

    context = {
        'sources': sources,
        'media': media,
        'jobs': jobs
    }
    return render(request, 'media/search_results.html', context)
