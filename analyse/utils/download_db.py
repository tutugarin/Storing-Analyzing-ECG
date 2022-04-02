"""
    Create list of ECG signals from open source db
    (e.g. from open source MIT-BIH Atrial Fibrillation Database
    https://physionet.org/content/afdb/1.0.0/)
"""

import wfdb
record = wfdb.rdrecord('Storing-Analyzing-ECG/analyse/data/recordings/04015', sampto=3000)
annotation = wfdb.rdann('Storing-Analyzing-ECG/analyse/data/recordings/04015', 'atr', sampto=3000)
