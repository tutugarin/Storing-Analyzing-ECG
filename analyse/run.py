"""
    Start this file to begin
"""

import json

from utils import download_db # pylint: disable=import-error

PATH_TO_DATA = "data/"


def main():
    """
        Parametrs of run: config/params.yml
    """
    with open(r'config/params.json', encoding='UTF-8') as file:
        params_list = json.load(file)

    signals = []
    for database in params_list['databases']:
        path = download_db.get_db(
            url=database['url'],
            filename=database['name'],
            destination=PATH_TO_DATA
        )
        new_signals = download_db.get_signals(path)
        if new_signals:
            signals.extend(new_signals)


if __name__ == "__main__":
    main()
