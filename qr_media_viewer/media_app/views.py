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

        # Generate QR Code pointing to the uploaded media file
        qr_url = request.build_absolute_uri(media.file.url)  # Use media.file.url
        qr_image = qrcode.make(qr_url)

        qr_folder = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
        os.makedirs(qr_folder, exist_ok=True)  # Ensure the directory exists
        qr_path = os.path.join(qr_folder, f"{media.id}.png")
        qr_image.save(qr_path)

        # Update model with QR code path
        media.qr_code = f"qrcodes/{media.id}.png"
        media.save()

        print(f"QR Code Path: {qr_path}")
        print(f"QR Code URL: {media.qr_code.url}")

        return render(request, 'upload.html', {'media': media})

    return render(request, 'upload.html')

def view_media(request, media_id):
    media = get_object_or_404(MediaFile, id=media_id)
    return render(request, 'media.html', {'media': media})