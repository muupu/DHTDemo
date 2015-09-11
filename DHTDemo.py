import socket
from random import randint
from hashlib import sha1
from bencode import bencode, bdecode
import threading
import time

BOOTSTRAP_NODES = (
    ("router.bittorrent.com", 6881),
    ("dht.transmissionbt.com", 6881),
    ("router.utorrent.com", 6881)
)


def entropy(length):
    return ''.join(chr(randint(0, 255)) for _ in range(length))

def random_id():
    h = sha1()
    e = entropy(20).encode('utf-8')
    h.update(e)  # 必须加.encode('utf-8')，否则报Unicode-objects must be encoded before hashing
    return h.digest()

def DHTServer(s):
    s.bind(('0.0.0.0', 6881))
    while True:
            try:
                (data, address) = s.recvfrom(65536)
                msg_dcode = bdecode(data)
                print('Received from %s:%s.\n' % address, msg_dcode)
            except Exception:
                pass

def DHTClient(s):
    trynum = 0
    while True:
        for address in BOOTSTRAP_NODES:
            nid = random_id()
            tid = entropy(2)
            msg = {
                "t": tid,
                "y": "q",
                "q": "find_node",
                "a": {
                    "id": nid,
                    "target": random_id()
                }
            }
            # print('Query msg %s:%s.' % address, msg)
            msg_bcode = bencode(msg)
            # print('bencode msg %s.' % msg_code)
            s.sendto(msg_bcode, address)
        trynum += 1
        print(trynum)
        time.sleep(3)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server = threading.Thread(target=DHTServer, name='DHTServer', args=(s,))
    client = threading.Thread(target=DHTClient, name='DHTClient', args=(s,))
    server.start()
    client.start()
    server.join()
    client.join()
