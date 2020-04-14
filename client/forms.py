import json

from django import forms

from client.models import HelpRequest, Language, DEFAULT_MAX_FIELD_LENGTH, ID_LENGTH
from client.validators import id_number_validator, phone_number_validator

FIELD_NAME_MAPPING = {
}

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
CITIES = [(str(x), str(x)) for x in onlyNames]

json_file.close()


def get_lang_choices():
    return [(str(x), str(x)) for x in Language.objects.all()]


class NoDefaultChoiceField(forms.ChoiceField):
    """
    A choice field with a blank option at the beginning.
    """
    def __init__(self, *args, choices=None, **kwargs):
        if choices is not None:
            choices = [('', '')] + list(choices)
        super().__init__(*args, choices=choices, initial='', **kwargs)


class VolunteerForm(forms.Form):
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

    BOOL = (
        ("YES", "כן"),
        ("NO", "לא"),
    )

    first_name = forms.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    last_name = forms.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    id_number = forms.CharField(max_length=ID_LENGTH, validators=[id_number_validator])
    organization = forms.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, required=False)
    date_of_birth = forms.DateField(input_formats=['%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y', '%d.%m.%Y', '%d.%m.%y'],
                                    required=True)
    area = forms.MultipleChoiceField(choices=AREAS, widget=forms.CheckboxSelectMultiple())
    languages = forms.MultipleChoiceField(choices=get_lang_choices, widget=forms.CheckboxSelectMultiple())
    phone_number = forms.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, validators=[phone_number_validator])
    email = forms.EmailField()
    city = NoDefaultChoiceField(choices=CITIES)
    neighborhood = forms.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, required=False)
    address = forms.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    available_on_saturday = forms.BooleanField(required=False)
    notes = forms.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, required=False)
    transportation = NoDefaultChoiceField(choices=MOVING_WAYS)
    hearing_way = NoDefaultChoiceField(choices=HEARING_WAYS)
    childrens = NoDefaultChoiceField(choices=BOOL)
    chamal = NoDefaultChoiceField(choices=BOOL)

    no_corona1 = forms.BooleanField()
    no_corona2 = forms.BooleanField()
    no_corona3 = forms.BooleanField()
    no_corona4 = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "שם פרטי"
        self.fields['last_name'].label = "שם משפחה"
        self.fields['id_number'].label = "מספר ת.ז"
        self.fields['organization'].label = "ארגון"
        self.fields['organization'].widget.attrs['readonly'] = True
        self.fields['languages'].label = "שפות שאתה דובר"
        self.fields['date_of_birth'].label = "תאריך לידה"
        self.fields['phone_number'].label = "מספר פלאפון"
        self.fields['email'].label = "כתובת אימייל"
        self.fields['area'].label = "איזור"
        self.fields['city'].label = "עיר מגורים"
        self.fields['neighborhood'].label = "שכונה"
        self.fields['address'].label = "כתובת מגורים"
        self.fields['available_on_saturday'].label = "האם זמין בשבת"
        self.fields['notes'].label = "הערות"
        self.fields['transportation'].label = "דרכי התניידות"
        self.fields['hearing_way'].label = "איך שמעת עלינו"
        self.fields['no_corona1'].label = "אני מאשר/ת כי לא חזרתי מחו\"ל ב-14 הימים האחרונים"
        self.fields['no_corona2'].label = (
            "אני מאשר/ת כי חשתי בטוב ב-14 הימים האחרונים - ללא תסמינים של שיעול, חום, צינון, כאב גרון וכיוצא בזה"
        )
        self.fields['no_corona3'].label = (
            "לא הייתי בבידוד ב-14 הימים האחרונים ולא שהיתי באותו הבית עם מישהו שנדרש בידוד"
        )
        self.fields['no_corona4'].label = (
            "אני מאשר/ת כי עברתי על המסלולים המעודכנים ביותר של החולים המאומתים, ולא באתי במגע עם אף אחד מהם"
        )

        self.fields['childrens'].label = (
            "האם את/ה מעוניינ/ת לסייע לעובדים חיוניים (מסגרות חיוניות לילדי צוות רפואי)? - עדיפות ל-3 ימי התנדבות."
        )
        self.fields['chamal'].label = (
            "?האם אתה מתנדב חמ\"ל"
        )


class GetCertificateForm(forms.Form):
    id_number = forms.CharField(max_length=9, validators=[id_number_validator], required=True)
    no_fever = forms.BooleanField(required=True)
    routes = forms.BooleanField(required=True)
    signing = forms.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_number'].label = 'אנא הזן תעודת זהות'
        self.fields['no_fever'].label = ''.join([
            'אני מאשר כי חום גופי אינו עולה על 38 מעלות וכי אני חש בטוב ללא תסמינים של חום, שיעול, ',
            'כאבי גרון, צינון וכיוצא בזה.'
        ])
        self.fields['routes'].label = (
            'אני מאשר/ת כי עברתי על המסלולים המעודכנים ביותר של החולים המאומתים, ולא באתי במגע עם אף אחד מהם.'
        )
        self.fields['signing'].label = 'הכנס שם מלא כדי לאשר:'


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

    full_name = forms.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    phone_number = forms.CharField(
        max_length=DEFAULT_MAX_FIELD_LENGTH,
        required=True,
        validators=[phone_number_validator]
    )
    area = NoDefaultChoiceField(choices=AREAS)
    city = NoDefaultChoiceField(choices=CITIES)
    address = forms.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH)
    request_reason = NoDefaultChoiceField(choices=HelpRequest.REQUEST_REASONS)
    notes = forms.CharField(max_length=DEFAULT_MAX_FIELD_LENGTH, required=False)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "שם מלא"
        self.fields['phone_number'].label = "מספר פלאפון"
        self.fields['area'].label = "אזור"
        self.fields['city'].label = "עיר מגורים"
        self.fields['address'].label = "כתובת מגורים"
        self.fields['notes'].label = "הערות"
        self.fields['request_reason'].label = 'סיבת הבקשה'


class PhoneHelpForm(BaseHelpForm):
    pass


class MedicForm(BaseHelpForm):
    need_prescription = forms.BooleanField(required=False)
    medic_name = forms.CharField(widget=forms.Textarea, max_length=5000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['need_prescription'].label = "האם מדובר בתרופת מרשם"
        self.fields['medic_name'].label = "שם תרופה"


class OtherForm(BaseHelpForm):
    other_need = forms.CharField(widget=forms.Textarea, max_length=5000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['other_need'].label = '\n'.join([
            'פרט לאיזו עזרה אתה זקוק',
            '(הארגון אינו תומך בסיוע כלכלי,נוכל להפנות לגורמים הרלוונטיים)',
        ])


class ShoppingForm(BaseHelpForm):
    to_buy = forms.CharField(max_length=5000, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to_buy'].label = "הכנס את רשימת הקניות שלך"


class TravelForm(BaseHelpForm):
    travel_need = forms.CharField(widget=forms.Textarea, max_length=5000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['travel_need'].label = "פרט את מסלול הנסיעה הנדרש"


class WorkersForm(BaseHelpForm):
    workplace_name = forms.CharField(max_length=100)
    workplace_need = forms.CharField(widget=forms.Textarea, max_length=5000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].label = "הערות"

        self.fields['workplace_name'].label = "שם המוסד בו את/ה עובד"
        self.fields['workplace_need'].label = "במה אתה זקוק לעזרה?"
