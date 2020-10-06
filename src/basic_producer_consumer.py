import threading
import time
import queue
import os
import sys

console = None

def get_available_threads():
    if sys.platform == 'win32':
        return (int)(os.environ['NUMBER_OF_PROCESSORS'])
    else:
        return (int)(os.popen('grep -c cores /proc/cpuinfo').read())

SIZE = get_available_threads()
q = queue.Queue()

class ProducerThread(threading.Thread):
    def __init__(self, threads):
        super(ProducerThread,self).__init__()
        self.threads = threads

    def run(self):
        try:
            i = 0
            while i < len(self.threads):
                if q.qsize() < SIZE:
                    q.put(self.threads[i])
                    i += 1
            while q.qsize() > 0:
                time.sleep(0.1)
        except Exception as e:
                console.print("[red]Error[/]: {}".format(e), style="bold")


class ConsumerThread(threading.Thread):
    def __init__(self):
        super(ConsumerThread,self).__init__()
        self.alive = True

    def stop(self):
        self.alive = False

    def run(self):
        while self.alive:
            try:
                if q.qsize() > 0:
                    t = q.get(False)
                    t.start()
                    if t.is_alive():
                        t.join(t.timeout)
            except queue.Empty as e:
                pass
            except Exception as e:
                console.print("[orange3]Warning[/]: {}".format(e), style="bold")

def start(threads):
    process(threads, get_available_threads())
    
def start_custom_limit(threads, limit):
    process(threads, limit)

def process(threads, limit):
    p = ProducerThread(threads)
    p.start()
    consumers = []
    for _ in range(limit):
        c = ConsumerThread()
        consumers.append(c)
        c.start()
    p.join()
    for c in consumers:
        c.stop()
    for c in consumers:
        if c.is_alive():
            c.join()