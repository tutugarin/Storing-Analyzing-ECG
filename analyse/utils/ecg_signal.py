"""
    ECG signal class is defined here
"""

class Signal:
    def __init__(self, name, data, info):
        """
            Initialize object with signal from database
        """
        self.name = name
        self.data = data

        self.sig_len = info['sig_len']
        self.sample_frequency = info['fs']
        self.sig_name = info['sig_name']

        self.windows = None

    def split(self, count):
        """
            Split signal to windows with 'count' RR intervals
        """
        count = count
        pass

    def get_r_peaks(self):
        """
            Returns indexes of R peaks
        """
        pass
