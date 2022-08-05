from collections import OrderedDict

class Encoder:
    """
        Encodes a python object to a bencoded sequence of bytes.

        Supported python types:
            - int
            - string
            - list
            - dict
            -bytes
    """
    def __init__(self, data):
        self._data = data
    
    def encode(self):
        """
            Encode a python object to a bencoded binary string

            :return The bencoded binary string
        """

        return self.encode_next(self._data)