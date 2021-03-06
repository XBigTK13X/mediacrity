from django.core.exceptions import ObjectDoesNotExist
from media.models import *
from extract import reddit
from common import file_cache, orm, ioutil
import message.write
import datetime, json
from web import settings
import subprocess, os

def handle(job, payload):
    source_id = payload['source_id']
    source = Source.objects.get(id=source_id)
    job.source_id = source
    print(f"Tracking progress in job {job.id} for source {source_id}")
    orm.job_log(job,f"Beginning extract of URL using ripme for {source.name}.")

    if source.legacy_v1_id == None or source.legacy_v1_id == "":
        source.legacy_v1_id = file_cache.hash(source.origin_path)
        source.save()

    script_path = f"{settings.SCRIPT_DIR}/ripme/ripme.sh"
    cwd =  f"{settings.SCRIPT_DIR}/ripme"
    rips_path = orm.extract_dir('ripme', source.legacy_v1_id)
    source.content_path = rips_path
    source.save()
    command = f"{script_path} {rips_path} {source.origin_path}"
    orm.job_log(job, f"Running command {command} in {cwd}")
    process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = process.communicate()
    orm.job_log(job, f"stdout: {stdout}")
    orm.job_log(job, f"stderr: {stderr}")
    result = process.returncode
    orm.job_fail(result, job, f"An error occurred when ripping [{source.origin_path}]")
    orm.job_log(job, "Completed rip")
    job_status = JobStatus.objects.get(name="success")
    job.status_id = job_status.id
    job.save()
    child_job_id = message.write.send(
        source_id=source.id,
        handler='transform-media'
    )
    orm.job_log(job, f"Created child job {child_job_id}")
