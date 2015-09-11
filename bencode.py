# The contents of this file are subject to the BitTorrent Open Source License
# Version 1.1 (the License).  You may not copy or use this file, in either
# source code or executable form, except in compliance with the License.  You
# may obtain a copy of the License at http://www.bittorrent.com/license/.
#
# Software distributed under the License is distributed on an AS IS basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.  See the License
# for the specific language governing rights and limitations under the
# License.

# Written by Petru Paler


def decode_int(bdata, de_index):
    de_index += 1
    e_index = bdata.index(b'e', de_index)
    n = int(bdata[de_index:e_index])
    if bdata[de_index] == b'-':
        if bdata[de_index + 1] == b'0':
            raise ValueError
    elif bdata[de_index] == b'0' and e_index != de_index+1:
        raise ValueError
    return (n, e_index+1)

def decode_string(bdata, de_index):
    colon = bdata.index(b':', de_index)
    n = int(bdata[de_index:colon])
    if bdata[de_index] == b'0' and colon != de_index+1:
        raise ValueError
    colon += 1
    return (bdata[colon:colon+n].decode('utf-8'), colon+n)

def decode_list(bdata, de_index):
    r, de_index = [], de_index+1
    while chr(bdata[de_index]) != 'e':
        #print('%d\n' % b'4')
        v, de_index = decode_func[chr(bdata[de_index])](bdata, de_index)
        r.append(v)
    return (r, de_index + 1)

def decode_dict(bdata, de_index):
    r, de_index = {}, de_index+1
    while chr(bdata[de_index]) != 'e':
        k, de_index = decode_string(bdata, de_index)
        r[k], de_index = decode_func[chr(bdata[de_index])](bdata, de_index)
    return (r, de_index + 1)

decode_func = {}
decode_func['l'] = decode_list
decode_func['d'] = decode_dict
decode_func['i'] = decode_int
decode_func['0'] = decode_string
decode_func['1'] = decode_string
decode_func['2'] = decode_string
decode_func['3'] = decode_string
decode_func['4'] = decode_string
decode_func['5'] = decode_string
decode_func['6'] = decode_string
decode_func['7'] = decode_string
decode_func['8'] = decode_string
decode_func['9'] = decode_string

def bdecode(bdata):
    try:
        r, l = decode_func[chr(bdata[0])](bdata, 0)
    except (IndexError, KeyError, ValueError):
        raise Exception("not a valid bencoded string")
    #if l != len(x):
    #    raise Exception("invalid bencoded value (data after valid prefix)")
    return r

#from types import StringType, IntType, LongType, DictType, ListType, TupleType
import types

class Bencached(object):

    __slots__ = ['bencoded']

    def __init__(self, s):
        self.bencoded = s

def encode_bencached(x,r):
    r.append(x.bencoded)

# 整数编码（<i>整数值<e>.可以为负数,如'i-3e'）
def encode_int(data, bcode_list):
    bcode_list.extend((b'i', str(data).encode('utf-8'), b'e'))

def encode_bool(x, r):
    if x:
        encode_int(1, r)
    else:
        encode_int(0, r)


def encode_string(x, r):
    r.extend((str(len(x)).encode('utf-8'), b':', x.encode('utf-8')))

# 字符串编码（<字符串长度>:字符串正文）
def encode_bytes(x, r):
    r.extend((str(len(x)).encode('utf-8'), b':', x))

# <l>  <e>
#  [ "spam", eggs" ] --> 'l4:spam4:eggse'
def encode_list(data, bcode_list):
    bcode_list.append(b'l')
    for i in data:
        encode_func[type(i)](i, bcode_list)
    bcode_list.append(b'e')

# <d><bencoded string><bencoded element><e>
# 字典必须根据主键预排序
def encode_dict(data,bcode_list):
    bcode_list.append(b'd')
    ilist = data.items()
    ilist = sorted(ilist)
    for k, v in ilist:
        bcode_list.extend((str(len(k)).encode('utf-8'), b':', str(k).encode('utf-8')))
        encode_func[type(v)](v, bcode_list)
    bcode_list.append(b'e')

encode_func = {}
encode_func[Bencached] = encode_bencached
encode_func[int] = encode_int
encode_func[int] = encode_int
encode_func[bytes] = encode_bytes
encode_func[str] = encode_string
encode_func[list] = encode_list
encode_func[tuple] = encode_list
encode_func[dict] = encode_dict
encode_func[bool] = encode_bool


def bencode(data):
    bcode_list = []
    encode_func[type(data)](data, bcode_list)
    return b''.join(bcode_list)
