from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.conf import settings

from ..models import Source, SourceKind, Storage, StorageKind

@login_required
def status(request, job_id):
    context = {}
    return render(request, 'media/job_status.html', context)
