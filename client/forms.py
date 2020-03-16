from django import forms
import json

FIELD_NAME_MAPPING = {
}


# Create your models here.
AREAS = (
    ("TZAF", "צפון"),
    ("JERU", "ירושלים והסביבה"),
    ("MERK", "מרכז"),
    ("YEHU", "יהודה ושומרון"),
    ("DARO", "דרום")
)

json_file = open('./client/city.json', encoding="utf-8")
data = json.load(json_file)
onlyNames = [a["name"] for a in data]
onlyNames.sort()
CITIES = tuple({i: onlyNames[i] for i in range(0, len(onlyNames))}.items())
json_file.close()

# class NameForm(forms.Form):
#     your_name = forms.CharField(label='Your name', max_length=100)




# SEND HELP FORM
# -------------------------------------------------------------------------------------------------------

class VolunteerForm(forms.Form):


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
    age = forms.IntegerField()
    area = forms.MultipleChoiceField(choices = AREAS, widget=forms.CheckboxSelectMultiple())
    languages = forms.MultipleChoiceField(choices = LANG_CHOICES, widget=forms.CheckboxSelectMultiple())
    phone_number = forms.CharField(max_length=200)
    city = forms.ChoiceField(choices = CITIES)
    address = forms.CharField(max_length=200)
    available_on_saturday = forms.BooleanField(required=False)
    notes = forms.CharField(max_length=200)
    transportation = forms.ChoiceField(choices=MOVING_WAYS)
    hearing_way = forms.MultipleChoiceField(choices=HEARING_WAYS, widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "שם מלא"
        self.fields['area'].label = "איזור"
        self.fields['languages'].label = "שפות שאתה דובר"
        self.fields['phone_number'].label = "מספר פלאפון"
        self.fields['city'].label = "עיר מגורים"
        self.fields['address'].label = "כתובת מגורים"
        self.fields['available_on_saturday'].label = "האם זמין בשבת"
        self.fields['notes'].label = "הערות"
        self.fields['age'].label = "גיל"
        self.fields['transportation'].label = "דרכי התניידות"
        self.fields['hearing_way'].label = "איך שמעת עלינו"



class ScheduleForm(forms.Form):
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

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['sunday'].label = "ראשון"
        self.fields['monday'].label = "שני"
        self.fields['tuesday'].label = "שלישי"
        self.fields['wednesday'].label = "רביעי"
        self.fields['thursday'].label = "חמישי"
        self.fields['friday'].label = "שישי"
        self.fields['saturday'].label = "שבת"
        self.fields['end_date'].label = "תאריך סיום"
        self.fields['age'].label = "גיל"
        self.fields['transportation'].label = "דרכי התניידות"
        self.fields['hearing_way'].label = "איך שמעת עלינו"




# GET HELP FORM
# -------------------------------------------------------------------------------------------------------

class BaseHelpForm(forms.Form):
    """TYPES = (
        ('BUYIN', 'קניות\\איסוף'),
        ('MEDICI', 'תרופות'),
        ('HOME_HEL', 'עזרה בבית'),
        ('PHONE_HEL', 'תמיכה טלפונית'),
        ('OTHER', 'אחר')
    )"""

    full_name = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=200)
    city = forms.ChoiceField(choices = CITIES)
    address = forms.CharField(max_length=200)
    notes = forms.CharField(max_length=200)
    #type = forms.ChoiceField(choices=TYPES)
    #type_text = forms.CharField(max_length=5000)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "שם מלא"
        self.fields['phone_number'].label = "מספר פלאפון"
        self.fields['city'].label = "עיר מגורים"
        self.fields['address'].label = "כתובת מגורים"
        self.fields['notes'].label = "הערות"

class HomeForm(BaseHelpForm):
    need_text = forms.CharField(max_length=5000)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['need_text'].label = "מהי העזרה שאתה צריך"


class MedicForm(BaseHelpForm):
    need_prescription = forms.BooleanField(required=False)
    medic_name = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['need_prescription'].label = "האם מדובר בתרופת מרשם"
        self.fields['medic_name'].label = "שם תרופה"


class OtherForm(BaseHelpForm):
    other_need = forms.CharField(max_length=5000)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['other_need'].label = "פרט לאיזו עזרה אתה זקוק"


class ShoppingForm(BaseHelpForm):
    to_buy = forms.CharField(max_length=5000, widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['to_buy'].label = "הכנס את רשימת הקניות שלך"




class TravelForm(BaseHelpForm):
    travel_need = forms.CharField(max_length=5000)
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['travel_need'].label = "'פרט את מסלול הנסיעה הנדרש"

