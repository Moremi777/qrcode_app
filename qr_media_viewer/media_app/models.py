from django.db import models

class Media(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='media/')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return self.title
