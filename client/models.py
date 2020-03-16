from django.db import models
from django.utils import timezone

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
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return self.name


class VolunteerSchedule(Timestampable):
    end_date = models.DateField(blank=True)
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
    areas = models.ManyToManyField(Area)
    languages = models.ManyToManyField(Language)
    phone_number = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    available_saturday = models.BooleanField()
    guiding = models.BooleanField()
    notes = models.CharField(max_length=200)
    moving_way = models.CharField(max_length=20, choices=MOVING_WAYS)
    hearing_way = models.CharField(max_length=20, choices=HEARING_WAYS)
    schedule = models.OneToOneField(VolunteerSchedule, on_delete=models.CASCADE, null=True)


class HelpRequest(Timestampable):
    TYPES = (
        ('BUYIN', 'קניות'),
        ('TRAVEL', 'איסוף'),
        ('MEDICI', 'תרופות'),
        ('HOME_HEL', 'עזרה בבית'),
        ('PHONE_HEL', 'תמיכה טלפונית'),
        ('OTHER', 'אחר')
    )

    STATUSES = (
        ('WAITING', 'התקבלה'),
        ('IN_CARE', 'בטיפול'),
        ('TO_VOLUNTER', 'הועבר למתנדב'),
        ('DONE', 'טופל'),
        ('NOT_DONE', 'לא טופל')
    )

    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    notes = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPES)
    type_text = models.CharField(max_length=5000)
    status = models.CharField(max_length=25, choices=STATUSES, blank=True)
    status_updater = models.CharField(max_length=100, blank=True)
