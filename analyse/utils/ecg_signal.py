"""
    ECG signal class is defined here
"""

import numpy as np
import pandas as pd
from wfdb import processing

from utils.ecg_window import Window
from utils.global_config import CONFIG


class Signal:
    """
        Class for 1-D signal pre-processing
    """
    def __init__(self, sig_name, data, info):
        """
            Initialize object with signal from database
            data: 1-D array
        """
        self.name = sig_name

        self.sig_len = info['sig_len']
        self.sample_frequency = info['fs']
        self.window_size = CONFIG.get('window_size')

        annotation = info['annotation'].__dict__
        self.ecg_statuses = np.rec.fromarrays([
            list(map(lambda s: ''.join(filter(str.isalpha, s)), annotation['aux_note'])),
            annotation['sample']
        ])

        self.windows = self.split(data, self.window_size)

    def split(self, data, count):
        """
            Split signal to windows with 'count' RR intervals
        """
        windows = []
        peak_indexes = self.get_r_peaks(data)
        total_amount = len(peak_indexes) - count
        prev = [0, 0]
        for start in range(total_amount):
            if peak_indexes[start] <= self.ecg_statuses[0][1]:
                continue

            name = f"{self.name}_{start}"

            windows.append(Window(name, peak_indexes[start:start + count]))
            windows[-1].search_defects(self.ecg_statuses, prev)

        return np.array(windows)

    def get_r_peaks(self, data):
        """
            Returns indexes of R peaks
        """
        x_qrs = processing.XQRS(sig=data, fs=self.sample_frequency)
        x_qrs.detect(verbose=False)
        max_bpm = CONFIG.get('max_bpm')
        radius = int(self.sample_frequency * 60 / max_bpm)
        corrected_peak_indexes = processing.correct_peaks(
            data, peak_inds=x_qrs.qrs_inds,
            search_radius=radius, smooth_window_size=self.window_size)
        return np.array(corrected_peak_indexes)

    def get_data(self):
        """
            returns pandas DataFrame with all windows
                and pandas DataFrame with their classification
        """
        windows = []
        classifications = []
        for window in self.windows:
            metrics, has_defect = window.get_data()
            windows.append(metrics)
            classifications.append(has_defect)
        return pd.DataFrame(windows), pd.DataFrame(classifications)
