# Generated by Django 3.0.4 on 2020-03-30 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_auto_20200330_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='schedule',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.VolunteerSchedule'),
        ),
    ]