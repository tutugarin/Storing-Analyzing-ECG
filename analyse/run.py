"""
    You should be at the same dir, where run.py is
    Start this file to begin
"""

from utils import download_db # pylint: disable=import-error
from utils import global_config # pylint: disable=import-error
from utils.global_config import GlobalConfig as CONFIG # pylint: disable=import-error

PATH_TO_DATA = "data/"


def main():
    """
        Parametrs of run: config/params.yml
    """
    global_config.init_config(r'config/params.json')

    signals = []
    for database in CONFIG.config('databases'):
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
