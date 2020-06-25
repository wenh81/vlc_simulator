class Quadcells(object):
    def __init__(self, x, y, qc_type, has_microlens):
        """Constructor"""

        # X position of QC
        self.x_pos = x

        # Y position of QC
        self.y_pos = y
        self.qc_type = qc_type

        # indicates if has microlens or not
        self.has_microlens = has_microlens
    
        pass
