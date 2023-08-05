from django.urls import path
from . import views

urlpatterns = [
    # A simple test page
    path('sample', views.index, name='sample'),
    path('upload', views.upload_file, name='upload_file'),
    path('file/<int:file_id>', views.file_attachment, name='database_file'),
]
