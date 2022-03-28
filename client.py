from __future__ import print_function
from prometheus_client import start_http_server, Summary
from base64 import decode, encode
from re import S
import csv
import socket
import struct
import time


REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

@REQUEST_TIME.time()
def main():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 5555))
        msg = s.recvfrom(1024)
        msg_bytes = bytes(msg[0])
        raw_data = struct.unpack("!QH%dsdI" % int.from_bytes(msg_bytes[11:12], "big") , msg_bytes[2:])
        data = [raw_data[0], raw_data[2].decode("ascii"), raw_data[3], raw_data[4]]
        # 
        with open('prices.csv', mode='a') as prices:
            prices_writer = csv.writer(prices, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 
            print("saving", data, "...")
            prices_writer.writerow([data])

if __name__ == "__main__":
    start_http_server(8000)
    main()