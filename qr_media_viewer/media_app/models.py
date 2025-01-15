import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models

class MediaFile(models.Model):
    media = models.FileField(upload_to='uploads/')
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.media and not self.qr_code:
            # Generate QR code when media is uploaded
            qr = qrcode.make(self.media.url)  # Create QR code for the media URL
            qr_io = BytesIO()
            qr.save(qr_io, 'PNG')
            qr_file = File(qr_io, name=f"{self.media.name}.png")
            self.qr_code.save(f"{self.media.name}.png", qr_file, save=False)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('display_media', kwargs={'media_name': self.media.name})
