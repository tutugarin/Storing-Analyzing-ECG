"""
    You should be at the same dir, where run.py is
    Start this file to begin
"""

import logging
import sys

from utils import download_db # pylint: disable=import-error
from utils import global_config # pylint: disable=import-error
from utils.global_config import GlobalConfig as CONFIG # pylint: disable=import-error

PATH_TO_DATA = "data/"


def main():
    """
        Parametrs of run: config/params.yml
        Get arg from command line: if 1 is given, data will be reloaded
    """

    reload = False
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        reload = True

    signals = []
    for database in CONFIG.config('databases'):
        path = download_db.get_db(
            url=database['url'],
            filename=database['name'],
            destination=PATH_TO_DATA
        )
        new_signals = download_db.get_signals(path, reload)
        signals.extend(new_signals)


if __name__ == "__main__":
    """
        Setup config and run main
    """
    logging.basicConfig(
        filename='run-logs.log', 
        encoding='utf-8', 
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.DEBUG, 
        filemode='w'
    )
    global_config.init_config(r'config/params.json')
    main()
