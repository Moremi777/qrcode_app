import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.urls import reverse

class MediaFile(models.Model):
    file_name = models.CharField(max_length=255)
    media = models.FileField(upload_to='uploads/')  # Example of a file field
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Only generate QR code when the instance is created
            url = reverse('display_media', kwargs={'media_name': self.file_name})  # Adjust URL to your needs
            qr_code_image = self.generate_qr_code(url)
            self.qr_code.save(f'{self.file_name}_qr.png', qr_code_image, save=False)
        super(MediaFile, self).save(*args, **kwargs)

    def generate_qr_code(self, data):
        """Generate a QR code image."""
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        
        # Save QR code as an in-memory file
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return File(img_io, name=f'{self.file_name}_qr.png')
