from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('upload/', views.media_upload, name='media_upload'),
    path('media/<int:media_id>/', views.media_display, name='media_display'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
