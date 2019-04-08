from django.urls import path

from . import views

app_name='media'

urlpatterns = [
    path('', views.index, name='index'),
    path('source/list', views.source_list, name='source_list'),
    path('source/edit/<int:source_id>', views.source_edit, name='source_edit'),
    path('source/add', views.source_add, name='source_add'),
    path('source/upsert', views.source_upsert, name='source_upsert')
]
