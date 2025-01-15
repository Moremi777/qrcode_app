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

from django.http import Http404
from .models import MediaFile

def display_media(request, media_name):
    try:
        # Using filter() to get a QuerySet instead of a single object
        media_files = MediaFile.objects.filter(file_name=media_name)

        # If there are multiple files, you can choose one (e.g., the first one)
        if media_files.exists():
            media_file = media_files.first()  # Or any other logic to choose one file
        else:
            raise Http404("Media file not found")

        # Handle the media file (e.g., display it)
        return render(request, 'media_display.html', {'media_file': media_file})

    except MediaFile.DoesNotExist:
        raise Http404("Media file not found")
