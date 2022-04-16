"""
    ECG window class is defined here
"""

class Window:
    """
        Class for special interval of a processed signal
    """
    def __init__(self, interval):
        """
            Initialize object with interval (interval_size can differ)
        """
        self.interval = interval
        #  self.r_peaks = r_peaks
        self.window_size = len(interval)
