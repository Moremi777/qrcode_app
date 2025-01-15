import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.urls import reverse

class MediaUpload(models.Model):
    file_name = models.CharField(max_length=255, blank=True, null=True)
    media = models.FileField(upload_to='uploads/')  
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Only generate QR code when the instance is created
            if not self.file_name:  # Check if file_name is empty or None
                self.file_name = self.media.name  # Default to media file name
            
            # Generate the URL for the QR code
            url = reverse('media_display', kwargs={'media_name': self.file_name})
            qr_code_image = self.generate_qr_code(url)
            self.qr_code.save(f'{self.file_name}_qr.png', qr_code_image, save=False)  # Don't save twice

        super().save(*args, **kwargs)

    def generate_qr_code(self, url):
        """Generate QR code image from URL."""
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill='black', back_color='white')
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return File(img_io, name='qr_code.png')

    def __str__(self):
        return self.file_name or "Untitled Media"
