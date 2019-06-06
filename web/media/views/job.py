from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.conf import settings

from ..models import Job, JobStatus

import message.read
import message.write
import json

@login_required
def view(request, job_id):
    job = Job.objects.select_related().get(id=job_id)
    job_logs = job.logs.replace('\\n','\n').split('\n')
    time_elapsed = job.updated - job.created
    context = {
        'job': job,
        'job_logs': job_logs,
        'time_elapsed': time_elapsed
    }
    return render(request, 'media/job_view.html', context)

@login_required
def list(request):
    jobs = Job.objects.select_related().exclude(status_id=1).order_by('-created').all()
    pager = Paginator(jobs, 250)
    context = {
        'jobs': pager.get_page(1),
        'message_count': message.read.count()
    }
    return render(request, 'media/job_list.html', context)

@login_required
def requeue(request, job_id):
    job = Job.objects.select_related().get(id=job_id)
    job_logs = job.logs.replace('\\n','\n').split('\n')
    # TODO The second log entry is always the payload. This should be moved to a field on the job.
    content = job_logs[1]
    content = content[2:-1]
    payload = json.loads(content)
    message.write.send(payload=payload)
    return HttpResponseRedirect(reverse('media:job_view', args=(job_id,)))
