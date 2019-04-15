from django.urls import path

from . import views

app_name='media'

urlpatterns = [
    path('source/list', views.source_list, name='source_list'),
    path('source/edit/<int:source_id>', views.source_edit, name='source_edit'),
    path('source/add', views.source_add, name='source_add'),
    path('source/upsert', views.source_upsert, name='source_upsert'),

    path('storage/list', views.storage_list, name='storage_list'),
    path('storage/edit/<int:storage_id>', views.storage_edit, name='storage_edit'),
    path('storage/add', views.storage_add, name='storage_add'),
    path('storage/upsert', views.storage_upsert, name='storage_upsert')
]
