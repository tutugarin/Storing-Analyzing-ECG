"""
    ECG signal class is defined here
"""

from wfdb import processing
from ecg_window import Window

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
        self.data = data

        self.sig_len = info['sig_len']
        self.sample_frequency = info['fs']

        self.windows = []

    def split(self, count):
        """
            Split signal to windows with 'count' RR intervals
        """
        peak_indexes = self.get_r_peaks()

        #  calculating a mean shift between two neighbour R peaks
        mean_peak_diff = 0
        peak_counter = 0
        for i in range(10, min(len(peak_indexes), 500)):
            mean_peak_diff += peak_indexes[i] - peak_indexes[i - 1]
            peak_counter += 1
        mean_peak_diff /= peak_counter

        rr_start = 0
        for i in range(count, len(peak_indexes), count):
            rr_end = min(peak_indexes[i] + mean_peak_diff, len(self.data))
            self.windows.append(Window(self.data[rr_start:rr_end]))
            rr_start = rr_end

    def get_r_peaks(self):
        """
            Returns indexes of R peaks
        """
        x_qrs = processing.XQRS(sig=self.data[:, 0], fs=self.sample_frequency)
        x_qrs.detect()
        max_bpm = 230
        window_size = 150
        radius = int(self.sample_frequency * 60 / max_bpm)
        corrected_peak_indexes = processing.correct_peaks(
            self.data[:, 0], peak_inds=x_qrs.qrs_inds,
            search_radius=radius, smooth_window_size=window_size)
        return corrected_peak_indexes

def create_signal(name, data, info):
    """
        create Signal object
    """
    return Signal(name, data, info)
