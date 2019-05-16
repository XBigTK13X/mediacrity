from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.conf import settings

from ..models import Job, JobStatus

@login_required
def status(request, job_id):
    job = Job.objects.get(id=job_id)
    job_status = JobStatus.objects.get(id=job.status_id)
    job_logs = job.logs.replace('\\n','\n').split('\n')
    time_elapsed = job.updated - job.created
    print(time_elapsed)
    context = {
        'job': job,
        'job_status': job_status,
        'job_logs': job_logs,
        'time_elapsed': time_elapsed
    }
    return render(request, 'media/job_status.html', context)
