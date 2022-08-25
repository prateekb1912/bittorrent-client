from collections import OrderedDict

from main.bencoding import Decoder, Encoder

class DecodingTests():

    def test_peek_is_idempotent(self):
        decoder = Decoder(b'12')
        
        self.assertEqual(b'1', decoder._peek())
        self.assertEqual(b'2', decoder._peek())