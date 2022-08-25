from collections import OrderedDict

from main.bencoding import Decoder, Encoder

class TestDecoding():

    def test_peek_is_idempotent(self):
        decoder = Decoder(b'12')
        
        assert decoder._peek() == b'1'
        assert decoder._peek() == b'2'
    