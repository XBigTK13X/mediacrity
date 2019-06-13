from django.urls import path

from .views import album
from .views import media
from .views import job
from .views import search
from .views import source
from .views import storage
from .views import link

app_name='media'

urlpatterns = [
    path('album/<int:album_id>', album.view, name='album_view'),
    path('album/list', album.list, name='album_list'),

    path('job/<int:job_id>', job.view, name='job_view'),
    path('job/list', job.list, name='job_list'),
    path('job/<int:job_id>/requeue', job.requeue, name='job_requeue'),

    path('link/edit', link.edit, name='link_edit'),
    path('link/update', link.update, name='link_update'),
    path('link/list', link.list, name='link_list'),

    path('media/<int:media_id>', media.edit, name='media_edit'),
    path('media/<int:media_id>/delete', media.delete, name="media_delete"),
    path('media/random', media.random, name="media_random"),
    path('media/list', media.list, name="media_list"),
    path('media/list?<slug:kind>', media.list, name="media_list"),
    path('media/list?<slug:kind>&<int:page>', media.list, name="media_list"),
    path('media/admin', media.admin, name='media_admin'),
    path('media/regnerate-thumbnails', media.regenerate_thumbnails, name="media_regenerate_thumbnails"),

    path('search', search.find, name='search_query'),
    path('search/<str:query>', search.results, name='search_results'),

    path('source/list', source.list, name='source_list'),
    path('source/list/<str:mode>', source.list, name='source_list'),
    path('source/add', source.add, name='source_add'),
    path('source/insert', source.insert, name='source_insert'),
    path('source/<int:source_id>/delete', source.delete, name='source_delete'),
    path('source/<int:source_id>/update', source.update, name='source_update'),
    path('source/<int:source_id>/edit', source.edit, name='source_edit'),
    path('source/<int:source_id>/sync', source.sync, name='source_sync'),

    path('storage/list', storage.list, name='storage_list'),
    path('storage/add', storage.add, name='storage_add'),
    path('storage/insert', storage.insert, name='storage_insert'),
    path('storage/<int:storage_id>/update', storage.update, name='storage_update'),
    path('storage/<int:storage_id>/edit', storage.edit, name='storage_edit'),
    path('storage/<int:storage_id>/mount', storage.mount, name='storage_mount'),
    path('storage/<int:storage_id>/unmount', storage.unmount, name='storage_unmount')
]
