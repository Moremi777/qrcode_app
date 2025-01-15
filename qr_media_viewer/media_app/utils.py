import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
from django.conf import settings
from .models import MediaUpload

def generate_qr_code(media_instance):
    # Generate the URL for the uploaded media
    media_url = f"{settings.MEDIA_URL}{media_instance.media.name}"

    # Create a QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(media_url)
    qr.make(fit=True)

    # Convert the QR code to an image
    img = qr.make_image(fill='black', back_color='white')

    # Save QR code to the media instance
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    media_instance.qr_code.save(f"{media_instance.media.name}_qr_code.png", ContentFile(buffer.read()), save=True)

    return media_instance

