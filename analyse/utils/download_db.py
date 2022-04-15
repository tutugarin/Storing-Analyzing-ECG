"""
    Create list of ECG signals from open source db
    (e.g. from open source MIT-BIH Atrial Fibrillation Database
    https://physionet.org/content/afdb/1.0.0/)
"""

import urllib.request
import ssl
import sys
import os
import zipfile
import wfdb

from .ecg_signal import create_signal


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

def get_signals(path):
    """
        Input:
            path - path to database with subdirectory RECORDS

        Output:
            list of objects of class Signal
    """
    signals = []
    all_records = f'{path}/RECORDS'
    for rec in open(all_records, "r"):
        rec = rec.replace('\n', '')
        try:
            data, info = wfdb.rdsamp(f"{path}/{rec}")
            n_sig = info['n_sig']
            if n_sig > 1:
                for sig in range(n_sig):
                    sig_name = f"{rec}/{info['sig_name'][sig]}"
                    signals.append(create_signal(name=sig_name, data=data[:, sig], info=info))
            else:
                sig_name = f"{rec}/{info['sig_name']}"
                signals.append(create_signal(name=sig_name, data=data, info=info))

        except:
            print(f"Record {rec} can't be read", file=sys.stderr)
    
    return signals