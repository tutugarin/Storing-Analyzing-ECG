"""
    Create list of ECG signals from open source db
    (e.g. from open source MIT-BIH Atrial Fibrillation Database
    https://physionet.org/content/afdb/1.0.0/)
"""

import urllib.request
import ssl
import os
import logging
import numpy as np
import pickle
import zipfile
import wfdb

from analyse.utils.ecg_signal import Signal


def get_db(url, filename, destination):
    """
        If no file with 'filename' existed, download to 'destination' db from 'url'
        Returns path to db
    """
    files = os.listdir(destination)
    if filename in files:
        return f"{destination}{filename}"
    try:
        logging.info(f"Downloading {filename}")
        zip_dest = f'{destination}zip_{filename}'
        urllib.request.urlretrieve(url, zip_dest)
        with zipfile.ZipFile(zip_dest, 'r') as zip_ref:
            zip_ref.extractall(destination)
            zip_ref.close()
            os.remove(zip_dest)
            new_files = [file for file in os.listdir(destination) if file not in files]
            os.rename(f"{destination}{new_files[0]}", f"{destination}{filename}")

        logging.info("Download finished!")
        bin_dir = f"{destination}{filename}-pickled"
        if bin_dir not in files:
            os.mkdir(bin_dir)
    except urllib.error.URLError:
        logging.error(f"Downloading stopped. Trying again")
        ssl._create_default_https_context = ssl._create_unverified_context  # pylint: disable=protected-access
        get_db(url, filename, destination)

    return f"{destination}{filename}"

def get_signals(path, reload=False):
    """
        Input:
            path - path to raw database with subdirectory RECORDS
            reload - bool var: if True clears {path}-pickled dir

        Output:
            list of objects of class Signal

        Consequences:
            fill {path}-pickled dir with pickled processed signals
    """
    bin_dir = f"{path}-pickled"
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
                data = np.array(data)

                info['annotation'] = wfdb.rdann(f"{path}/{rec}", 'atr')

                n_sig = info['n_sig']
                if n_sig == 1:
                    data = np.array(data, ndmin=2).T
                elif n_sig == 0:
                    logging.warning(f"Record {rec} has no channels")
                    continue

                for sig in range(n_sig):
                    sig_name = f"{rec}_{info['sig_name'][sig]}"
                    filename = f"{bin_dir}/{sig_name}.pickle"
                    if f"{sig_name}.pickle" in processed_signals:
                        with open(filename, 'rb') as bin_file:
                            logging.info(f"unpickling {filename}")
                            signals.append(pickle.load(bin_file))
                    else:
                        logging.info(f"preprocessing {filename}")
                        signals.append(Signal(sig_name, data[:, sig], info))
                        logging.info(f"pickling {filename}")
                        with open(filename, 'wb') as bin_file:
                            pickle.dump(
                                signals[-1],
                                file=bin_file,
                                protocol=pickle.HIGHEST_PROTOCOL
                            )

            except ValueError:
                logging.warning(f"Record {rec} can't be read")

    return np.array(signals)
