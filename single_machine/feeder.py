from random import randint

def feeder(queue, wanted, stop_marker, debug=False):
    if debug:
        print('[d] Feeder starting...')
    fed = 0
    while fed < wanted:
        try:
            data = randint(1, 10**10)
            queue.put(data)
            fed += 1
#             if debug:
#                 print('[d] Feeder: {} fed'.format(data))
        except KeyboardInterrupt:
            break
    queue.put(stop_marker)
    if debug:
        print('[d] Feeder quittting...')
