from django.db import models

class MediaFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)

    def __str__(self):
        return self.file.name
