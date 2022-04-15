"""
    ECG signal class is defined here
"""

from wfdb import processing


class Signal:
    def __init__(self, name, data, info):
        """
            Initialize object with signal from database
            data: 1-D array
        """
        self.name = name
        self.data = data

        self.sig_len = info['sig_len']
        self.sample_frequency = info['fs']
        self.sig_name = info['sig_name']

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
            self.windows.append(self.data[rr_start:rr_end])
            rr_start = rr_end
        pass

    def get_r_peaks(self):
        """
            Returns indexes of R peaks
        """
        x_qrs = processing.XQRS(sig=self.data[:, 0], fs=self.sample_frequency)
        x_qrs.detect()
        MAX_BPM = 230
        WINDOW_SIZE = 150
        radius = int(self.sample_frequency * 60 / MAX_BPM)
        corrected_peak_indexes = processing.correct_peaks(self.data[:, 0], peak_inds=x_qrs.qrs_inds,
                                                          search_radius=radius, smooth_window_size=WINDOW_SIZE)
        return corrected_peak_indexes
        pass
