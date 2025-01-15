import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models

class MediaFile(models.Model):
    media = models.FileField(upload_to='uploads/')
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate QR code when media is uploaded
        if self.media and not self.qr_code:
            # Create the QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.get_absolute_url())  # URL where the media can be accessed
            qr.make(fit=True)

            # Create an image from the QR code
            img = qr.make_image(fill='black', back_color='white')

            # Save the image to the model's qr_code field
            qr_code_image = BytesIO()
            img.save(qr_code_image, 'PNG')
            qr_code_image.seek(0)
            self.qr_code.save(f'qr_code_{self.pk}.png', File(qr_code_image), save=False)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('display_media', kwargs={'media_name': self.media.name})
