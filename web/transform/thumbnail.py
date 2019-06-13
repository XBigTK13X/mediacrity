import os
import subprocess
import hashlib
from common import ioutil
from transform import transcode
from web import settings
from common import orm
import shutil
import math

def frame_count(input_path):
    command = f"ffmpeg -i '{input_path}' -map 0:v:0 -c copy -f null -"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = process.communicate()
    result = process.returncode
    if result != 0:
        return 0
    # The third line from the end has the frame_count info
    # Using linux tools in the above command wasn't returning the reuslts properly to Python
    count = f"{stderr}".split('\\n')[-3].split("frame=")[1].split('fps=')[0].strip()
    return int(count)

def get_path(source, media):
    transform_dir = orm.transform_dir('thumbnail', source.legacy_v1_id)
    transform_path = ioutil.path(transform_dir, f"{media.content_hash}.png")
    return transform_path

def generate(job, source, media, force=False):
    if not force and ioutil.cached(media.thumbnail_path):
        return media.thumbnail_path

    media.thumbnail_path = get_path(source, media)
    media.save()

    input_path = media.server_path
    output_path = media.thumbnail_path

    if transcode.is_video(input_path):
        video(job, input_path, output_path)
    else:
        image(job, input_path, output_path)

def fail(result, input_path, output_path, command):
    if result != 0 or not os.path.isfile(output_path):
        print(f"A thumbnail error occurred when converting [{input_path}] to [{output_path}]. See command below")
        print(f"cmd: [{command}]")
        raise Exception(f"Unable to generate thumbnail from {input_path} to {output_path}")


def video(job, input_path, output_path):
    total_frames = frame_count(input_path)
    thumbnail_frame = math.floor(total_frames/2)
    temp_path = output_path.replace('.png', '.tmp.png')
    script_path = f"{settings.SCRIPT_DIR}/transform/thumbnail-video.sh"
    cwd =  f"{settings.SCRIPT_DIR}/transform"
    command = f"{script_path} {thumbnail_frame} '{input_path}' '{temp_path}' {settings.SUPPRESS_TRANSCODE_LOGGING}"
    orm.job_log(job, f"Running command {command}")
    process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = process.communicate()
    result = process.returncode
    if result == 0 and os.path.isfile(temp_path):
        orm.job_log(job, f"stdout: {stdout}")
        orm.job_log(job, f"stderr: {stderr}")
        shutil.move(temp_path, output_path)
    else:
        orm.job_log(job, f"stdout: {stdout}")
        orm.job_log(job, f"stderr: {stderr}")
        orm.job_fail(result, job, f"An error occurred when generating thumbnail for [{input_path}]")
        return fail(result, input_path, output_path, command)

def image(job, input_path, output_path):
    script_path = f"{settings.SCRIPT_DIR}/transform/thumbnail-image.sh"
    cwd =  f"{settings.SCRIPT_DIR}/transform"
    command = f"{script_path} '{input_path}' '{output_path}'"
    orm.job_log(job, f"Running command {command}")
    process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = process.communicate()
    result = process.returncode
    if result != 0:
        orm.job_log(job, f"stdout: {stdout}")
        orm.job_log(job, f"stderr: {stderr}")
        orm.job_fail(result, job, f"An error occurred when generating thumbnail for [{input_path}]")
        return fail(result, input_path, output_path, command)
