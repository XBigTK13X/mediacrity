from django.urls import path

from . import views

app_name='media'

urlpatterns = [
    path('source/list', views.source_list, name='source_list'),
    path('source/add', views.source_add, name='source_add'),
    path('source/insert', views.source_insert, name='source_insert'),
    path('source/<int:source_id>/update', views.source_update, name='source_update'),
    path('source/<int:source_id>/edit', views.source_edit, name='source_edit'),
    path('source/<int:source_id>/sync', views.source_sync, name='source_sync'),

    path('job/<int:job_id>', views.job_status),

    path('storage/list', views.storage_list, name='storage_list'),
    path('storage/add', views.storage_add, name='storage_add'),
    path('storage/insert', views.storage_insert, name='storage_insert'),
    path('storage/<int:storage_id>/update', views.storage_update, name='storage_update'),
    path('storage/<int:storage_id>/edit', views.storage_edit, name='storage_edit'),
    path('storage/<int:storage_id>/mount', views.storage_mount, name='storage_mount'),
    path('storage/<int:storage_id>/unmount', views.storage_unmount, name='storage_unmount')
]
