from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_media, name='upload'),
    path('media/<int:media_id>/', views.view_media, name='view_media'),
]
