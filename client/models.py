from django.db import models
from django.utils import timezone

# Create your models here.
AREAS = (
    ("TZAF", "צפון"),
    ("JERU", "ירושלים והסביבה"),
    ("MERK", "מרכז"),
    ("YEHU", "יהודה ושומרון"),
    ("DARO", "דרום")
)

class Timestampable(models.Model):
    created_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(User, self).save(*args, **kwargs)

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


class VolunteerSchedule(Timestampable):
    end_date = models.DateField()
    sunday = models.CharField(max_length=3)
    monday = models.CharField(max_length=3)
    tuesday = models.CharField(max_length=3)
    wednesday = models.CharField(max_length=3)
    thursday = models.CharField(max_length=3)
    friday = models.CharField(max_length=3)
    saturday = models.CharField(max_length=3)


class Volunteer(Timestampable):
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
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    available_saturday = models.BooleanField()
    notes = models.CharField(max_length=200)
    moving_way = models.CharField(max_length=20, choices=MOVING_WAYS)
    hearing_way = models.CharField(max_length=20, choices=HEARING_WAYS)
    schedule = models.OneToOneField(VolunteerSchedule, on_delete=models.CASCADE, null=True)


class HelpRequest(Timestampable):
    TYPES = (
        ('BUYIN', 'קניות\\איסוף'),
        ('MEDICI', 'תרופות'),
        ('HOME_HEL', 'עזרה בבית'),
        ('PHONE_HEL', 'תמיכה טלפונית'),
        ('OTHER', 'אחר')
    )

    STATUSES = (
        ('WAITING', 'התקבלה'),
        ('IN_CARE', 'בטיפול'),
        ('TO_VOLUNTER', 'הועבר למתנדב'),
        ('DONE', 'טופל')
    )

    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    notes = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPES)
    type_text = models.CharField(max_length=5000)
    status = models.CharField(max_length=25, choices=STATUSES, blank=True)
