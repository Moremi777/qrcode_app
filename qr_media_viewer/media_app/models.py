from django.db import models

class MediaFile(models.Model):
    media = models.FileField(upload_to='uploads/')  # Field for uploading media
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)  # Generated QR code for the media

    def __str__(self):
        return self.media.name

