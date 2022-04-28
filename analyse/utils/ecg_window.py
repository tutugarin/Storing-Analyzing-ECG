"""
    ECG window class is defined here
"""

import numpy as np
import regex as re

from analyse.utils.global_config import GlobalConfig as CONFIG


class Window:
    """
        Class for special interval of a processed signal
    """
    def __init__(self, name, r_peak_indexes):
        """
            Initialize object with interval (interval_size can differ)
        """
        self.name = name
        self.r_peaks = r_peak_indexes

        self.has_defect : bool = None

        ratios = self.get_ratios()

        self.alphabet = self.code_ratios(ratios)

        self.median = np.median(ratios)
        self.mean = np.mean(ratios)
        self.variance = np.var(ratios)
        self.mean_abs = np.mean(np.abs(ratios))
        self.max = np.max(ratios)
        self.min = np.min(ratios)
        self.sum = np.sum(ratios)

    def get_ratios(self):
        """
            Output:
                get list of ratios
                ratio_i = 1 - y_i / y_{i-1}
                where y_i = len of i time interval
        """
        ratios = []
        prev_len = self.r_peaks[1] - self.r_peaks[0]
        for i in range(1, len(self.r_peaks) - 1):
            cur_len = self.r_peaks[i + 1] - self.r_peaks[i]
            if prev_len != 0:
                ratios.append((cur_len / prev_len) - 1)
            prev_len = cur_len
        return np.array(ratios)


    def code_ratios(self, ratios):
        """
            Make from ratios list of coded letters:
            A - if abs(ratio) <  treshold
            B - if ratio > treshold
            C - if ratio < -1 * treshold
        """
        treshold = CONFIG.get('treshold')
        alphabet = []
        for ratio in ratios:
            if ratio > treshold:
                alphabet.append('B')
                continue
            if ratio < -treshold:
                alphabet.append('C')
                continue
            alphabet.append('A')

        return ''.join(alphabet)

    def search_defects(self, ecg_statuses, prev=None) -> bool:
        """
            Get Continuous Arrhythmia Sections and mark window, if it has defect
        """
        if prev is None:
            prev = [0, 0]

        total_statuses = ecg_statuses.shape[0]
        while prev[0] + 1 < total_statuses and self.r_peaks[0] > ecg_statuses[prev[0] + 1][1]:
            prev[0] += 1
        while prev[1] + 1 < total_statuses and self.r_peaks[-1] > ecg_statuses[prev[1] + 1][1]:
            prev[1] += 1
        
        for status, _ in ecg_statuses[prev[0]:prev[1] + 1]:
            if status != 'N':
                self.has_defect = True
                return True
        self.has_defect = False
        return False
    
    def count_ngrams(self, word=None):
        """
            count all ngams in alphbet
        """
        if word is None:
            word = self.alphabet
        possible_ngramms = CONFIG.get("possible_ngramms")
        dict_ = {s: 0 for s in possible_ngramms}
        for ngramm in possible_ngramms:
            dict_[ngramm] = len(re.findall(ngramm, word, overlapped=True))
        return dict_

    def get_data(self):
        """
            make from window dict
        """
        metrics = {
            "median"    : self.median,
            "mean"      : self.mean,
            "variance"  : self.variance,
            "mean_abs"  : self.mean_abs,
            "max"       : self.max,
            "min"       : self.min,
            "sum"       : self.sum,
        }
        metrics.update(self.count_ngrams())

        return metrics, self.has_defect
