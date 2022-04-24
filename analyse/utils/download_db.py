"""
    Create list of ECG signals from open source db
    (e.g. from open source MIT-BIH Atrial Fibrillation Database
    https://physionet.org/content/afdb/1.0.0/)
"""

import urllib.request
import ssl
import sys
import os
import pickle
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

        bin_dir = f"{destination}{filename}-binary"
        if bin_dir not in files:
            os.mkdir(bin_dir)
    except urllib.error.URLError:
        ssl._create_default_https_context = ssl._create_unverified_context # pylint: disable=protected-access
        get_db(url, filename, destination)

    return f"{destination}{filename}"

def get_signals(path, reload=False):
    """
        Input:
            path - path to raw database with subdirectory RECORDS
            reload - bool var: if True clears {path}-binary dir

        Output:
            list of objects of class Signal

        Consequences:
            fill {path}-binary dir with pickeled processed signals
    """
    bin_dir = f"{path}-binary"
    processed_signals = os.listdir(bin_dir)

    if reload is True:
        for file in processed_signals:
            os.remove(os.path.join(bin_dir, file))
        processed_signals = []

    signals = []

    all_records = f'{path}/RECORDS'
    with open(all_records, encoding='UTF-8') as file:
        for rec in file:
            rec = rec.replace('\n', '')
            try:
                data, info = wfdb.rdsamp(f"{path}/{rec}")
                n_sig = info['n_sig']
                if n_sig > 1:
                    for sig in range(n_sig):
                        sig_name = f"{rec}_{info['sig_name'][sig]}"
                        filename = f"{bin_dir}/{sig_name}.pickle"
                        if f"{sig_name}.pickle" in processed_signals:
                            with open(filename, 'rb') as bin_file:
                                signals.append(pickle.load(bin_file))
                        else:
                            signals.append(create_signal(sig_name, data[:, sig], info))
                            with open(filename, 'wb') as bin_file:
                                pickle.dump(
                                    signals[-1],
                                    file=bin_file,
                                    protocol=pickle.HIGHEST_PROTOCOL
                                )
                else:
                    sig_name = f"{rec}/{info['sig_name']}"
                    filename = f"{bin_dir}/{sig_name}.pickle"
                    if f"{sig_name}.pickle" in processed_signals:
                        with open(filename, 'rb') as bin_file:
                            signals.append(pickle.load(bin_file))
                    else:
                        signals.append(create_signal(sig_name, data, info))
                        with open(filename, 'wb') as bin_file:
                            pickle.dump(
                                signals[-1],
                                file=bin_file,
                                protocol=pickle.HIGHEST_PROTOCOL
                            )

            except ValueError:
                print(f"Record {rec} can't be read", file=sys.stderr)

    return signals
