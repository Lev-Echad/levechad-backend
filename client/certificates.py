import io

from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display
from django.conf import settings
from django.contrib.staticfiles import finders

MINIMUM_CERT_TEXT_WIDTH = 417


def create_image(certificate):
    volunteer = certificate.volunteer
    tag_filename = finders.find('client/tag.jpeg')
    font_filename = finders.find('client/fonts/BN Amnesia.ttf')
    with Image.open(tag_filename) as photo:
        drawing = ImageDraw.Draw(photo)
        font = ImageFont.truetype(font_filename, size=settings.CERTIFICATE_TEXT_SIZE)

        lines_to_insert = [
            f'שם מתנדב: {volunteer.first_name} {volunteer.last_name}',
            f'תעודת זהות: {volunteer.tz_number}',
            f'תוקף התעודה: {certificate.expiration_date}',
            f'מספר תעודה: {certificate.id}',
        ]
        pos_x, pos_y = settings.CERTIFICATE_TEXT_POSITION
        text_width, _ = drawing.textsize(
            get_display('\n'.join(lines_to_insert)),
            font=font,
        )
        # Takes care of possible text overflow because of long names.
        if text_width > MINIMUM_CERT_TEXT_WIDTH:
            pos_x -= text_width - MINIMUM_CERT_TEXT_WIDTH
        drawing.text(
            (pos_x, pos_y),
            get_display('\n'.join(lines_to_insert)),
            fill=settings.CERTIFICATE_TEXT_COLOR,
            font=font,
            align='right'
        )

        with io.BytesIO() as output:
            photo.save(output, format='png')
            result = output.getvalue()
    return result
