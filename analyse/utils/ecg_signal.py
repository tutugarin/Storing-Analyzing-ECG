"""
    ECG sygnal class is defined here
"""

class Sygnal:
    def __init__(self, name, data, info):
        """
            Initialize object with sygnal from database
        """
        self.name = name
        self.data = data

        self.sig_len = info['sig_len']
        self.sample_frequency = info['fs']
        self.sig_name = info['sig_name']

        self.windows = None

    def split(self, count):
        """
            Sptilt sygnal to windows with 'count' RR intervals
        """
        count=count
        pass

    def get_r_peaks(self):
        """
            Returns indecis of R peaks
        """
        pass
