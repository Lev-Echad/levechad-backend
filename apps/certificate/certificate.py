import os
import io

from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

from django.contrib.staticfiles import finders
from django.utils.translation import gettext as _

FONT_SIZE = 35
FONT_COLOR  = (3, 8, 12)
RIGHT_PADDING = 70

def create_certificate_image(certificate):
    # FIX: change to english strings and translate using gettext
    TEMPLATE = [
        _(f'שם מתנדב: {certificate.volunteer.first_name} {certificate.volunteer.last_name}'),
        _(f'תעודת זהות: {certificate.volunteer.tz_number}'),
        _(f'תוקף התעודה: {certificate.expiration_date}'),
        _(f'מספר תעודה: {certificate.id}'),
    ]


    tag_filename = finders.find('client/tag.jpeg')
    font_filename = finders.find('client/fonts/BN Amnesia.ttf')
    photo = None
    try:
        photo = Image.open(tag_filename)
        drawing = ImageDraw.Draw(photo)
        font = ImageFont.truetype(font_filename, size=FONT_SIZE)

        longest = max(TEMPLATE, key=len)
        text_size = font.getsize(longest)[0]
        align = photo.size[0] - text_size - RIGHT_PADDING

        text_position = (align, 200)

        drawing.text(
            text_position,
            get_display(os.linesep.join(TEMPLATE)),
            fill=FONT_COLOR,
            font=font,
            align='right'
        )
        output = io.BytesIO()
        photo.save(output, format='png')

    finally:
        if photo is not None:
            photo.close()

    return output


