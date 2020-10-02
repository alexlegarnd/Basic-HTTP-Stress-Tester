import threading
import time
import queue
import os
import sys

def get_available_threads():
    if sys.platform == 'win32':
        return (int)(os.environ['NUMBER_OF_PROCESSORS'])
    else:
        return (int)(os.popen('grep -c cores /proc/cpuinfo').read())

SIZE = get_available_threads()
q = queue.Queue()
not_finished = True

class ProducerThread(threading.Thread):
    def __init__(self, threads):
        super(ProducerThread,self).__init__()
        self.threads = threads

    def run(self):
        global not_finished
        try:
            i = 0
            while i < len(self.threads):
                if q.qsize() < SIZE:
                    q.put(self.threads[i])
                    i += 1
            while q.qsize() > 0:
                time.sleep(1)
        except:
            pass
        not_finished = False


class ConsumerThread(threading.Thread):
    def __init__(self):
        super(ConsumerThread,self).__init__()

    def run(self):
        while not_finished:
            if q.qsize() > 0:
                t = q.get()
                t.start()
                t.join()

def start(threads):
    p = ProducerThread(threads)
    p.start()
    consumers = []
    for _ in range(get_available_threads()):
        c = ConsumerThread()
        consumers.append(c)
        c.start()
    p.join()
    for c in consumers:
        c.join()
    