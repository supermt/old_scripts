#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Echo server program
"""

import socket
import os

HOST = ''
PORT = 6666

file_path = "./t_order"
file_length = os.path.getsize(file_path)
target_file = open(file_path, "rb")
response_body = target_file.read(file_length)
print response_body

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    try:
        while True:
            conn, addr = s.accept()
            print('Connected by {}'.format(addr))

            income = conn.recv(1024)
            print income
            if not income:
                break
            conn.sendall(response_body)
            conn.close
    except:
        s.close()
    finally:
        s.close()

if __name__ == '__main__':
    main()
