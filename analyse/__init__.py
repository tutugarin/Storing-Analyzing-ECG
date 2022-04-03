"""
    Start this file to begin
"""

import yaml

from utils.download_db import get_db  # pylint: disable=import-error

PATH_TO_DATA = "data/"

def main():
    """
        Parameters of run: config/params.yml
    """
    with open(r'config/params.yml', encoding='UTF-8') as file:
        params_list = yaml.load(file, Loader=yaml.FullLoader)
    urls = params_list["urls"]
    db_names = params_list["db_names"]

    databases = []
    for url, db_name in zip(urls, db_names):
        databases.append(get_db(url=url, filename=db_name, destination=PATH_TO_DATA))


if __name__ == "__main__":
    main()
