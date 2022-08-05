from collections import OrderedDict

# Tokens indicating the start of data in the bencoded sequence

TOKEN_INTEGER = b'i'
TOKEN_LIST = b'l'
TOKEN_DICT = b'd'
TOKEN_END = b'e'


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


class Decoder:
    """
        Decodes a bencoded sequence of bytes
    """

    def __init__(self, data:bytes):
        if not isinstance(data, bytes):
            raise TypeError("Argument 'data' must be of type - 'bytes' ")
        
        self._data = data
        self._index = 0

    def decode(self):
        """
            Decodes the bencoded data and returns the matching python object

            :return A python object representing the bencoded data
        """
        c = self._peek()

        if c is None:
            raise EOFError('Unexpected end-of-file')
        elif c == TOKEN_INTEGER:
            self._consume()
            return self._decode_int()
        elif c.isdigit():
            self._consume()
            self._consume()
            return self._decode_str(int(c))


    def _peek(self):
        """
            Returns the next character of the bencoded data 
        """

        if self._index + 1 >= len(self._data):
            return None
        
        return self._data[self._index: self._index + 1]

    def _consume(self):
        """
            Read the next character from the data
        """
        self._index += 1
    
    def _decode_int(self):
        occ = self._data.index(TOKEN_END, self._index)
        res = self._data[self._index:occ]
        return int(res)

    def _decode_str(self, num):
        return self._data[self._index:self._index+num].decode('utf-8')


print(Decoder(b'4:eggs').decode())