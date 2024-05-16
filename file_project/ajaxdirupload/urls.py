#file_upload/urls.py
from django.urls import re_path, path
from . import views

# namespace
app_name = "ajaxfilesupload"

urlpatterns = [
    # Upload File Without Using Model Form
    # re_path(r'^upload3/$', views.file_upload, name='file_upload'),

    # Upload Files Using Model Form
    # re_path(r'^upload2/$', views.model_form_upload, name='model_form_upload'),

    # re_path(r'^ajax_upload/$', views.ajax_upload, name='ajax_upload'),

    # View File List
    path('', views.upload_files, name='upload_files'),
    path('upload', views.upload_files, name='upload_files'),
]
