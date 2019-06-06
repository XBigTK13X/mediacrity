from django.db import models
import datetime
from common import ioutil
from web import settings
import os
import urllib

class StorageKind(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    mount_script_path = models.CharField(max_length=1024,blank=True,null=True)
    unmount_script_path = models.CharField(max_length=1024,blank=True,null=True)

class Storage(models.Model):
    kind = models.ForeignKey(StorageKind, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    path = models.CharField(max_length=1024)
    mount_arguments = models.CharField(max_length=1024,blank=True,null=True)
    unmount_arguments = models.CharField(max_length=1024,blank=True,null=True)

    @property
    def locked(self):
        return len([x for x in self.contents if 'ECRYPTFS' in x]) > 0

    @property
    def contents(self):
        return os.listdir(self.path)

class SourceKind(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)

class Source(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    kind = models.ForeignKey(SourceKind, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    origin_path = models.CharField(max_length=1024)
    content_path = models.CharField(max_length=1024)
    discussion_path = models.CharField(max_length=1024)
    legacy_order = models.IntegerField(blank=True, null=True)
    legacy_v1_id = models.CharField(max_length=1024)
    legacy_v2_id = models.CharField(max_length=1024)
    sort_order = models.IntegerField(blank=True, null=True)

class MediaKind(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)

class Media(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    content_hash = models.CharField(max_length=128)
    origin_path = models.CharField(max_length=1024, blank=True, null=True)
    extract_path = models.CharField(max_length=1024)
    transform_path = models.CharField(max_length=1024)
    load_path = models.CharField(max_length=1024)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    sort_order = models.IntegerField(blank=True, null=True)
    thumbnail_path = models.CharField(max_length=1024)
    hidden = models.BooleanField(default=False)
    byte_size = models.IntegerField(blank=True, null=True)
    kind = models.ForeignKey(MediaKind, on_delete=models.CASCADE, blank=True, null=True)
    file_created = models.DateTimeField(blank=True, null=True)

    @property
    def extension(self):
        return ioutil.extension(self.server_path)

    @property
    def server_path(self):
        if self.transform_path != None and self.transform_path != "":
            return self.transform_path
        if self.extract_path != None and self.extract_path != "":
            return self.extract_path
        return self.origin_path

    @property
    def original_file_path(self):
        if self.origin_path != None and not 'http' in self.origin_path:
            return self.origin_path
        return self.extract_path

    @property
    def web_content_path(self):
        return urllib.parse.quote(self.server_path)

    @property
    def web_thumbnail_path(self):
        return urllib.parse.quote(self.thumbnail_path)

class Album(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    sources = models.ManyToManyField(Source)
    media = models.ManyToManyField(Media)
    albums = models.ManyToManyField("self", blank=True)
    generated_by_source_v1_id = models.CharField(max_length=1024, blank=True, null=True)

class WebLink(models.Model):
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    url = models.CharField(max_length=1024)

class Tag(models.Model):
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    sources = models.ManyToManyField(Source)
    media = models.ManyToManyField(Media)
    album = models.ManyToManyField(Album)

class JobStatus(models.Model):
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)

class Job(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(JobStatus, on_delete=models.CASCADE)
    logs = models.TextField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE, blank=True, null=True)
    media = models.ForeignKey(Media, on_delete=models.CASCADE, blank=True, null=True)
