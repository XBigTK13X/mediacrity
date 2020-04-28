import os
import subprocess
import uuid

from common import ioutil, orm
from web import settings

def is_video(path):
    return ioutil.extension(path) in settings.VIDEO_FORMATS

def is_image(path):
    return ioutil.extension(path) in settings.IMAGE_FORMATS

def has_audio(input_path):
    command = f"ffprobe -v error -show_entries stream=codec_type '{input_path}' | grep -q audio"
    process = subprocess.Popen(command, shell=True, cwd=os.getcwd())
    return process.wait() == 0


def video(job, input_path, output_path):
    orm.job_log(job, f"Attempting to transcode video {input_path} to {output_path}")
    extension = ioutil.extension(input_path)
    if not has_audio(input_path):
        orm.job_log(job, f"No audio detected. Converting to webm")
        if extension == 'webm':
            return input_path
        output_path = output_path.replace('.mp4','.webm')
        if not ioutil.cached(output_path):
            animate(job, input_path, output_path)
        return output_path

    if extension == 'mp4':
        orm.job_log(job, f"Video already in web supported format")
        return input_path

    if not ioutil.cached(output_path):
        orm.job_log(job, f"Performing conversion")
        ffmpeg(job, input_path, output_path)

    return output_path

def image(job, input_path, output_path):
    script_path = f"{settings.SCRIPT_DIR}/transform/transcode-image.sh"
    cwd =  f"{settings.SCRIPT_DIR}/transform"
    command = f"{script_path} '{input_path}' '{output_path}' {settings.SUPPRESS_TRANSCODE_LOGGING}"
    orm.job_log(job, f"Running command {command}")
    process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = process.communicate()
    result = process.returncode
    if result != 0:
        orm.job_log(job, f"stdout: {stdout}")
        orm.job_log(job, f"stderr: {stderr}")
        error = f"An error occurred when transcoding media [{input_path}]"
        orm.job_fail(result, job, error)
        raise Exception(error)
    return output_path

def animate(job, input_path, output_path):
    script_path = f"{settings.SCRIPT_DIR}/transform/transcode-animation.sh"
    cwd =  f"{settings.SCRIPT_DIR}/transform"
    command = f"{script_path} '{input_path}' '{output_path}' {settings.SUPPRESS_TRANSCODE_LOGGING}"
    orm.job_log(job, f"Running command {command}")
    process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = process.communicate()
    result = process.returncode
    if result != 0:
        orm.job_log(job, f"stdout: {stdout}")
        orm.job_log(job, f"stderr: {stderr}")
        error = f"An error occurred when transcoding media [{input_path}]"
        orm.job_fail(result, job, error)
        raise Exception(error)

def ffmpeg(job, input_path, output_path, log=False):
    fallback_mode = 0
    result = -1
    script_path = f"{settings.SCRIPT_DIR}/transform/transcode-video.sh"
    cwd =  f"{settings.SCRIPT_DIR}/transform"
    # mpg and avi files seem to fail on the primary conversion method
    if not '.mpg' in input_path and not '.avi' in input_path:
        command = f"{script_path} '{input_path}' '{output_path}' {settings.SUPPRESS_TRANSCODE_LOGGING} {fallback_mode}"
        orm.job_log(job, f"Running primary command {command}")
        process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = process.communicate()
        result = process.returncode
        if result != 0:
            orm.job_log(job, f"stdout: {stdout}")
            orm.job_log(job, f"stderr: {stderr}")
            error = f"An error occurred when transcoding media [{input_path}]"

    if result != 0:
        fallback_mode = 1
        command = f"{script_path} '{input_path}' '{output_path}' {settings.SUPPRESS_TRANSCODE_LOGGING} {fallback_mode}"
        orm.job_log(job, f"Running fallback command {command}")
        process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = process.communicate()
        result = process.returncode
        if result != 0:
            orm.job_log(job, f"stdout: {stdout}")
            orm.job_log(job, f"stderr: {stderr}")
            error = f"An error occurred when transcoding media [{input_path}]"
            orm.job_fail(result, job, error)
            raise Exception(error)

    if result != 0:
        error = f"A transcoding error occurred when converting [{input_path}] to [{output_path}] - command [{command}]"
        print(error)
        raise Exception(error)
