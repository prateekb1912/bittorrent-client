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
        elif type(data) == bytes:
            return self._encode_bytes(data)
        elif type(data) == dict or type(data) == OrderedDict:
            return self._encode_dict(data)
        else: 
            return None
    
    def _encode_string(self, data):
        return str.encode(str(len(data))+':' + data)

    def _encode_int(self, data):
        return str.encode('i'+str(data)+'e')

    def _encode_bytes(self, data):
        res = bytearray()
        res += str.encode(str(len(data)))
        res += b':'
        res += data
        
        return res

    def _encode_list(self, data):
        
        res = bytearray('l', 'utf-8')
        res += b''.join([self.encode_next(d) for d in data])        
        res += b'e'

        return res
    
    def _encode_dict(self, data):
        res = bytearray('d', 'utf-8')

        for k,v in data.items():
            key = self.encode_next(k)
            val = self.encode_next(v)

            if key and val:
                res += key
                res += val
            else:
                raise RuntimeError('Bad dict')
            
        res += b'e'
        return res
d = OrderedDict()
d['cow'] = 'moo'
d['spam'] = 'eggs'

encoder = Encoder(d)
print(encoder.encode())