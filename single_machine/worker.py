import os
from prime import is_prime

def worker(input_queue, results_queue, stop_marker, debug=False):
    if debug:
        print('[d] Worker {} starting...'.format(os.getpid()))

    while True:
        try:
            n = input_queue.get()
            if n == stop_marker:
                if debug:
                    print('[d] Worker stopping...')
                input_queue.put(stop_marker)  # for the other workers
                results_queue.put(stop_marker)  # for the collector
                return  # quit the worker

            result = is_prime(n)
#             if debug:
#                 print('[d] {} is {}a prime'.format(n, '' if result else 'not '))

            results_queue.put( (n, result) )  # (42, False) .. (73, True)
        except KeyboardInterrupt:
            pass