from django import forms
import json

# Create your models here.
AREAS = (
    ("TZAF", "צפון"),
    ("JERU", "ירושלים והסביבה"),
    ("MERK", "מרכז"),
    ("YEHU", "יהודה ושומרון"),
    ("DARO", "דרום")
)

json_file = open('./client/city.json')
data = json.load(json_file)
onlyNames = [a["name"] for a in data]
CITIES = tuple({i: onlyNames[i] for i in range(0, len(onlyNames))}.items())
json_file.close()


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)



class BaseForm(forms.Form):
    LANG_CHOICES = (
        ("1", "ערבית"),
        ("2", "רוסית"),
        ("3", "צרפתית"),
        ("4", "אנגלית"),
    )

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


    full_name = forms.CharField(max_length=200)
    # age = forms.IntegerField()
    # area = forms.MultipleChoiceField(choices = AREAS)
    # languages = forms.MultipleChoiceField(choices = LANG_CHOICES)
    # phone_number = forms.CharField(max_length=200)
    # city = forms.ChoiceField(choices = CITIES)
    # address = forms.CharField(max_length=200)
    # available_on_saturday = forms.BooleanField(required=false)
    # notes = forms.CharField(max_length=200)
    # transportation = forms.ChoiceField(choices=MOVING_WAYS)
    # hearing_way = forms.MultipleChoiceField(choices=HEARING_WAYS)


class ScheduleForm(BaseForm):
    TIMES = (
        ("MORNING", "בוקר"),
        ("NOON", 'צהריים'),
        ("EVENING", 'ערב')
    )
    sunday = forms.MultipleChoiceField(choices=TIMES)
    monday = forms.MultipleChoiceField(choices=TIMES)
    tuesday = forms.MultipleChoiceField(choices=TIMES)
    wednesday = forms.MultipleChoiceField(choices=TIMES)
    thursday = forms.MultipleChoiceField(choices=TIMES)
    friday = forms.MultipleChoiceField(choices=TIMES)
    saturday = forms.MultipleChoiceField(choices=TIMES)
    end_date = forms.DateField()


# class HelpForm(forms.Form):
#     TYPES = (
#         ('BUYIN', 'קניות\\איסוף'),
#         ('MEDICI', 'תרופות'),
#         ('HOME_HEL', 'עזרה בבית'),
#         ('PHONE_HEL', 'תמיכה טלפונית'),
#         ('OTHER', 'אחר')
#     )
#
#     full_name = forms.CharField(max_length=200)
#     phone_number = forms.CharField(max_length=200)
#     city = forms.ChoiceField(choices = CITIES)
#     address = forms.CharField(max_length=200)
#     notes = forms.CharField(max_length=200)
#     type = forms.ChoiceField(choices=TYPES)
#     #type_text = forms.CharField(max_length=5000)

class HomeForm(BaseForm):
    need_text = forms.CharField(max_length=5000)


class MedicForm(BaseForm):
    need_prescription = forms.BooleanField(required=False)
    medic_name = forms.CharField(max_length=200)


class OtherForm(BaseForm):
    other_need = forms.CharField(max_length=5000)


class ShoppingForm(BaseForm):
    to_buy = forms.CharField(max_length=5000)


class TravelForm(BaseForm):
    travel_need = forms.CharField(max_length=5000)















