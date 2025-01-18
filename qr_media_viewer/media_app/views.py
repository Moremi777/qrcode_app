from django.shortcuts import render, redirect
from django.conf import settings
from .models import MediaFile
import qrcode
import os

def index(request):
    return render(request, 'index.html')

def upload_media(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        media = MediaFile(file=uploaded_file)
        media.save()

        # Generate QR Code
        qr_url = request.build_absolute_uri(f"/media/{media.file}")
        qr_image = qrcode.make(qr_url)

        qr_path = os.path.join(settings.MEDIA_ROOT, 'qrcodes', f"{media.id}.png")
        os.makedirs(os.path.dirname(qr_path), exist_ok=True)
        qr_image.save(qr_path)

        media.qr_code = f"qrcodes/{media.id}.png"
        media.save()

        return render(request, 'upload.html', {'media': media})

    return render(request, 'upload.html')

def view_media(request, media_id):
    media = get_object_or_404(MediaFile, id=media_id)
    return render(request, 'media.html', {'media': media})