import yaml

from utils.download_db import get_db

PATH_TO_DATA = "data/"

def main():
    """
        Start 
    """
    with open(r'params.yml') as file:
        params_list = yaml.load(file, Loader=yaml.FullLoader)
    urls = params_list["urls"]
    db_names = params_list["db_names"]

    databases = []
    for i in range(len(urls)):
        databases.append(get_db(url=urls[i], filename=db_names[i], path2data=PATH_TO_DATA))


if __name__ == "__main__":
    main()
