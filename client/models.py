from django.db import models

# Create your models here.
AREAS = (
    ("TZAF", "צפון"),
    ("JERU", "ירושלים והסביבה"),
    ("MERK", "מרכז"),
    ("YEHU", "יהודה ושומרון"),
    ("DARO", "דרום")
)

class Language(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=200)
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return self.name


class VolunteerSchedule(models.Model):
    end_date = models.DateField()
    sunday = models.CharField(max_length=3)
    monday = models.CharField(max_length=3)
    tuesday = models.CharField(max_length=3)
    wednesday = models.CharField(max_length=3)
    thursday = models.CharField(max_length=3)
    friday = models.CharField(max_length=3)
    saturday = models.CharField(max_length=3)


class Volunteer(models.Model):
    MOVING_WAYS = (
        ("CAR", "רכב"),
        ("PUBL", 'תחב"צ'),
        ("FOOT", 'רגלית')
    )

    HEARING_WAYS = (
        ("FB_INST", "פייסבוק ואינסטגרם"),
        ("WHTSP", "ווצאפ"),
        ("RAD_TV", "רדיו וטלוויזיה"),
        ("OTHR", "אחר")
    )

    full_name = models.CharField(max_length=200)
    age = models.IntegerField()
    area = models.CharField(max_length=10, choices=AREAS)
    languages = models.ManyToManyField(Language)
    phone_number = models.CharField(max_length=200)
    city = models.OneToOneField(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    available_saturday = models.BooleanField()
    notes = models.CharField(max_length=200)
    moving_way = models.CharField(max_length=20, choices=MOVING_WAYS)
    hearing_way = models.CharField(max_length=20, choices=HEARING_WAYS)
    schedule = models.OneToOneField(VolunteerSchedule, on_delete=models.CASCADE)
    creation_date = models.DateTimeField()


class HelpRequest(models.Model):
    TYPES = (
        ('BUYIN', 'קניות\\איסוף'),
        ('MEDICI', 'תרופות'),
        ('HOME_HEL', 'עזרה בבית'),
        ('PHONE_HEL', 'תמיכה טלפונית'),
        ('OTHER', 'אחר')
    )

    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    city = models.OneToOneField(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    notes = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPES)
    type_text = models.CharField(max_length=5000)
