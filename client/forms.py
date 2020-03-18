from django import forms
import json
from django.core.validators import RegexValidator
from client.models import Language

FIELD_NAME_MAPPING = {
}


# Create your models here.
AREAS = (
    ("צפון", "צפון"),
    ("ירושלים והסביבה", "ירושלים והסביבה"),
    ("מרכז", "מרכז"),
    ("יהודה ושומרון", "יהודה ושומרון"),
    ("דרום", "דרום")
)

json_file = open('./client/city.json', encoding="utf-8")
data = json.load(json_file)
onlyNames = [a["name"] for a in data]
onlyNames.sort()
CITIES = [(str(x),str(x)) for x in onlyNames]
json_file.close()
# class NameForm(forms.Form):
#     your_name = forms.CharField(label='Your name', max_length=100)




# SEND HELP FORM
# -------------------------------------------------------------------------------------------------------

def get_the_lang_choices():
    return  [(str(x),str(x)) for x in Language.objects.all()]

class VolunteerForm(forms.Form):
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

    BOOL = (
        ("YES", "כן"),
        ("NO", "לא"),
    )

    my_validator = RegexValidator(r"^\d+$")
    full_name = forms.CharField(max_length=200)
    identity = forms.CharField(max_length=9, validators=[my_validator])
    age = forms.IntegerField()
    area = forms.MultipleChoiceField(choices = AREAS, widget=forms.CheckboxSelectMultiple())
    languages = forms.MultipleChoiceField(choices = get_the_lang_choices, widget=forms.CheckboxSelectMultiple())
    phone_number = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)
    city = forms.ChoiceField(choices = CITIES)
    address = forms.CharField(max_length=200)
    available_on_saturday = forms.BooleanField(required=False)
    notes = forms.CharField(max_length=200)
    transportation = forms.ChoiceField(choices=MOVING_WAYS)
    hearing_way = forms.ChoiceField(choices=HEARING_WAYS)
    area = forms.MultipleChoiceField(choices = AREAS, widget=forms.CheckboxSelectMultiple())
    childrens = forms.MultipleChoiceField(choices = BOOL, widget=forms.CheckboxSelectMultiple())
    no_corona1 = forms.BooleanField()
    no_corona2 = forms.BooleanField()
    no_corona3 = forms.BooleanField()
    no_corona4 = forms.BooleanField()



    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "שם מלא"
        self.fields['identity'].label = "מספר ת.ז"
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
        self.fields['no_corona1'].label = "אני מאשר\ת כי לא חזרתי מחו''ל ב-14 הימים האחרונים"
        self.fields['no_corona2'].label = "אני מאשר\ת כי חשתי בטוב ב-14 הימים האחרונים - ללא תסמינים של שיעול, חום, צינון, כאב גרון וכיוצא בזה"
        self.fields['no_corona3'].label = "לא הייתי בבידוד ב-14 הימים האחרונים ולא שהיתי באותו הבית עם מישהו שנדרש בידוד"

        self.fields['no_corona4'].label = "אני מאשר\ת כי עברתי על המסלולים המעודכנים ביותר של החולים המאומתים, ולא באתי במגע עם אף אחד מהם"

        self.fields['childrens'].label = (
            "סיוע לעובדים חיוניים"
            + " - "
            + "האם את\ה מעוניין\ת בלעזור בהפעלת ילדים של עובדים חיוניים? "
        )

class ScheduleForm(forms.Form):
    TIMES = (
        ("1", "בוקר"),
        ("2", 'צהריים'),
        ("3", 'ערב')
    )
    sunday = forms.MultipleChoiceField(choices=TIMES, widget=forms.CheckboxSelectMultiple(), required=False)
    monday = forms.MultipleChoiceField(choices=TIMES, widget=forms.CheckboxSelectMultiple(), required=False)
    tuesday = forms.MultipleChoiceField(choices=TIMES, widget=forms.CheckboxSelectMultiple(), required=False)
    wednesday = forms.MultipleChoiceField(choices=TIMES, widget=forms.CheckboxSelectMultiple(), required=False)
    thursday = forms.MultipleChoiceField(choices=TIMES, widget=forms.CheckboxSelectMultiple(), required=False)
    friday = forms.MultipleChoiceField(choices=TIMES, widget=forms.CheckboxSelectMultiple(), required=False)
    saturday = forms.MultipleChoiceField(choices=TIMES, widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['sunday'].label = "ראשון"
        self.fields['monday'].label = "שני"
        self.fields['tuesday'].label = "שלישי"
        self.fields['wednesday'].label = "רביעי"
        self.fields['thursday'].label = "חמישי"
        self.fields['friday'].label = "שישי"
        self.fields['saturday'].label = "שבת"




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

    my_validator = RegexValidator(r"^\+?(972|0)(\-)?0?(([23489]{1}\d{7})|[5]{1}\d{8})$")
    full_name = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=200, required=True, validators=[my_validator])
    area = forms.ChoiceField(choices = AREAS)
    city = forms.ChoiceField(choices = CITIES)
    address = forms.CharField(max_length=200)
    notes = forms.CharField(max_length=200, required=False)
    #type = forms.ChoiceField(choices=TYPES)
    #type_text = forms.CharField(max_length=5000)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "שם מלא"
        self.fields['phone_number'].label = "מספר פלאפון"
        self.fields['area'].label = "אזור"
        self.fields['city'].label = "עיר מגורים"
        self.fields['address'].label = "כתובת מגורים"
        self.fields['notes'].label = "הערות"

class HomeForm(BaseHelpForm):
    need_text = forms.CharField(widget=forms.Textarea, max_length=5000)

    def __init__(self, *args, **kwargs):
        super(BaseHelpForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "שם מלא"
        self.fields['phone_number'].label = "מספר פלאפון"
        self.fields['area'].label = "אזור"
        self.fields['city'].label = "עיר מגורים"
        self.fields['address'].label = "כתובת מגורים"
        self.fields['notes'].label = "הערות"
        self.fields['need_text'].label = "מהי העזרה שאתה צריך"


class MedicForm(BaseHelpForm):
    need_prescription = forms.BooleanField(required=False)
    medic_name = forms.CharField(widget=forms.Textarea, max_length=5000)

    def __init__(self, *args, **kwargs):
        super(BaseHelpForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "שם מלא"
        self.fields['phone_number'].label = "מספר פלאפון"
        self.fields['area'].label = "אזור"
        self.fields['city'].label = "עיר מגורים"
        self.fields['address'].label = "כתובת מגורים"
        self.fields['notes'].label = "הערות"
        self.fields['need_prescription'].label = "האם מדובר בתרופת מרשם"
        self.fields['medic_name'].label = "שם תרופה"


class OtherForm(BaseHelpForm):
    other_need = forms.CharField(widget=forms.Textarea, max_length=5000)

    def __init__(self, *args, **kwargs):
        super(BaseHelpForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "שם מלא"
        self.fields['phone_number'].label = "מספר פלאפון"
        self.fields['area'].label = "אזור"
        self.fields['city'].label = "עיר מגורים"
        self.fields['address'].label = "כתובת מגורים"
        self.fields['notes'].label = "הערות"
        self.fields['other_need'].label = "פרט לאיזו עזרה אתה זקוק" + "\n" + "(הארגון אינו תומך בסיוע כלכלי,נוכל להפנות לגורמים הרלוונטיים)"


class ShoppingForm(BaseHelpForm):
    to_buy = forms.CharField(max_length=5000, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(BaseHelpForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "שם מלא"
        self.fields['phone_number'].label = "מספר פלאפון"
        self.fields['area'].label = "אזור"
        self.fields['city'].label = "עיר מגורים"
        self.fields['address'].label = "כתובת מגורים"
        self.fields['notes'].label = "הערות"
        self.fields['to_buy'].label = "הכנס את רשימת הקניות שלך"


class TravelForm(BaseHelpForm):
    travel_need = forms.CharField(widget=forms.Textarea, max_length=5000)

    def __init__(self, *args, **kwargs):
        super(BaseHelpForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "שם מלא"
        self.fields['phone_number'].label = "מספר פלאפון"
        self.fields['area'].label = "אזור"
        self.fields['city'].label = "עיר מגורים"
        self.fields['address'].label = "כתובת מגורים"
        self.fields['notes'].label = "הערות"
        self.fields['travel_need'].label = "'פרט את מסלול הנסיעה הנדרש"


class WorkersForm(BaseHelpForm):
    workplace_name = forms.CharField(max_length=100)
    workplace_need = forms.CharField(widget=forms.Textarea, max_length=5000)

    def __init__(self, *args, **kwargs):
        super(BaseHelpForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "שם מלא"
        self.fields['phone_number'].label = "מספר פלאפון"
        self.fields['area'].label = "אזור"
        self.fields['city'].label = "עיר מגורים"
        self.fields['address'].label = "כתובת מגורים"
        self.fields['notes'].label = "הערות"

        self.fields['workplace_name'].label = "שם המוסד בו את/ה עובד"
        self.fields['workplace_need'].label = "במה אתה זקוק לעזרה?"
