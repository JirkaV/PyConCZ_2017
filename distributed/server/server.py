from multiprocessing.managers import BaseManager
import queue

PORT = 12345
LISTEN_ADDRESS = ''
AUTHKEY = b'PyCon-CZ-2017'  # must be bytes
QUEUE_SIZE = 1000

class QueueManager(BaseManager):
    pass

if __name__ == '__main__':

    work_queue = queue.Queue(QUEUE_SIZE)
    results_queue = queue.Queue(QUEUE_SIZE)

    QueueManager.register('work_queue', lambda:work_queue)
    QueueManager.register('results_queue', lambda:results_queue)

    m = QueueManager(address=(LISTEN_ADDRESS, PORT), authkey=AUTHKEY)

    s = m.get_server()
    print('[i] Listening on {}:{}'.format(LISTEN_ADDRESS, PORT))
    s.serve_forever()
