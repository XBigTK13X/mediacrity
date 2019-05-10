from django.urls import path

from .views import storage
from .views import source
from .views import job

app_name='media'

urlpatterns = [
    path('source/list', source.list, name='source_list'),
    path('source/add', source.add, name='source_add'),
    path('source/insert', source.insert, name='source_insert'),
    path('source/<int:source_id>/update', source.update, name='source_update'),
    path('source/<int:source_id>/edit', source.edit, name='source_edit'),
    path('source/<int:source_id>/sync', source.sync, name='source_sync'),

    path('job/<int:job_id>', job.status, name='job_status'),

    path('storage/list', storage.list, name='storage_list'),
    path('storage/add', storage.add, name='storage_add'),
    path('storage/insert', storage.insert, name='storage_insert'),
    path('storage/<int:storage_id>/update', storage.update, name='storage_update'),
    path('storage/<int:storage_id>/edit', storage.edit, name='storage_edit'),
    path('storage/<int:storage_id>/mount', storage.mount, name='storage_mount'),
    path('storage/<int:storage_id>/unmount', storage.unmount, name='storage_unmount')
]
