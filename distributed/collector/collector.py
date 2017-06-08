import sys
from multiprocessing.managers import BaseManager
from time import sleep
from queue import Empty

DEBUG = True

SERVER_ADDRESS = '127.0.0.1'
PORT = 12345
AUTHKEY = b'PyCon-CZ-2017'  # must be bytes
STOP_MARKER = '::QUIT::'

class QueueManager(BaseManager):
    pass
QueueManager.register('results_queue')

if __name__ == '__main__':

    manager = QueueManager(address=(SERVER_ADDRESS, PORT), authkey=AUTHKEY)
    print('[i] Connecting to {}:{} ...'.format(SERVER_ADDRESS, PORT))
    manager.connect()
    print('[i] Connected')

    results_q = manager.results_queue()

    print('[d] Starting collector...')

    while True:

        try:
            elem = results_q.get_nowait()

            if elem == STOP_MARKER:
                pass  # left as a practice item for the reader :)

            n, result = elem

            if result:
                print('[d] {} is {}a prime'.format(n, '' if result else 'not '))

        except Empty:
            try:
                sleep(.1)  # this helps with KeyboardInterrupt
            except KeyboardInterrupt:
                print('[i] Quitting...')
                sys.exit()  # end the worker

    print('[i] Collector quitting...')
