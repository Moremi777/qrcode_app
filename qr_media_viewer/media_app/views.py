from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import MediaFileForm
from .utils import generate_qr_code
from .models import MediaFile

def home(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save form and generate QR code
            media_instance = form.save()
            generate_qr_code(media_instance)  # Generate QR code based on the uploaded media

            # Get the QR code URL and media name
            qr_code_url = media_instance.qr_code.url
            media_name = media_instance.media.name  # Get the media name for the URL

            return render(request, 'index.html', {'form': form, 'qr_code_url': qr_code_url, 'media_name': media_name})

    else:
        form = MediaFileForm()

    return render(request, 'index.html', {'form': form})


def display_media(request, media_name):
    # Retrieve media file by exact match on the file name
    media = get_object_or_404(MediaFile, media__icontains=media_name)
    return render(request, 'media_display.html', {'media_instance': media})
