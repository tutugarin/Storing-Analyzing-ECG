"""
    Start this file to begin
"""

import json

from utils.download_db import get_db # pylint: disable=import-error

PATH_TO_DATA = "data/"

def main():
    """
        Parametrs of run: config/params.yml
    """
    with open(r'config/params.json', encoding='UTF-8') as file:
        params_list = json.load(file)

    databases = []
    for database in params_list['databases']:
        databases.append(get_db(url=database['url'], filename=database['name'], destination=PATH_TO_DATA))


if __name__ == "__main__":
    main()
