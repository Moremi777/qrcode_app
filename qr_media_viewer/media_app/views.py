import qrcode
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Media
from .forms import MediaUploadForm
from django.core.files.storage import default_storage
from io import BytesIO
from PIL import Image


def media_upload(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the media
            media = form.save()

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            media_url = request.build_absolute_uri(media.get_absolute_url())  # URL for the media display page
            qr.add_data(media_url)
            qr.make(fit=True)

            # Create image
            img = qr.make_image(fill='black', back_color='white')

            # Save the QR code image
            qr_code_path = f'qr_codes/{media.id}_qr.png'
            img.save(default_storage.open(qr_code_path, 'wb'))

            # Update the media instance with the QR code
            media.qr_code = qr_code_path
            media.save()

            return redirect('media_display', media_id=media.id)
    else:
        form = MediaUploadForm()

    return render(request, 'media_upload.html', {'form': form})


def media_display(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    return render(request, 'media_display.html', {'media': media})


def landing_page(request):
    return render(request, 'landing_page.html')
