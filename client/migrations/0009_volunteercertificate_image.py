# Generated by Django 3.0.4 on 2020-04-01 20:57

import client.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_auto_20200329_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteercertificate',
            name='image',
            field=models.FileField(blank=True, upload_to=client.models.VolunteerCertificate._certificate_image_path),
        ),
    ]