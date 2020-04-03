import xlwt
import datetime

import django.db.models.manager
from django.db import models
from django.http import HttpResponse


def export_model_to_xls(
        model_type,
        fields_descriptions,
        filename=None,
        spreadsheet_name=None
):
    """
    Exports all model objects in the database to a .xls file, and returns a response with it as an attachment.
    Serializes:
     - Fields with choices to their corresponding value
     - bools to "לא" or "כן"
     - datetime objects to a formatted time ('%Y/%m/%d %H:%M')
     - ManyToMany relationships as a comma-joined list of Model objects str() was called on
     - Model objects by calling str() on them
    :param model_type: The django.db.models.Model instance to operate on
    :param fields_descriptions: A dictionary, with keys as the field names as specified in the model, and values as
                                the text to display in the header row
    :param filename: The filename to generate without the .xls extension
                     Default: <model_name_lower>_data-%Y_%m_%d-%H%M%S (with formatted time)
    :param spreadsheet_name: The name of the spreadsheet in the file
                             Default: <model_name>s

    :return: HttpResponse of content type application/ms-excel with the .xls file as an attachment
    """
    if filename is None:
        current_time = datetime.datetime.now().strftime('%Y_%m_%d-%H%M%S')
        filename = f'{model_type.__name__.lower()}_data-{current_time}'

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{filename}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(spreadsheet_name if spreadsheet_name is not None else f'{model_type.__name__}s')
    ws.cols_right_to_left = True

    bold_font = xlwt.easyxf('font:bold on')

    for col_num, header in enumerate(fields_descriptions.values()):
        ws.write(0, col_num, header, bold_font)

    for row_num, volunteer in enumerate(model_type.objects.all(), start=1):
        for col_num, key in enumerate(fields_descriptions.keys()):
            value = getattr(volunteer, key)
            field_choices = volunteer._meta.get_field(key).choices
            if field_choices is not None:
                value = dict(field_choices)[value]

            if isinstance(value, bool):
                value = 'כן' if value else 'לא'
            elif isinstance(value, datetime.datetime):
                value = value.strftime('%Y/%m/%d %H:%M')
            elif isinstance(value, django.db.models.manager.Manager):
                value = ', '.join([str(item) for item in value.all()])
            elif isinstance(value, models.Model):
                value = str(value)

            ws.write(row_num, col_num, value)

    wb.save(response)
    return response
