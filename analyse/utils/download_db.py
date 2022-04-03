"""
    Create list of ECG signals from open source db
    (e.g. from open source MIT-BIH Atrial Fibrillation Database
    https://physionet.org/content/afdb/1.0.0/)
"""


import urllib.request
import ssl
import os
import sys
import zipfile
# import wfdb

def get_db(url, filename, destination):
    """
        If no file with 'filename' existed, download to 'destination' db from 'url'
        Returns path to db
    """
    files = os.listdir(destination)
    if filename in files:
        print(f"File with filename '{filename}' is already existed", file=sys.stderr)
        return f"{destination}{filename}"
    try:
        print(f"Downloading {filename}...", file=sys.stderr)
        destination = f'{destination}zip_{filename}'
        urllib.request.urlretrieve(url, destination)
        print("Download finished.", file=sys.stderr)
        print("Unzipping database...", file=sys.stderr)
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(destination)
            zip_ref.close()
            os.remove(destination)
            new_files = [file for file in os.listdir(destination) if file not in files]
            os.rename(f"{destination}{new_files[0]}", f"{destination}{filename}")
        print("Unzipping finished.", file=sys.stderr)
    except urllib.error.URLError:
        print("Stop! urllib.error.URLError occured\nTrying again...", file=sys.stderr)
        ssl._create_default_https_context = ssl._create_unverified_context # pylint: disable=protected-access
        get_db(url, filename, destination)

    return f"{destination}{filename}"
