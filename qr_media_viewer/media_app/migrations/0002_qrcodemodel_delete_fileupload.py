# Generated by Django 5.1.2 on 2025-01-08 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QRCodeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qrcodes/')),
            ],
        ),
        migrations.DeleteModel(
            name='FileUpload',
        ),
    ]
