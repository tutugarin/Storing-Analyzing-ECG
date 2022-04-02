"""
    Create list of ECG signals from open source db
    (e.g. from open source MIT-BIH Atrial Fibrillation Database
    https://physionet.org/content/afdb/1.0.0/)
"""

import urllib
import ssl
import os
import sys
import zipfile
import wfdb

def get_db(url, filename, path2data='../data/'):
    """
        Download to 'path2data' db from 'url' if no file with 'filename' existed
    """
    files = os.listdir(path2data)
    if filename in files:
        print(f"File with filename '{filename}' is already existed", file=sys.stderr)
        return
    try:
        print(f"Downloading {filename}...", file=sys.stderr)
        destination = f'{path2data}zip_{filename}'
        urllib.request.urlretrieve(url, destination)
        print("Download finished.", file=sys.stderr)
        print("Unzipping database...", file=sys.stderr)
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(path2data)
            zip_ref.close()
            os.remove(destination)
            os.rename(f"{path2data}files", f"{path2data}{filename}")
        print("Unzipping finished.", file=sys.stderr)
    except urllib.error.URLError:
        print("Stop! urllib.error.URLError occured\nTrying again...", file=sys.stderr)
        ssl._create_default_https_context = ssl._create_unverified_context # pylint: disable=protected-access
        get_db(url, filename)


URL = "https://physionet.org/static/published-projects/afdb/mit-bih-atrial-fibrillation-database-1.0.0.zip" # pylint: disable=line-too-long
FILENAME = "mit-bih"

get_db(url=URL, filename=FILENAME)

record = wfdb.rdrecord(f'../data/{FILENAME}/04015', sampto=3000)
annotation = wfdb.rdann(f'../data/{FILENAME}/04015', 'atr', sampto=3000)
