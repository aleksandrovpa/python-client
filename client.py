from __future__ import print_function
from prometheus_client import Summary, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Response, Flask
import csv
import socket
import struct
import time
from threading import Thread
import os

app = Flask(__name__)
life = 5
REQUEST_SUCCESS_COUNTER = Counter('request_success', 'Success requests count')
REQUEST_ERROR_COUNTER = Counter('request_error', 'Error requests count')

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_TIME_HISTOGRAM = Histogram(
    'request_time_histogram', 'Histogram for the duration in seconds', buckets=(0, 0.5, 1, 2, 5, 6, 10))


@REQUEST_TIME.time()
def fetch():
    start = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((os.environ['server_ip'], int(os.environ['server_port'])))
    msg = s.recvfrom(1024)
    msg_bytes = bytes(msg[0])
    raw_data = struct.unpack("!QH%dsdI" % int.from_bytes(
        msg_bytes[11:12], "big"), msg_bytes[2:])
    data = [raw_data[0], raw_data[2].decode("ascii"), raw_data[3], raw_data[4]]
    end = time.time()
    REQUEST_TIME_HISTOGRAM.observe(end - start)

    with open('prices.csv', mode='a') as prices:
        prices_writer = csv.writer(
            prices, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        prices_writer.writerow([data])


def main():
    global life
    print('Start fetching data...')
    while True:
        try:
            fetch()
            if life < 5:
                life += 1
            REQUEST_SUCCESS_COUNTER.inc()
        except BaseException as error:
            print(error)
            if life != 0:
                life -= 1
            REQUEST_ERROR_COUNTER.inc()
            time.sleep(1)


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/health")
def healthcheck():

    if life == 0:
        raise ValueError('A very specific bad thing happened')
    else:
        return "ok"


if __name__ == "__main__":
    thread = Thread(target=main)
    thread.start()
    app.run(host="0.0.0.0", port=8000)
