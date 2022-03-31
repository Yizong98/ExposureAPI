from dateutil import parser
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import pandas as pd
import json
import os


def get_value_from_request(request, key):
    try:
        val = request.args[key]
        return False, val
    except KeyError:
        return True, None


def convert_string_to_date_time(date_list):
    date_time_list = []
    for date_str in date_list:
        try:
            date_time_list.append(parser.parse(date_str))
        except:
            pass

    return list(set(date_time_list))


def get_most_recent_7_days(date_time_list):
    date_time_list.sort(reverse=True)
    date_list_recent_7_days = []

    for i in range(min(7, len(date_time_list))):
        date_list_recent_7_days.append(date_time_list[i].strftime("%m/%d/%y"))

    return date_list_recent_7_days


def sort_and_unify_dates(date_list):
    return get_most_recent_7_days(convert_string_to_date_time(date_list))


def fetch_latest_exposure_data(instance_path):
    scope = ['https://spreadsheets.google.com/feeds']
    cred_path = os.path.join(instance_path, '.env/google_credentials.json')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        cred_path, scope)
    gc = gspread.authorize(credentials)
    spreadsheet_key = '1K4w2y4q7wZ0fs6_Tg51qXId1m2JaHrlADTHyvQFkiq0'
    book = gc.open_by_key(spreadsheet_key)
    worksheet = book.worksheet("Exposure")
    table = worksheet.get_all_values()
    logging.debug('Finished fetching latest exposure data')

    return pd.DataFrame(table[1:], columns=table[0])


def get_building_exposure_map(instance_path):
    exposure_data = fetch_latest_exposure_data(instance_path)
    exposure_data['available_dates'] = exposure_data[[
        'On-site infectivity dates', 'Latest Infectivity Date', 'Older Dates']].agg(','.join, axis=1)
    exposure_data['available_dates'] = exposure_data['available_dates'].str.strip()
    exposure_data['available_dates'] = exposure_data['available_dates'].str.split(
        ",")
    exposure_data['available_dates'] = exposure_data['available_dates'].apply(
        sort_and_unify_dates)

    logging.debug('Finished creating building_exposure_map')
    return dict(
        zip(exposure_data['CANN'], exposure_data['available_dates']))


def read_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def write_json(date_val, filename="./dashboard_request.json"):
    print(filename)
    data = read_file(filename)
    data.append(date_val)


    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return
