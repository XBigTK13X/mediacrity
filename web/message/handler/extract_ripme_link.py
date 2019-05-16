from django.core.exceptions import ObjectDoesNotExist
from media.models import Source, SourceKind, Storage, StorageKind, Job, JobStatus, Album
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

        # TODO Have a way to mark storage as the ripme target
        storage = Storage.objects.first()
        script_path = f"{settings.SCRIPT_DIR}/ripme/ripme.sh"
        cwd =  f"{settings.SCRIPT_DIR}/ripme"
        rips_path = f"{storage.path}/ripme/{source.legacy_v1_id}"
        rips_path = ioutil.path_compact(rips_path)
        source.content_path = rips_path
        source.save()
        command = f"{script_path} {rips_path} {source.origin_path}"
        orm.job_log(job, f"Running command {command}")
        process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = process.communicate()

        result = process.returncode
        if result != 0:
            error = f"An error occurred when ripping [{source.origin_path}]\nout:{stdout}\nerr:{stderr}"
            job_status = JobStatus.objects.get(name="failed")
            job.status_id = job_status.id
            job.save()
            orm.job_log(job, error)
            raise Exception(error)
        orm.job_log(job, f"stdout: {stdout}")
        orm.job_log(job, f"stderr: {stderr}")
        orm.job_log(job, "Completed rip")
        job_status = JobStatus.objects.get(name="success")
        job.status_id = job_status.id
        job.save()
