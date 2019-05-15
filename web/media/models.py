from django.db import models

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

class SourceKind(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)

class Source(models.Model):
    kind = models.ForeignKey(SourceKind, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    origin_path = models.CharField(max_length=1024)
    content_path = models.CharField(max_length=1024)
    discussion_path = models.CharField(max_length=1024)
    legacy_order = models.IntegerField(blank=True, null=True)
    legacy_v1_id = models.CharField(max_length=1024)
    legacy_v2_id = models.CharField(max_length=1024)

class Media(models.Model):
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    content_hash = models.CharField(max_length=128)
    extract_path = models.CharField(max_length=1024)
    transform_path = models.CharField(max_length=1024)
    load_path = models.CharField(max_length=1024)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    order = models.IntegerField(blank=True, null=True)
    thumbnail_path = models.CharField(max_length=1024)
    hidden = models.BooleanField(default=False)

class Album(models.Model):
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    sources = models.ManyToManyField(Source)
    media = models.ManyToManyField(Media)
    albums = models.ManyToManyField("self", blank=True)

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
