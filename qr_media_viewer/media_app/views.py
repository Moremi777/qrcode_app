from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import MediaFileForm
from .utils import generate_qr_code
from .models import MediaFile

def home(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            media_instance = form.save()
            return render(request, 'index.html', {
                'form': form,
                'qr_code_url': media_instance.qr_code.url,
                'media_name': media_instance.media.name,
            })
    else:
        form = MediaFileForm()

    return render(request, 'index.html', {'form': form})

from django.shortcuts import render
from django.conf import settings
import os

def display_media(request, media_name):
    media_path = os.path.join(settings.MEDIA_ROOT, media_name)
    if os.path.exists(media_path):
        with open(media_path, 'rb') as media_file:
            # Handle file response or display media
            return HttpResponse(media_file.read(), content_type="image/jpeg")
    return HttpResponseNotFound("Media not found")


def display_media(request, media_name):
    # Decode the media_name (which is URL-encoded) and fetch the MediaFile instance
    media_instance = get_object_or_404(MediaFile, media__icontains=media_name)

    # Render the media_display.html template with the media_instance
    return render(request, 'media_display.html', {'media_instance': media_instance})
