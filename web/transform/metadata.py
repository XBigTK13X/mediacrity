import exifread
import datetime
import os

def oldest_datetime(path):
    modified = file_modified(path)
    exif = exif_created(path)
    if modified is None:
        if exif != None:
            return exif
        return modified
    if exif is None:
        if modified != None:
            return modified
        return exif
    return modified if modified < exif else exif

def file_modified(path):
    os.path.getmtime(path)

def exif_created(path):
    with open(path, 'rb') as fh:
        tags = exifread.process_file(fh)
        oldest_time = None
        for tag, entry in tags.items():
            if 'DateTime' in tag:
                current_time = datetime.datetime.strptime(str(entry), "%Y:%m:%d %H:%M:%S")
                if oldest_time is None or current_time < oldest_time:
                    oldest_time = current_time
        return oldest_time
