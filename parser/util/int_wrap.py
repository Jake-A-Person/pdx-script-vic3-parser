
class IntWrap(object):
    """
    A wrapper for an int
    Used in Scope class to allow for ints to be passed by reference
    """
    def __init__(self, val):
        self.val = val