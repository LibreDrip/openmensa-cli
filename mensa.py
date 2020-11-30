#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import datetime
import argparse
import sys
import requests

# https://openmensa.org/c/CANTEEN_ID
CANTEEN_ID = 843

ap = argparse.ArgumentParser(prog='TODO',description='show meal information from OpenMensa.org')
# optionally set CANTEEN_ID per option
# ap.add_argument('-i', '--id', nargs='?', const=CANTEEN_ID, default=CANTEEN_ID, type=int)
group = ap.add_mutually_exclusive_group()
group.add_argument("-t", "--tomorrow", action="store_true", help='print meal plan for tomorrow')
group.add_argument("-w", "--week", action="store_true", help='print meal plan for the next 7 days')
group.add_argument("-d", "--debug", action="store_true", help='debug option')
args = ap.parse_args()


# CANTEEN_ID = args.id

# def set_date():
# today = datetime.date.today()
# tomorrow = today + datetime.timedelta(days=1)
# day_date = today

def jprint(request):
    pretty_json = json.dumps(request, indent=4, sort_keys=True, ensure_ascii=False) # needs ensure_ascii for utf8
    print(pretty_json)

# Kategorie, Name, Preis(students)
def canteenprint(day_date):
    # GET /canteens/:canteen_id/days/:day_date/meals
    mahlzeit = requests.get("https://openmensa.org/api/v2/canteens/{}/days/{}/meals".format(CANTEEN_ID,day_date))
    meals = len(mahlzeit.json())  # number of meals on each day
    print()  # formatting
    for i in range(0, meals):  # loop through meals
        category = mahlzeit.json()[i]['category']
        name = mahlzeit.json()[i]['name']
        prices = mahlzeit.json()[i]['prices']['students']  # employees, others, pupils, students
        prices = "{:.2f}€".format(prices)
        print(category)
        # print(category + ": "+ name + " Preis: " + prices))
        print(name)
        print("Preis: " + prices)
        print()


def check_closed(day_date):
    closed_json = requests.get("https://openmensa.org/api/v2/canteens/{}/days/".format(CANTEEN_ID))
    for element in closed_json.json():
        if str(element['date']) == (str(day_date)):
            # print("not closed")
            return False
            break
    else:
        # print("closed")
        return True


# no option passed
if not len(sys.argv) > 1:
    today = datetime.date.today()
    day_date = today
    canteenprint(day_date)
    # print(test)


if args.debug is True:
    response = requests.get("https://openmensa.org/api/v2/canteens")
    print(response.status_code)  # should return 200 if everything is ok

    # print Json File
    day_date = datetime.date.today()
    mahlzeit = requests.get("https://openmensa.org/api/v2/canteens/{}/days/{}/meals".format(CANTEEN_ID,day_date))
    jprint(mahlzeit.json())

if args.tomorrow is True:
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    day_date = tomorrow
    canteenprint(day_date)

if args.week is True:
    today = datetime.date.today()
    for i in range(0, 6):
        day_date = today + datetime.timedelta(days=i)
        if not check_closed(day_date):
            print(day_date.strftime('%A') + ":")
            canteenprint(day_date)
