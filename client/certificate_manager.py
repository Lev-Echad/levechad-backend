import os
from datetime import date

from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display
from django.contrib.staticfiles import finders

CERTIFICATE_TEXT_COLOR = (3, 8, 12)  # (R, G, B)
CERTIFICATE_TEXT_SIZE = 40
CERTIFICATE_TEXT_POSITION = (700, 200)


def create_certificate_image(certificate):
    """
    Creates the volunteer certificate image with the current data and stores it under the correct path, overwriting
    the possibly-existing file.
    :param certificate: the VolunteerCertificate object to create the image for
    """
    volunteer = certificate.volunteer
    tag_filename = finders.find('client/tag.jpeg')
    font_filename = finders.find('client/fonts/BN Amnesia.ttf')
    photo = None
    try:
        photo = Image.open(tag_filename)
        drawing = ImageDraw.Draw(photo)
        font = ImageFont.truetype(font_filename, size=CERTIFICATE_TEXT_SIZE)

        lines_to_insert = [
            f'שם מתנדב: {volunteer.first_name} {volunteer.last_name}',
            f'תעודת זהות: {volunteer.tz_number}',
            f'תוקף התעודה: {certificate.expiration_date}',
            f'מספר תעודה: {certificate.id}',
        ]

        drawing.text(
            CERTIFICATE_TEXT_POSITION,
            get_display('\n'.join(lines_to_insert)),
            fill=CERTIFICATE_TEXT_COLOR,
            font=font,
            align='right'
        )
        photo.save(certificate.image_path, format='png')
    finally:
        if photo is not None:
            photo.close()


g_last_certificate_purge = None


def lazy_purge_certificates(certificate_model):
    """
    This is a function that should run daily. To avoid adding bloated, unneeded libraries / unnecessary complication
    to this project, we use this method, that's ran every time a new certificate is generated, and only purges
    certificates if a calendar day has passed from the last time of doing so.
    :param certificate_model: The VolunteerCertificate model, to avoid circular dependency
    """
    global g_last_certificate_purge

    today = date.today()
    if g_last_certificate_purge is None or today > g_last_certificate_purge:
        g_last_certificate_purge = today
        for certificate in certificate_model.objects.filter(expiration_date__lt=date.today()):
            try:
                os.remove(certificate_model.IMAGE_PATH_FORMAT.format(certificate.id))
            except OSError:
                continue
            certificate.delete()
