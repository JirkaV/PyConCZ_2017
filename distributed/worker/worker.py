import sys
from multiprocessing.managers import BaseManager
from time import sleep
from queue import Empty, Full

from prime import is_prime

DEBUG = True

SERVER_ADDRESS = '127.0.0.1'
PORT = 12345
AUTHKEY = b'PyCon-CZ-2017'  # must be bytes
STOP_MARKER = '::QUIT::'

class QueueManager(BaseManager):
    pass
QueueManager.register('work_queue')
QueueManager.register('results_queue')

if __name__ == '__main__':

    manager = QueueManager(address=(SERVER_ADDRESS, PORT), authkey=AUTHKEY)
    print('[i] Connecting to {}:{} ...'.format(SERVER_ADDRESS, PORT))
    manager.connect()
    print('[i] Connected')

    work_q = manager.work_queue()
    results_q = manager.results_queue()

    print('[d] Starting worker...')

    while True:

        try:
            n = work_q.get_nowait()

            if n == STOP_MARKER:
                print('[i] Stop marker encountered, quitting...')
                work_q.put(STOP_MARKER)  # for other workers, may take a while
                break

            try:
                result = is_prime(n)
            except KeyboardInterrupt:
                print('[i] Quitting...')
                sys.exit()  # end the worker
            if DEBUG:
                print('[d] {} is {}a prime'.format(n, '' if result else 'not '))

            sent = False
            while not sent:
                try:
                    # we purposefully put the "unpacked" version of target to the queue
                    results_q.put_nowait( (n, result) )
                    sent = True
                except Full:
                    try:
                        sleep(.1)  # this helps with KeyboardInterrupt
                    except KeyboardInterrupt:
                        print('[i] Quitting...')
                        sys.exit()  # end the worker
        except Empty:
            try:
                sleep(.1)  # this helps with KeyboardInterrupt
            except KeyboardInterrupt:
                print('[i] Quitting...')
                sys.exit()  # end the worker
