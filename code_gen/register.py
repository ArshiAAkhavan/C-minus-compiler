class RegisterFile:
    def __init__(self, sp_address, fp_address, ra_address, rv_address):
        self.sp = sp_address
        self.fp = fp_address
        self.ra = ra_address
        self.rv = rv_address
