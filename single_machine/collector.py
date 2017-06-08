
def collector(results_queue, stop_marker, workers_count, debug=False):
    workers_finished = 0
    if debug:
        print('[d] Collector starting...')
    while workers_finished < workers_count:
        try:
            result = results_queue.get()
            if result == stop_marker:
                workers_finished += 1
                continue
            if result[1]:
                print('{} is {}a prime'.format(result[0], '' if result[1] else 'not '))
        except KeyboardInterrupt:
            pass
    if debug:
        print('[d] Collector quitting...')
