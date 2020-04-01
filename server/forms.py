from django import forms
import json
from django.core.validators import RegexValidator
from client.models import Language, DEFAULT_MAX_FIELD_LENGTH, ID_LENGTH

with open('./client/city.json', encoding="utf-8") as json_file:
    data = json.load(json_file)
onlyNames = [a["name"] for a in data]
onlyNames.append('')
onlyNames.sort()
CITIES = [(str(x), str(x)) for x in onlyNames]

AREAS = (
    ("צפון", "צפון"),
    ("ירושלים והסביבה", "ירושלים והסביבה"),
    ("מרכז", "מרכז"),
    ("יהודה ושומרון", "יהודה ושומרון"),
    ("דרום", "דרום")
)


class VolunteerSearchForm(forms.Form):
    LANGUAGES = [(str(x), str(x)) for x in Language.objects.all()]
    SORT_BY = [('id', 'מזהה מתנדב'),
               ('first_name', 'שם'),
               ('city', 'עיר'),
               ('age', 'גיל')]
    areas = forms.MultipleChoiceField(choices=AREAS, widget=forms.CheckboxSelectMultiple(), required=False)
    languages = forms.MultipleChoiceField(choices=LANGUAGES, widget=forms.CheckboxSelectMultiple(), required=False)
    sort_by = forms.ChoiceField(choices=SORT_BY, widget=forms.RadioSelect(), required=False)
    show_only_daycare = forms.BooleanField(widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['areas'].label = "אזורים להצגה"
        self.fields['languages'].label = "שפות"
        self.fields['sort_by'].label = "מיין לפי"
        self.fields['show_only_daycare'].label = "האם להראות רק את המתנדבים שמוכנים להתנדב לחוגים?"
