import os
import sys

def get_available_threads():
    if sys.platform == 'win32':
        return (int)(os.environ['NUMBER_OF_PROCESSORS'])
    else:
        return (int)(os.popen('grep -c cores /proc/cpuinfo').read())

def start_one_by_one(threads):
    for t in threads:
        t.run()

def start(threads):
    process(threads, get_available_threads())
    
def start_custom_limit(threads, limit):
    process(threads, limit)

def process(threads, limit):
    started = []
    for t in threads:
        t.start()
        started.append(t)
        if len(started) >= limit:
            for s in started:
                if s.is_alive():
                    s.join()
            started.clear()
    for s in started:
        if s.is_alive():
            s.join()
