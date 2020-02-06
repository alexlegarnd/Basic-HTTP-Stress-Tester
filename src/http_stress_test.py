#!/usr/bin/python3

import sys
import http.client
import threading
import time


class stressThread (threading.Thread):
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
    
    def isSucceeded(self):
        return self.success

    def getTime(self):
        return self.time

def start(host, port, path, timeout, threadnumber):
    threadArray = []
    for i in range(0, threadnumber):
        threadArray.append(stressThread(host, port, path, timeout, i))
    for t in threadArray:
        t.start()
    for t in threadArray:
        t.join()
    showStat(threadArray, (timeout * 1000))

def showStat(tArray, timeoutInMs):
    total, succeeded = [0, 0]
    Tmax, Tmin, Tavg = [0, timeoutInMs, 0]
    for t in tArray:
        total += 1
        Tavg += t.getTime()
        if t.getTime() > Tmax:
            Tmax = t.getTime()
        if t.getTime() < Tmin:
            Tmin = t.getTime()
        if t.isSucceeded():
            succeeded += 1
    Tavg = round(Tavg / total)
    print("====== FINISHED ======")
    print("Failed : {}, Succeeded : {}, Total : {}".format((total - succeeded), succeeded, total))
    print("Min : {} ms, Max : {} ms, Average : {} ms".format(Tmin, Tmax, Tavg))

def showHelp():
    print("")
    print("Usage: python http_stress_test.py -h host [-p port] -pth path [-t number_of_thread] [-tm timeout_in_second]")
    print("Exemple: python http_stress_test.py -h www.google.fr -pth / -t 10")
    print("")
    print("Available arguments:")
    print("  -h host      The server IP or domain name")
    print("  -p port      The server HTTP port")
    print("  -pth path    The path of the HTTP resource")
    print("  -t thread    Number of threads")
    print("  -tm second   Timeout of the request")

def getArgs(header, important, notfoundcode, valuenotfoundcode, default = ""):
    if (header in sys.argv):
        try:
            i = sys.argv.index(header)
            if (len(sys.argv) > (i + 1)):
                return sys.argv[i + 1]
            elif important:
                print ("Error: argument {} found but not the value".format(header))
                showHelp()
                sys.exit(valuenotfoundcode)
        except ValueError:
            print ("Error: argument {} not found".format(header))
            if important:
                showHelp()
                sys.exit(notfoundcode)
    else:
        if important:
            print ("Error: argument {} not found".format(header))
            showHelp()
            sys.exit(notfoundcode)
    return default

if ((len(sys.argv) >= 2) and (("--help" in sys.argv) or ("/?" in sys.argv))):    
    print("Basic HTTP Stress test")
    print("by Alexis Delhaie (@alexlegarnd)")
    showHelp()
    sys.exit(0);

host = getArgs("-h", True, 1001, 1002)
port = int(getArgs("-p", False, 1003, 1004, "80"))
path = getArgs("-pth", True, 1005, 1006)
tnumber = int(getArgs("-t", False, 1007, 1008, "5"))
timeout = int(getArgs("-tm", False, 1009, 1010, "10"))

start(host, port, path, timeout, tnumber)