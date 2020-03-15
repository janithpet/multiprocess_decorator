import socket
import pickle

import argparse

if __name__ == '__main__':
    port = 9000
    host = 'localhost'

    s = socket.socket()
    s.connect((host, port))

    data = 'exit'
    data = pickle.dumps(data)
    s.sendall(data)

    s.close()