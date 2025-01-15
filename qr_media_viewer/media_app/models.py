import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.urls import reverse

class MediaFile(models.Model):
    media = models.FileField(upload_to='uploads/')
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def get_absolute_url(self):
        # Generate the URL for the detail page (adjust 'media_detail' to match your URL name)
        return reverse('media_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        # Save the media file
        super().save(*args, **kwargs)

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.get_absolute_url())
        qr.make(fit=True)

        # Save the QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        qr_image.save(buffer)
        qr_filename = f'qrcode-{self.pk}.png'
        self.qr_code.save(qr_filename, File(buffer), save=False)

        # Save the model instance again with the QR code
        super().save(*args, **kwargs)
