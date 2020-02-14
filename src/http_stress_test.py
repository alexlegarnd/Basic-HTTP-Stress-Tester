#!/usr/bin/python3

import sys
import http.client
import threading
import time


class StressThread (threading.Thread):
    def __init__(self, host, port, path, timeout, n):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.path = path
        self.timeout = timeout
        self.n = n
        self.success = False
        self.time = 0

    def run(self):
        try:
            print("Request {}: GET on {}".format(self.n, self.path))
            now = time.time()            
            c = http.client.HTTPConnection(self.host, self.port, timeout=self.timeout)
            c.request("GET", self.path)
            res = c.getresponse()
            processed = round((time.time() - now) * 1000)
            print("Request {}: {} {} (in {} ms)".format(self.n, res.status, res.reason, processed))
            self.time = processed
            if res.status < 400:
                self.success = True
        except Exception as e:
            print("Request {}: {}".format(self.n, e))
    
    def is_succeeded(self):
        return self.success

    def get_time(self):
        return self.time

def start(host, port, path, timeout, thread_number, one_by_one = False):
    thread_array = []
    for i in range(0, thread_number):
        thread_array.append(StressThread(host, port, path, timeout, i))
    for t in thread_array:
        if one_by_one:
            t.run()
        else:
            t.start()
    if not one_by_one:
        for t in thread_array:
            t.join()
    show_stat(thread_array, (timeout * 1000))

def show_stat(tArray, timeoutInMs):
    total, succeeded = [0, 0]
    Tmax, Tmin, Tavg = [0, timeoutInMs, 0]
    for t in tArray:
        total += 1
        Tavg += t.get_time()
        if t.get_time() > Tmax:
            Tmax = t.get_time()
        if t.get_time() < Tmin:
            Tmin = t.get_time()
        if t.is_succeeded():
            succeeded += 1
    Tavg = round(Tavg / total)
    print("====== FINISHED ======")
    print("Failed : {}, Succeeded : {}, Total : {}".format((total - succeeded), succeeded, total))
    print("Min : {} ms, Max : {} ms, Average : {} ms".format(Tmin, Tmax, Tavg))

def show_help():
    print("")
    print("Usage: python http_stress_test.py -h host [-p port] -pth path [-t number_of_thread] [-tm timeout_in_second]")
    print("Exemple: python http_stress_test.py -h www.google.fr -pth / -t 10")
    print("")
    print("Available arguments:")
    print("  -h host        The server IP or domain name")
    print("  -p port        The server HTTP port")
    print("  -pth path      The path of the HTTP resource")
    print("  -t thread      Number of threads")
    print("  -tm second     Timeout of the request")
    print("  --one-by-one   Send request one by one")

def get_args(header, important, notfoundcode, valuenotfoundcode, default = ""):
    if (header in sys.argv):
        try:
            i = sys.argv.index(header)
            if (len(sys.argv) > (i + 1)):
                return sys.argv[i + 1]
            elif important:
                print ("Error: argument {} found but not the value".format(header))
                show_help()
                sys.exit(valuenotfoundcode)
        except ValueError:
            print ("Error: argument {} not found".format(header))
            if important:
                show_help()
                sys.exit(notfoundcode)
    else:
        if important:
            print ("Error: argument {} not found".format(header))
            show_help()
            sys.exit(notfoundcode)
    return default

def get_flag(header):
    return (header in sys.argv)

if ((len(sys.argv) >= 2) and (("--help" in sys.argv) or ("/?" in sys.argv))):    
    print("Basic HTTP Stress test")
    print("by Alexis Delhaie (@alexlegarnd)")
    show_help()
    sys.exit(0);

host = get_args("-h", True, 1001, 1002)
port = int(get_args("-p", False, 1003, 1004, "80"))
path = get_args("-pth", True, 1005, 1006)
thread_number = int(get_args("-t", False, 1007, 1008, "5"))
timeout = int(get_args("-tm", False, 1009, 1010, "10"))
one_by_one = get_flag("--one-by-one")

start(host, port, path, timeout, thread_number, one_by_one)