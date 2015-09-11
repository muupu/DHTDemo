__author__ = 'qiaoda.zqd'

import unittest
from bencode import bencode, decode_int, decode_string, decode_list, decode_dict, bdecode

class TestBdecode(unittest.TestCase):
    def test_decode_int(self):
        bstr = b'i123e'
        self.assertEqual((123, 5), decode_int(bstr, 0))

    def test_decode_string(self):
        bstr = b'3:abc'
        self.assertEqual((b'abc', 5), decode_string(bstr, 0))

    def test_decode_list(self):
        bstr = b'l4:spam4:eggse'
        # r, de_index = decode_list(bstr, 0)
        # self.assertListEqual([b'spam',b'eggs'], r)
        # self.assertEquals(14, de_index)
        self.assertEqual(([b'spam', b'eggs'], 14), decode_list(bstr, 0))

    def test_decode_dict(self):
        bstr = b'd2:id4:spam6:target4:eggse'
        # r, de_index = decode_list(bstr, 0)
        # self.assertListEqual([b'spam',b'eggs'], r)
        # self.assertEquals(14, de_index)
        self.assertEqual(({"id":b"spam", "target":b"eggs"}, 26), decode_dict(bstr, 0))

    def test_bdecode(self):
        bstr = b'd1:ad2:id20:abcdefghij01234567896:target20:mnopqrstuvwxyz123456e1:q9:find_node1:t2:aa1:y1:qe'
        bdestr = {"t":b"aa", "y":b"q", "q":b"find_node", "a": {"id":b"abcdefghij0123456789", "target":b"mnopqrstuvwxyz123456"}}
        self.assertEqual(bdestr, bdecode(bstr))


class TestBencode(unittest.TestCase):
    def test_encode_int(self):
        bstr = 123
        self.assertEqual(b'i123e', bencode(bstr))

    def test_encode_str(self):
        bstr = 'abc'
        self.assertEqual(b'3:abc', bencode(bstr))

    def test_encode_bytes(self):
        bstr = b'abc'
        self.assertEqual(b'3:abc', bencode(bstr))

    def test_encode_list(self):
        bstr = [ 'spam', 'eggs' ]
        self.assertEqual(b'l4:spam4:eggse', bencode(bstr))

    def test_encode_dict(self):
        bstr = {"id":"spam", "target":"eggs"}
        self.assertEqual(b'd2:id4:spam6:target4:eggse', bencode(bstr))

    def test_bencode(self):
        bstr = {"t":"aa", "y":"q", "q":"find_node", "a": {"id":"abcdefghij0123456789", "target":"mnopqrstuvwxyz123456"}}
        self.assertEqual(b'd1:ad2:id20:abcdefghij01234567896:target20:mnopqrstuvwxyz123456e1:q9:find_node1:t2:aa1:y1:qe',
                          bencode(bstr))

if __name__ == '__main__':
    unittest.main()
