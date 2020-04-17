# coding=utf-8
import io
import math
from datetime import timedelta, date, datetime, time

import boto3
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display

from django.contrib.staticfiles import finders
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import F, Count
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.conf import settings
from django.urls import reverse

from django.dispatch import receiver
from django.db.models.signals import pre_save
from multiselectfield import MultiSelectField

DEFAULT_MAX_FIELD_LENGTH = 200
SHORT_FIELD_LENGTH = 20
ID_LENGTH = 11
DAY_NAME_LENGTH = 3


class Timestampable(models.Model):
    created_date = models.DateTimeField(null=True, editable=False)
    updated_date = models.DateTimeField(null=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Update timestamps on save
        if not self.id:
            self.created_date = timezone.now()
        self.updated_date = timezone.now()
        return super(Timestampable, self).save(*args, **kwargs)


class Area(models.Model):
    name = models.CharField(max_length=SHORT_FIELD_LENGTH, primary_key=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, primary_key=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, primary_key=True)
    x = models.FloatField()
    y = models.FloatField()
    region = models.ForeignKey(Area, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class VolunteerSchedule(Timestampable):
    end_date = models.DateField(null=True, blank=True)
    Sunday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)
    Monday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)
    Tuesday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)
    Wednesday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)
    Thursday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)
    Friday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)
    Saturday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)


class ExtendedVolunteerManager(models.Manager):
    @staticmethod
    def _add_distance(qs, helprequest_coordinates, as_int=False):
        qs = qs.annotate(y_distance=(F('city__y') - helprequest_coordinates[1]) ** 2)
        qs = qs.annotate(x_distance=(F('city__x') - helprequest_coordinates[0]) ** 2)
        qs = qs.annotate(distance=models.ExpressionWrapper(((F('x_distance') + F('y_distance')) ** 0.5) / 100,
                                                           output_field=models.IntegerField() if as_int
                                                           else models.FloatField()))
        return qs

    @staticmethod
    def _add_num_helprequests(qs):
        qs = qs.annotate(num_helprequests=Count('helprequest'))
        return qs

    def all_by_distance(self, helprequest_coordinates):
        volunteers_qs = self.get_queryset()
        volunteers_qs = self._add_distance(volunteers_qs, helprequest_coordinates)
        return volunteers_qs.order_by('distance')

    def all_by_score(self, helprequest_coordinates):
        # In the future, add more parameters
        volunteers_qs = self.get_queryset()
        volunteers_qs = self._add_distance(volunteers_qs, helprequest_coordinates, as_int=True)
        volunteers_qs = self._add_num_helprequests(volunteers_qs)
        return volunteers_qs.order_by('distance', 'num_helprequests')

    def all_with_helprequests_count(self):
        volunteers_qs = self.get_queryset()
        volunteers_qs = self._add_num_helprequests(volunteers_qs)
        return volunteers_qs


class Volunteer(Timestampable):
    objects = ExtendedVolunteerManager()
    MOVING_WAYS = (
        ("BIKE", "אופניים"),
        ("SCOOTER", "קטנוע"),
        ("CAR", "מכונית"),
        ("PUBL", "תחבורה ציבורית"),
        ("FOOT", "רגלית")
    )
    HEARING_WAYS = (
        ("FB_INST", "פייסבוק ואינסטגרם"),
        ("WHTSP", "ווצאפ"),
        ("RAD_TV", "רדיו וטלוויזיה"),
        ("OTHR", "אחר")
    )
    DEFAULT_TYPE = "MISSIONS"
    TYPES = (
        ("NIGHBORHOOD_COORDINATOR", "רכז שכונה"),
        ("CITY_COORDINATOR", "רכז עיר"),
        ("STAFF", "מטה"),
        ("HAMAL", "חמל"),
        ("PROJECT", "פרויקט"),
        ("CHILD_CARE", "משפחתון"),
        ("AGRICULTURE", "חקלאות"),
        (DEFAULT_TYPE, "משימות")
    )

    WANTED_ASSIGNMENTS = (
        ("FOOD", "חלוקת מזון"),
        ("MEDICINES", "משלוח תרופות"),
        ("STAFF", "סיוע לעובדים חיוניים"),
        ("TRANSPORTATION", "הסעות"),
        ("TELEPHONE SUPPORT", "תמיכה טלפונית"),
        ("CHILD_CARE", "עזרה במשפחתונים"),
        ("OTHER", "אחר"),
    )

    GENDERS = (
        ('MALE', 'זכר'),
        ('FEMALE', 'נקבה'),
        ('OTHER', 'מגדר אחר'),
    )

    _original_values = {
        'first_name': None,
        'last_name': None,
        'tz_number': None
    }

    def _update_original_values(self):
        """
        Updates the dict used to keep track of changes in certain fields between changes
        """
        self._original_values['tz_number'] = self.tz_number
        self._original_values['first_name'] = self.first_name
        self._original_values['last_name'] = self.last_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._update_original_values()

    def save(self, *args, **kwargs):
        if self.id is not None:
            for key, value in self._original_values.items():
                if getattr(self, key) != value:
                    # A change occurred in one of the fields listed in the dict - update valid certificates images
                    for certificate in self.get_active_certificates():
                        certificate.create_image()

                    break

        super().save(*args, **kwargs)
        self._update_original_values()

    def get_or_generate_valid_certificate(self):
        certificate = self.get_active_certificates().first()
        if certificate is None:
            certificate = VolunteerCertificate.objects.create(volunteer_id=self.id)

        return certificate

    def get_active_certificates(self):
        """
        Returns the active certificates a volunteer has, ordered by expiration date (first certificate has
        most time to live)
        """
        return self.certificates.filter(expiration_date__gte=date.today()).order_by('-expiration_date')

    tz_number = models.CharField(max_length=ID_LENGTH, blank=True)
    first_name = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, default="")
    last_name = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, default="")
    organization = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True, default=None)
    gender = models.CharField(max_length=SHORT_FIELD_LENGTH, choices=GENDERS, null=True, default=None, blank=True)
    date_of_birth = models.DateField(null=True, blank=True, default=None)
    # What is volunteer_type? wanted_assignments is kind of the same...
    volunteer_type = models.CharField(
        max_length=DEFAULT_MAX_FIELD_LENGTH,
        choices=TYPES,
        null=True,
        blank=True,
        default=DEFAULT_TYPE
    )
    wanted_assignments = MultiSelectField(choices=WANTED_ASSIGNMENTS, default=[item[0] for item in WANTED_ASSIGNMENTS])
    week_assignments_capacity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    areas = models.ManyToManyField(Area, blank=True)
    languages = models.ManyToManyField(Language)
    phone_number = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    email = models.EmailField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    neighborhood = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, null=True, blank=True)
    address = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    location_latitude = models.FloatField(default=0)
    location_longitude = models.FloatField(default=0)
    available_saturday = models.BooleanField(default=False)
    keep_mandatory_worker_children = models.BooleanField(default=False, blank=True, null=True)
    guiding = models.BooleanField(default=False, null=True, blank=True)
    notes = models.CharField(max_length=5000, null=True, blank=True)
    moving_way = models.CharField(max_length=SHORT_FIELD_LENGTH, choices=MOVING_WAYS)
    hearing_way = models.CharField(max_length=SHORT_FIELD_LENGTH, choices=HEARING_WAYS, blank=True, null=True)
    schedule = models.OneToOneField(VolunteerSchedule, on_delete=models.CASCADE, blank=True, null=True)
    score = models.IntegerField(default=0)

    @property
    def times_volunteered(self):
        return HelpRequest.objects.filter(helping_volunteer=self).count()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name


class VolunteerCertificate(models.Model):
    CERTIFICATE_TEXT_COLOR = (3, 8, 12)  # (R, G, B)
    CERTIFICATE_TEXT_SIZE = 40
    CERTIFICATE_TEXT_POSITION = (700, 200)
    IMAGE_PATH = 'certificates/{id}.png'
    DOWNLOAD_LINK_EXPIRATION_SECONDS = 600

    def _certificate_image_path(self, filename):
        return type(self).IMAGE_PATH.format(id=self.id)

    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='certificates', null=False)
    expiration_date = models.DateField(default=date.today)
    _image = models.FileField(blank=True, upload_to=_certificate_image_path)

    def create_image(self, save=True):
        volunteer = self.volunteer
        tag_filename = finders.find('client/tag.jpeg')
        font_filename = finders.find('client/fonts/BN Amnesia.ttf')
        photo = None
        try:
            photo = Image.open(tag_filename)
            drawing = ImageDraw.Draw(photo)
            font = ImageFont.truetype(font_filename, size=type(self).CERTIFICATE_TEXT_SIZE)

            lines_to_insert = [
                f'שם מתנדב: {volunteer.first_name} {volunteer.last_name}',
                f'תעודת זהות: {volunteer.tz_number}',
                f'תוקף התעודה: {self.expiration_date}',
                f'מספר תעודה: {self.id}',
            ]

            drawing.text(
                type(self).CERTIFICATE_TEXT_POSITION,
                get_display('\n'.join(lines_to_insert)),
                fill=type(self).CERTIFICATE_TEXT_COLOR,
                font=font,
                align='right'
            )
            with io.BytesIO() as output:
                photo.save(output, format='png')
                self._image.save(type(self).IMAGE_PATH.format(id=self.id), ContentFile(output.getvalue()), save=save)
        finally:
            if photo is not None:
                photo.close()

    def update_image_if_nonexistent(self, save=True):
        if not self._image.name:
            self.create_image(save=save)

    @property
    def image(self):
        if self.id is not None:
            self.update_image_if_nonexistent()
        return self._image

    @property
    def image_download_url(self):
        if settings.ENV == 'PRODUCTION':
            s3 = boto3.client('s3')
            return s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': 'levechad-media-bucket',
                    'Key': 'media/{}'.format(type(self).IMAGE_PATH.format(id=self.id)),
                    'ResponseContentDisposition': 'attachment;filename={}'.format(f'{self.id}.png'),
                },
                ExpiresIn=type(self).DOWNLOAD_LINK_EXPIRATION_SECONDS
            )
        else:
            return reverse('download_certificate', kwargs={'pk': self.id})


class HelpRequest(Timestampable):
    TYPES = (
        ('BUYIN', 'קניות'),
        ('TRAVEL', 'איסוף'),
        ('MEDICI', 'תרופות'),
        ('HOME_HEL', 'עזרה בבית'),
        ('PHONE_HEL', 'תמיכה טלפונית'),
        ('VITAL_WORK', 'סיוע לעובדים חיוניים'),
        ('OTHER', 'אחר')
    )

    STATUSES = (
        ('WAITING', 'התקבלה'),
        ('IN_CARE', 'בטיפול'),
        ('TO_VOLUNTER', 'הועבר למתנדב'),
        ('DONE', 'טופל'),
        ('NOT_DONE', 'לא טופל')
    )

    REQUEST_REASONS = (
        ('ISOLATION', 'בידוד'),
        ('HIGH_RISK_GROUP', 'קבוצת סיכון גבוהה'),
        ('OTHER', 'אחר'),
    )

    full_name = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    phone_number = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    location_latitude = models.FloatField(default=0)
    location_longitude = models.FloatField(default=0)
    notes = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, blank=True, null=True)
    type = models.CharField(max_length=SHORT_FIELD_LENGTH, choices=TYPES)
    type_text = models.CharField(max_length=5000)
    request_reason = models.CharField(max_length=25, choices=REQUEST_REASONS, default='OTHER')
    status = models.CharField(max_length=25, choices=STATUSES, blank=True, default='WAITING')
    status_updater = models.CharField(max_length=100, blank=True)
    helping_volunteer = models.ForeignKey(Volunteer, on_delete=models.SET_NULL, null=True, blank=True)


class HamalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.area)


class ParentalConsent(models.Model):
    parent_name = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    parent_id = models.CharField(max_length=9)
    volunteer = models.OneToOneField(Volunteer, on_delete=models.CASCADE, related_name='parental_consent')

# TODO: models validation is a good practice and should be added in the future - due to some inconsistency about our DB
# TODO: constraints over the time, the model validation blocks lots of functionality the used to work. in the future,
# TODO: when our data will be more normalized and standing with our constraints, this should be re-added.
# @receiver(pre_save, sender=Volunteer)
# @receiver(pre_save, sender=VolunteerCertificate)
# @receiver(pre_save, sender=VolunteerSchedule)
# def pre_save_handler(sender, instance, *args, **kwargs):
#     """
#     Django doesn't validate fields before saving by calling clean functions because of compatibility issues.
#     This does.
#     See https://docs.djangoproject.com/en/3.0/ref/models/instances/#validating-objects
#     """
#     instance.full_clean()
