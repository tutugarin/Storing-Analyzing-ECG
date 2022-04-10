"""
    ECG sygnal class is defined here
"""

class Sygnal:
    def __init__(self, data):
        """
            Initialize object with sygnal from database
        """
        self.data = data
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
