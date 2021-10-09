import os.path
import json
import datetime
from helpers import create_zip
from gdrive import gdrive_login, gdrive_upload_file

config = []
with open("config.json") as config_json:
    config = json.load(config_json)


def initialize():
    for save in config:
        save[
            "DESIRED_FILE_NAME"
        ] = f"{save['DESIRED_FILE_NAME']}-{str(datetime.datetime.now()).split('.')[0].replace(' ', '-').replace(':', '', 2)}.zip"
        create_zip_and_upload(save["LOCATION"], save["DESIRED_FILE_NAME"])


def cleanup():
    for save in config:
        os.remove(save["DESIRED_FILE_NAME"])


def create_zip_and_upload(location, desired_file_name):
    create_zip(location, desired_file_name)
    gdrive_upload_file(desired_file_name)


if __name__ == "__main__":
    try:
        gdrive_login()
        initialize()
    except:
        print("Something went wrong.")
    finally:
        cleanup()
        input("Press a key to terminate the program.")
