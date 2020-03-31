# Generated by Django 3.0.4 on 2020-03-26 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='VolunteerSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(editable=False, null=True)),
                ('updated_date', models.DateTimeField(editable=False, null=True)),
                ('end_date', models.DateField(null=True)),
                ('Sunday', models.CharField(blank=True, max_length=3)),
                ('Monday', models.CharField(blank=True, max_length=3)),
                ('Tuesday', models.CharField(blank=True, max_length=3)),
                ('Wednesday', models.CharField(blank=True, max_length=3)),
                ('Thursday', models.CharField(blank=True, max_length=3)),
                ('Friday', models.CharField(blank=True, max_length=3)),
                ('Saturday', models.CharField(blank=True, max_length=3)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(editable=False, null=True)),
                ('updated_date', models.DateTimeField(editable=False, null=True)),
                ('tz_number', models.CharField(blank=True, max_length=11)),
                ('full_name', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('phone_number', models.CharField(max_length=200)),
                ('email', models.CharField(blank=True, max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('available_saturday', models.BooleanField()),
                ('keep_mandatory_worker_children', models.BooleanField(default=False)),
                ('guiding', models.BooleanField()),
                ('notes', models.CharField(max_length=5000)),
                ('moving_way', models.CharField(choices=[('CAR', 'רכב'), ('PUBL', 'תחבצ'), ('FOOT', 'רגלית')], max_length=20)),
                ('hearing_way', models.CharField(choices=[('FB_INST', 'פייסבוק ואינסטגרם'), ('WHTSP', 'ווצאפ'), ('RAD_TV', 'רדיו וטלוויזיה'), ('OTHR', 'אחר')], max_length=20)),
                ('areas', models.ManyToManyField(to='client.Area')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.City')),
                ('languages', models.ManyToManyField(to='client.Language')),
                ('schedule', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='client.VolunteerSchedule')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HelpRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(editable=False, null=True)),
                ('updated_date', models.DateTimeField(editable=False, null=True)),
                ('full_name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('notes', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('BUYING', 'קניות'), ('TRAVEL', 'איסוף'), ('MEDICI', 'תרופות'), ('HOME_HELP', 'עזרה בבית'), ('PHONE_HEL', 'תמיכה טלפונית'), ('VITAL_WORK', 'סיוע לעובדים חיוניים'), ('OTHER', 'אחר')], max_length=20)),
                ('type_text', models.CharField(max_length=5000)),
                ('status', models.CharField(blank=True, choices=[('WAITING', 'התקבלה'), ('IN_CARE', 'בטיפול'), ('TO_VOLUNTEER', 'הועבר למתנדב'), ('DONE', 'טופל'), ('NOT_DONE', 'לא טופל')], default='WAITING', max_length=25)),
                ('status_updater', models.CharField(blank=True, max_length=100)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='client.Area')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.City')),
                ('helping_volunteer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='client.Volunteer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HamalUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Area')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
