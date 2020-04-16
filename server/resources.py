from import_export import resources
from import_export.fields import Field

from client.models import Volunteer, HelpRequest


class VolunteerResource(resources.ModelResource):
    id = Field(attribute='id', column_name='מזהה מתנדב', default='')
    first_name = Field(attribute='first_name', column_name='שם פרטי', default='')
    last_name = Field(attribute='last_name', column_name='שם משפחה', default='')
    tz_number = Field(attribute='tz_number', column_name='תעודת זהות', default='')
    volunteer_type = Field(attribute='get_volunteer_type_display', column_name='סוג מתנדב', default='')
    date_of_birth = Field(attribute='date_of_birth', column_name='תאריך לידה', default='')
    organization = Field(attribute='organization', column_name='ארגון', default='')
    phone_number = Field(attribute='phone_number', column_name='מספר טלפון', default='')
    areas = Field(attribute='areas', column_name='איזור מגורים', default='')
    languages = Field(attribute='languages', column_name='שפות', default='')
    email = Field(attribute='email', column_name='אימייל', default='')
    city = Field(attribute='city', column_name='עיר', default='')
    neighborhood = Field(attribute='neighborhood', column_name='שכונת מגורים', default='')
    address = Field(attribute='address', column_name='כתובת', default='')
    available_saturday = Field(attribute='available_saturday', column_name='מין בשבת?', default='')
    keep_mandatory_worker_children = Field(attribute='keep_mandatory_worker_children', column_name='מעוניין לסייע לילדי עובדים חיוניים?', default='')
    guiding = Field(attribute='guiding', column_name='מדריך', default='')
    notes = Field(attribute='notes', column_name='הערות', default='')
    moving_way = Field(attribute='get_moving_way_display', column_name='אמצעי תחבורה', default='')
    hearing_way = Field(attribute='get_hearing_way_display', column_name='איך שמע על לב אחד', default='')
    created_date = Field(attribute='created_date', column_name='מועד הרשמה', default='')

    class Meta:
        model = Volunteer
        fields = ('id', 'first_name', 'last_name', 'tz_number', 'volunteer_type', 'date_of_birth', 'organization', 'phone_number', 'areas', 'languages', 'email', 'city', 'neighborhood', 'address', 'available_saturday', 'keep_mandatory_worker_children', 'guiding', 'notes', 'moving_way', 'hearing_way', 'created_date', )

    def dehydrate_available_saturday(self, flag):
        return 'כן' if flag else 'לא'

    def dehydrate_keep_mandatory_worker_children(self, flag):
        return 'כן' if flag else 'לא'

    def dehydrate_guiding(self, flag):
        return 'כן' if flag else 'לא'


class HelpRequestResource(resources.ModelResource):
    id = Field(attribute='id', column_name='מזהה בקשה', default='')
    created_date = Field(attribute='created_date', column_name='תאריך הבקשה', default='')
    full_name = Field(attribute='full_name', column_name='שם פונה', default='')
    phone_number = Field(attribute='phone_number', column_name='טלפון', default='')
    area = Field(attribute='area', column_name='איזור', default='')
    address = Field(attribute='address', column_name='כתובת', default='')
    request_reason = Field(attribute='get_request_reason_display', column_name='סיבת הבקשה', default='')
    city = Field(attribute='city', column_name='עיר', default='')
    type = Field(attribute='get_type_display', column_name='סוג פנייה', default='')
    notes = Field(attribute='notes', column_name='הערות', default='')
    status = Field(attribute='get_status_display', column_name='סטטוס', default='')
    helping_volunteer = Field(attribute='helping_volunteer', column_name='מתנדב שמטפל', default='')

    class Meta:
        model = HelpRequest
        fields = ('id', 'created_date', 'full_name', 'phone_number', 'area', 'address', 'request_reason', 'city', 'type', 'notes', 'status', 'helping_volunteer', )
