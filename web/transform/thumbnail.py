import os
import subprocess
import hashlib
from common import ioutil
from transform import transcode
from web import settings
from common import orm
import shutil

def get_path(source, media):
    transform_dir = orm.transform_dir('thumbnail', source.legacy_v1_id)
    transform_path = ioutil.path(transform_dir, f"{media.content_hash}.png")
    return transform_path

def generate(job, source, media):
    media.thumbnail_path = get_path(source, media)
    media.save()
    if not ioutil.cached(media.thumbnail_path):
        input_path = media.server_path
        output_path = media.thumbnail_path
        if ioutil.cached(output_path):
            return output_path

        if transcode.is_video(input_path):
            video(job, input_path, output_path)
        else:
            image(job, input_path, output_path)

def fail(result, input_path, output_path, command):
    if result != 0 or not os.path.isfile(output_path):
        print(f"A thumbnail error occurred when converting [{input_path}] to [{output_path}]. See command below")
        print(f"cmd: [{command}]")
        raise Exception("Unable to generate thumbnail from {input_path} to {output_path}")


def video(job, input_path, output_path):
    fail_safe = 10
    frame = 0
    temp_path = output_path.replace('.png', '.tmp.png')
    script_path = f"{settings.SCRIPT_DIR}/transform/thumbnail-video.sh"
    cwd =  f"{settings.SCRIPT_DIR}/transform"
    while fail_safe > 0:
        command = f"{script_path} {frame} {input_path} {temp_path} {settings.SUPPRESS_TRANSCODE_LOGGING}"
        orm.job_log(job, f"Running command {command}")
        process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = process.communicate()
        result = process.returncode
        if result == 0 and os.path.isfile(temp_path):
            orm.job_log(job, f"stdout: {stdout}")
            orm.job_log(job, f"stderr: {stderr}")
            shutil.move(temp_path, output_path)
        else:
            if fail_safe == 10:
                orm.job_log(job, f"stdout: {stdout}")
                orm.job_log(job, f"stderr: {stderr}")
                orm.job_fail(result, job, f"An error occurred when generating thumbnail for [{input_path}]")
                return fail(result, input_path, output_path, command)
            else:
                return
        frame += 5
        fail_safe -= 1

def image(job, input_path, output_path):
    script_path = f"{settings.SCRIPT_DIR}/transform/thumbnail-image.sh"
    cwd =  f"{settings.SCRIPT_DIR}/transform"
    command = f"{script_path} {input_path} {output_path}"
    orm.job_log(job, f"Running command {command}")
    process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = process.communicate()
    result = process.returncode
    if result != 0:
        orm.job_log(job, f"stdout: {stdout}")
        orm.job_log(job, f"stderr: {stderr}")
        orm.job_fail(result, job, f"An error occurred when generating thumbnail for [{input_path}]")
        return fail(result, input_path, output_path, command)
