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
from pathlib import Path
import pickle
import zipfile
import wfdb
from sklearn.model_selection import train_test_split
import pandas as pd

from utils.ecg_signal import Signal
from utils.global_config import CONFIG


script_location = str(Path(__file__).absolute().parent)
PATH_TO_DATA = script_location + "/../data/"


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
                    sig_name = f"{rec}_ECG{sig + 1}"
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

            except ValueError as e:
                logging.warning(f"Record {rec} can't be read: {e}")

    return np.array(signals)


def get_all_signals(reload=False):
    """
        Input:
            reload - bool var: if True clears pickled dir
        Output:
            list of objects of class Signal from all databases
    """
    signals = []
    for database in CONFIG.get('databases'):
        path = get_db(
            url=database['url'],
            filename=database['name'],
            destination=PATH_TO_DATA
        )
        new_signals = get_signals(path, reload)
        signals.extend(new_signals)
    return np.array(signals)

def split_preprocess_signals(signals, test_size=0.25, seed=42):
    """
        Input:
            signals - list: splits it into test (with size test_size) and train lists
            test_size - float: from 0 to 1, size of test list
            seed - integer: seed for random splitting reproduction
        Output:
            four DataFrames, two for training and two for testing
            X_train, y_train, X_test, y_test
    """
    signals_train, signals_test = train_test_split(signals, test_size=test_size, random_state=seed)

    train_windows = pd.DataFrame()
    train_classification = pd.DataFrame()
    for signal in signals_train:
        metrics, classifications = signal.get_data()
        train_windows = pd.concat([train_windows, metrics], ignore_index=True)
        train_classification = pd.concat([train_classification, classifications], ignore_index=True)

    test_windows = pd.DataFrame()
    test_classification = pd.DataFrame()
    for signal in signals_test:
        metrics, classifications = signal.get_data()
        test_windows = pd.concat([test_windows, metrics], ignore_index=True)
        test_classification = pd.concat([test_classification, classifications], ignore_index=True)

    return train_windows, train_classification,\
           test_windows, test_classification

def split_dbs(test_size, seed=42, reload=False):
    """
        Input:
            test_size, seed, reload
        Output:
            four DataFrames, two for training and two for testing
            X_train, y_train, X_test, y_test
    """
    X_trains = pd.DataFrame()
    y_trains = pd.DataFrame()
    X_tests = pd.DataFrame()
    y_tests = pd.DataFrame()
    for database in CONFIG.get('databases'):
        db_path = get_db(database['url'], database['name'], PATH_TO_DATA)
        signals = get_signals(db_path, reload=reload)

        X_train_db, y_train_db, X_test_db, y_test_db = split_preprocess_signals(signals, test_size, seed)

        X_trains = pd.concat([X_trains, X_train_db], ignore_index=True)
        y_trains = pd.concat([y_trains, y_train_db], ignore_index=True)
        X_tests = pd.concat([X_tests, X_test_db], ignore_index=True)
        y_tests = pd.concat([y_tests, y_test_db], ignore_index=True)

    return X_trains, y_trains, \
           X_tests, y_tests
