"""
    Create list of ECG signals from open source db
    (e.g. from open source MIT-BIH Atrial Fibrillation Database
    https://physionet.org/content/afdb/1.0.0/)
"""


import urllib.request
import ssl
import os
import zipfile

def get_db(url, filename, destination):
    """
        If no file with 'filename' existed, download to 'destination' db from 'url'
        Returns path to db
    """
    files = os.listdir(destination)
    if filename in files:
        return f"{destination}{filename}"
    try:
        zip_dest = f'{destination}zip_{filename}'
        urllib.request.urlretrieve(url, zip_dest)
        with zipfile.ZipFile(zip_dest, 'r') as zip_ref:
            zip_ref.extractall(destination)
            zip_ref.close()
            os.remove(zip_dest)
            new_files = [file for file in os.listdir(destination) if file not in files]
            os.rename(f"{destination}{new_files[0]}", f"{destination}{filename}")
    except urllib.error.URLError:
        ssl._create_default_https_context = ssl._create_unverified_context # pylint: disable=protected-access
        get_db(url, filename, destination)

    return f"{destination}{filename}"
