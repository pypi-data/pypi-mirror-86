# A control file for importing Boundary-Line.
# Not all areas have ONS codes, so we have to have something
# manual to e.g. tell us if some WMC have changed.
#
# Things without new ONS codes: CED


def check(name, type, country, geometry, **args):
    """Should return True if this area is NEW, False if we should match"""
    return False
