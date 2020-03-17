import os
import json
import django
import pandas as pd
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "levechad.settings")
django.setup()

# your imports, e.g. Django models
from client.models import Volunteer, Area, VolunteerSchedule, City, Language

Volunteer.objects.all().delete()
VolunteerSchedule.objects.all().delete()

SIDE_XLSX_NAME = 'sheet_manually.xlsx'
WRONG_COUNTER = 790

writer = pd.ExcelWriter(SIDE_XLSX_NAME, mode='a')

def parse_saturday(txt):
    if txt == "כן":
        return True

    return False

def get_age(age):
    try:
        if int(age) == age:
            return age
    except Exception:
        return 0

    return 0

def save_sheet_to_db(sheets_name, relevant_sheet_name):
    df = pd.read_excel(sheets_name, sheet_name=None)[relevant_sheet_name]
    df = df.fillna('')
    volunteers_number = len(df)
    for index, row in df.iterrows():
        if index <= 780:
            continue
        print("Row N.", index)
        try:
            v = \
                Volunteer(full_name=row["שם + משפחה"],
                          age=get_age(row["גיל"]),
                          phone_number=row["מס' טלפון"],
                          city=parse_city(row),
                          address=row["כתובת"],
                          available_saturday=parse_saturday(row["האם זמין בשבת?"]),
                          guiding=False,
                          notes="יובא מהמערכת הישנה. " + row["הערות"],
                          moving_way=parse_moving_way(row),
                          hearing_way=parse_hearing_way(row),
                          schedule=parse_schedule(row))
            v.save()
            v.areas.set(parse_area(row))
            v.languages.set(parse_languages(row))
            print('Inserted ' + str(index) + "\\" + str(volunteers_number))
        except Exception as e:
            print("Putting aside")
            save_row_aside(row)
            print("Couldn't insert volunteer, moving on. This was the error: ", str(e))
            continue


def manual_parse(input_msg, options=None, func_on_inp=None):
    """
    when the script couldn't parse a field, ask a person
    :param input_msg: explain about the field
    :param options: the options of the field. for convenience matters.
    :return:
    """

    if options:
        err_msg = 'Invalid input. please choose a number that matches an input from the list'
        opt_str = 'Insert the number of the correct input, as shown below. Press enter to insert "None":\n'
        for i, opt in enumerate(options):
            opt_str += str(i) + " : " + opt + " | "

        print(input_msg)

        # get a valid input
        inp = None
        while True:
            print()
            inp = input(opt_str)

            # this options for fields that aren't important
            if inp == '':
                print()
                return None

            try:
                ret_val = options[int(inp)]
                print()
                return ret_val

            # ValueError for not an int, IndexError for invalid int
            except (IndexError, ValueError) as e:
                print(err_msg)
                print()
                continue

    else:
        if func_on_inp:
            ret_val = func_on_inp(input(input_msg))
            print()
            return ret_val
        else:
            ret_val = input(input_msg)
            print()
            return ret_val

def save_row_aside(row):
    global WRONG_COUNTER
    head = WRONG_COUNTER == 0
    row.to_excel(writer, sheet_name='AAA', startcol=WRONG_COUNTER+1, header=False, index=False)
    WRONG_COUNTER += 1
    writer.save()


def parse_area(row):
    given = re.split(',|\\\|/|\.', row["איזור"])
    if given == ['']:
        return None
    areas_given = []
    for area_given in given:
        prev_size = len(areas_given)
        res = Area.objects.all().filter(name=area_given).first()
        if res is not None:
            areas_given.append(res)
        elif area_given == "ירושליים":
            # it's JERU
            areas_given.append(Area.objects.get("ירושלים"))
        elif area_given == 'יו"ש':
            # it's YEHU
            areas_given.append(Area.objects.get("יהודה ושומרון"))
        if len(areas_given) == prev_size:
            #it means it couldnt parse the area
            areas = Area.objects.all()
            areas_explained=""
            got_from_user = manual_parse(
                "Couldn't parse the area. Parse it :).\n The area way we couldn't parse was: " + area_given + "\n" + areas_explained,
                areas)
            if got_from_user != '':
                areas_given.append(got_from_user)

    return areas_given


def parse_schedule(row):
    schd = VolunteerSchedule(
        Sunday="123",
        Monday="123",
        Tuesday="123",
        Wednesday="123",
        Thursday="123",
        Friday="123",
        Saturday="123")
    schd.save()
    return schd


def parse_hearing_way(row):
    given = row["איך שמעת על לב אחד?"]
    hearing_ways = Volunteer.hearing_way.field.choices
    if given == '':
        return hearing_ways[3][0]

    for tup in hearing_ways:
        if given == tup[1]:
            return tup[0]
        elif given == "ווטסאפ":
            # its WHTSP
            return hearing_ways[1][0]
        elif given == "פייסבוק" or given == "אינסטגרם":
            # its FB_INST
            return hearing_ways[0][0]
        elif "טלוויזיה" in given or "רדיו" in given or "טלויזיה" in given:
            # its RAD_TV
            return hearing_ways[2][0]

    ways = [a[0] for a in hearing_ways]
    ways_explained = ", ".join([a[0] + " refers to:" + a[1] for a in hearing_ways])
    return manual_parse(
        "Couldn't parse the hearing way. Parse it :).\n The hearing way we couldn't parse was: " + given + "\n" + ways_explained,
        ways)


def parse_moving_way(row):
    given = row["דרך התניידות"]
    if given == '':
        return None

    moving_ways = Volunteer.moving_way.field.choices
    for tup in moving_ways:
        if given == tup[1]:
            return tup[0]
        elif given == "תחבורה ציבורית":
            # it's PUBL
            return moving_ways[1][0]

    ways = [a[0] for a in moving_ways]
    ways_explained = ", ".join([a[0] + " refers to:" + a[1] for a in moving_ways])
    return manual_parse(
        "Couldn't parse the moving way. Parse it :).\n The moving way we couldn't parse was: " + given + "\n" + ways_explained,
        ways)


def parse_city(row):
    """
    Only take the first city
    :param row:
    :return:
    """
    # only take the first city if some were inserted
    given = re.split(',|\\\|/|\.', row["יישוב"])
    if given == [""]:
        return None

    cities = City.objects.all()
    if len(given) > 1:
        inp = manual_parse("write 0 if it's one city, 1 if it's some cities: " + ",".join(given))
        if inp == 1:
            raise ValueError("2 or more cities. saving aside for later.")

    given = given[0]
    if "תל אביב" in given:
        return cities.get(name="תל אביב -יפו")

    try:
        city_obj = cities.get(name=given)
        return city_obj
    except Exception:
        try:
            def get_city(inp):
                return cities.get(name=inp)

            return manual_parse(
                "Couldn't parse the city. Write the city name if you understand. Otherwise press enter\n" +
                "the city we can't parse is: " + given,
                None,
                get_city)
        except Exception:
            return None


def parse_languages(row):
    # only take the first city if some were inserted
    given = row["האם אתה דובר שפות זרות?"].split(",")
    if given == ['']:
        return [None]

    languages = Language.objects.all()

    lng_list = []
    for given_lng in given:
        try:
            lng_obj = languages.get(name=given_lng)
            lng_list.append(lng_obj)
        except Exception:
            def get_language(inp):
                return languages.get(name=inp)

            try:
                lng_list.append(manual_parse(
                    "Couldn't parse the Language. Write the language name if you understand. Otherwise press enter\n" +
                    "the language we can't parse is: " + given_lng,
                    None,
                    get_language))
            except Exception:
                pass

    print("Final language list: ", lng_list)

    return lng_list


if __name__ == '__main__':
    sheets_name = 'sheet_db.xlsx'
    relevant_sheet_name = 'כללי'
    print("Make sure you ran the command 'python setup.py' in the Past. It is probably the case.\n\n")
    save_sheet_to_db(sheets_name, relevant_sheet_name)
