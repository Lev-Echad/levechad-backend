# coding=utf-8

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta, date
# -*- coding: utf-8 -*-

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
        ''' On save, update timestamps '''
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

    def __str__(self):
        return self.name


class VolunteerSchedule(Timestampable):
    end_date = models.DateField(null=True)
    Sunday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)
    Monday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)
    Tuesday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)
    Wednesday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)
    Thursday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)
    Friday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)
    Saturday = models.CharField(max_length=DAY_NAME_LENGTH, blank=True)


class Volunteer(Timestampable):
    MOVING_WAYS = (
        ("CAR", "רכב"),
        ("PUBL", "תחבצ"),
        ("FOOT","רגלית")
    )
    HEARING_WAYS = (
        ("FB_INST", "פייסבוק ואינסטגרם"),
        ("WHTSP", "ווצאפ"),
        ("RAD_TV", "רדיו וטלוויזיה"),
        ("OTHR", "אחר")
    )
    TYPES = (
        ("NIGHBORHOOD_COORDINATOR", "רכז שכונה"),
        ("CITY_COORDINATOR", "רכז עיר"),
        ("STAFF", "מטה"),
        ("HAMAL", "חמל"),
        ("PROJECT", "פרויקט"),
        ("CHILD_CARE", "משפחתון"),
        ("MISSIONS", "משימות")
    )

    def get_or_generate_valid_certificate(self):
        certificate = self.get_active_certificates().first()
        if certificate is None:
            certificate = VolunteerCertificate.objects.create(volunteer_id=self.id)

        return certificate

    def get_active_certificates(self):
        return self.certificates.filter(expiration_date__gte=date.today())

    tz_number = models.CharField(max_length=ID_LENGTH, blank=True)
    first_name = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, default="")
    last_name = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, default="")
    full_name = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, blank=True)
    organization = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, blank=True)
    age = models.IntegerField()
    volunteer_type = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, choices=TYPES, default="MISSIONS")
    areas = models.ManyToManyField(Area)
    languages = models.ManyToManyField(Language)
    phone_number = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    email = models.EmailField(blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    neighborhood = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, blank=True)
    address = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    available_saturday = models.BooleanField()
    keep_mandatory_worker_children = models.BooleanField(default=False)
    guiding = models.BooleanField()
    notes = models.CharField(max_length=5000)
    moving_way = models.CharField(max_length=SHORT_FIELD_LENGTH, choices=MOVING_WAYS)
    hearing_way = models.CharField(max_length=SHORT_FIELD_LENGTH, choices=HEARING_WAYS)
    schedule = models.OneToOneField(VolunteerSchedule, on_delete=models.CASCADE, null=True)


class VolunteerCertificate(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='certificates', null=False)
    expiration_date = models.DateField(default=date.today)


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

    full_name = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    phone_number = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    notes = models.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    type = models.CharField(max_length=SHORT_FIELD_LENGTH, choices=TYPES)
    type_text = models.CharField(max_length=5000)
    status = models.CharField(max_length=25, choices=STATUSES, blank=True, default="WAITING")
    status_updater = models.CharField(max_length=100, blank=True)
    helping_volunteer = models.ForeignKey(Volunteer, on_delete=models.SET_NULL, null=True)


class HamalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.area)
