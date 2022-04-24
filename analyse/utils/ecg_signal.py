"""
    ECG signal class is defined here
"""

import numpy as np
from wfdb import processing

from .ecg_window import create_window
from .global_config import GlobalConfig as CONFIG


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
        self.window_size = CONFIG.config('window_size')

        self.windows = self.split(data, self.window_size)

    def split(self, data, count):
        """
            Split signal to windows with 'count' RR intervals
        """
        windows = []
        peak_indexes = self.get_r_peaks(data)
        total_amount = len(peak_indexes) - count
        if total_amount > 0 :
            for start in range(total_amount):
                name = f"{self.name}_{start}"
                windows.append(create_window(name, peak_indexes[start:start + count]))

        return np.array(windows)

    def get_r_peaks(self, data):
        """
            Returns indexes of R peaks
        """
        x_qrs = processing.XQRS(sig=data, fs=self.sample_frequency)
        x_qrs.detect(verbose=False)
        max_bpm = 230
        window_size = 150
        radius = int(self.sample_frequency * 60 / max_bpm)
        corrected_peak_indexes = processing.correct_peaks(
            data, peak_inds=x_qrs.qrs_inds,
            search_radius=radius, smooth_window_size=window_size)
        return corrected_peak_indexes

def create_signal(name, data, info):
    """
        create Signal object
    """
    return Signal(name, data, info)
