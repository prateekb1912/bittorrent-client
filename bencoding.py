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
    
    def encode_next(self, data):
        if type(data) == str:
            return self._encode_string(data)
        elif type(data) == int:
            return self._encode_int(data)
        elif type(data) == list:
            return self._encode_list(data)
    
    def _encode_string(self, data):
        return str.encode(str(len(data))+':' + data)

    def _encode_int(self, data):
        return str.encode('i'+str(data)+'e')

    def _encode_list(self, data):
        
        res = 'l'

        for elem in data:
            if type(elem) == str:
                res += f'{len(elem)}:{elem}'
            elif type(elem) == int:
                res += f'i{elem}e'
        
        res += 'e'

        return str.encode(res)

encoder = Encoder(['spam', 'eggs', 123])

print(encoder.encode())