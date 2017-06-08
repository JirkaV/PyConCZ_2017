import os
import multiprocessing
from time import sleep

from worker import worker
from feeder import feeder
from collector import collector

DEBUG = True

WANTED = 250
WORKERS_CNT = 5
MAX_QUEUE_SIZE = 200
STOP_MARKER = '::QUIT::'

if __name__ == '__main__':

    input_queue = multiprocessing.Queue(MAX_QUEUE_SIZE)
    results_queue = multiprocessing.Queue(MAX_QUEUE_SIZE)

    for x in range(WORKERS_CNT):
        p = multiprocessing.Process(target=worker,
                                    args=(input_queue, results_queue,
                                          STOP_MARKER, DEBUG))
        p.start()

    sleep(1)
    f = multiprocessing.Process(target=feeder,
                                args=(input_queue, WANTED, STOP_MARKER, DEBUG))
    f.start()

    collector(results_queue, STOP_MARKER, WORKERS_CNT, DEBUG)
