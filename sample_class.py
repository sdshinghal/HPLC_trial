""" Trial with a class"""

class Sample:
    """Sample object with all its information"""
    def __init__(self, name):
        self.name = name
        self.vial_num = None
        self.volume = None
        self.row = None
        self.peak = None
        self.result = None

    def set_vial(self, vial_num):
        """ Add in vial number"""
        self.vial_num = vial_num

    def set_volume(self, volume):
        """ Add in volume"""
        self.volume = volume

    def set_row(self, row):
        """ Add in row"""
        self.row = row

    def set_peak(self, peak):
        """ Add in peak"""
        self.peak = peak

    def set_result(self, result):
        """ Add in result"""
        self.result = result

    def __str__(self):
        return self.name
