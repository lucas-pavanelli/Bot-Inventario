import os
import shutil
import json
from io import StringIO
import pandas as pd


def get_date(folder="./Staging"):
    file_names = os.listdir(folder)
    if len(file_names) == 1:
        try:
            date = {"Day": int(file_names[0][:2]), "Month": int(
                file_names[0][3:5]), "Year": int(file_names[0][6:10])}
        except:
            clean_staging_area(file_names[0])
            # Error handling must be implemented so people don't upload files with invalid titles. If that is done this Try-catch can be removed
            raise Exception(
                "Sorry, file name must start with the DD_MM_YYYY date format")
        else:
            return file_names[0], date
    raise Exception(
        "Sorry, you need at least 1 item in the staging area to begin update process")


def write_date(date, destination="./data/last_update.json"):
    with open(destination, "w") as date_file:
        json.dump(date, date_file)
    return "Last Update date is now: Day {}, Month {}, Year {}".format(date["Day"], date["Month"], date["Year"])

def write_json(date, destination="./data/last_update.json"):
        with open(destination, "w") as date_file:
            json.dump(date, date_file)
        return "Success"

def get_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as date_file:
            data = json.load(date_file)
            return data
def write_input_file(file_name, source="./Staging/", destination="./data/input_file.xlsx"):
    if file_name.endswith("xlsx"):
        shutil.copy(source + file_name, destination)
        return "Success, Input File Updated"
def clean_staging_area(file_name, folder="./Staging/"):
    if os.path.exists(folder + file_name):
        os.remove(folder + file_name)
        return "File removed successfully"
def get_input_file(xlsx,xlsx_title):
    try: 
        with open("./Staging/"+xlsx_title+".xlsx", "wb") as file:
                        file.write(xlsx)
        file_name, date = get_date()
        write_date(date, "./data/last_update.json")
        write_input_file(file_name,
            destination="./data/input_file.xlsx")
        clean_staging_area(
                    file_name, folder="./Staging/")
    except:
        return "Mission Failed we'll get them next time"
    return "Success, Input File Updated"


