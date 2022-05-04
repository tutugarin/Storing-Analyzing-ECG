"""
    You should be at the same dir, where run.py is
    Start this file to begin
"""

import logging
import sys

sys.path.append('../')

from utils import download_db as ddb


def main():
    """
        Parametrs of run: config/params.yml
        Get arg from command line: if 1 is given, data will be reloaded
    """

    reload = False
    if len(sys.argv) > 1 and sys.argv[1] == '1':
        reload = True

    signals = ddb.get_all_signals()


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
    main()
