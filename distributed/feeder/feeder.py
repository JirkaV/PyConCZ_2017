from random import randint
from time import sleep
from multiprocessing.managers import BaseManager
from queue import Full

DEBUG = True

SERVER_ADDRESS = '127.0.0.1'
PORT = 12345
AUTHKEY = b'PyCon-CZ-2017'  # must be bytes
STOP_MARKER = '::QUIT::'

WANTED = 1000

class QueueManager(BaseManager):
    pass
QueueManager.register('work_queue')

if __name__ == '__main__':

    manager = QueueManager(address=(SERVER_ADDRESS, PORT), authkey=AUTHKEY)
    print('[i] Connecting to {}:{} ...'.format(SERVER_ADDRESS, PORT))
    manager.connect()
    print('[i] Connected')

    work_q = manager.work_queue()

    print('[i] Starting feeder loop...')
    fed = 0
    while fed < WANTED:
        try:
            data = randint(1, 10**10)
            work_q.put_nowait(data)
            fed += 1
            if DEBUG:
              print('[d] Feeder: {} fed'.format(data))
        except Full:
            if DEBUG:
                print('[d] queue full, sleeping')
            try:
                sleep(1)  # this helps with KeyboardInterrupt
            except KeyboardInterrupt:
                print('[i] Quitting...')
                break  # end the feeder loop

    work_q.put(STOP_MARKER)  # may take a while if queue is full
    print('[d] Feeder done')
