import threading
import http.client
import platform
import time
import os
import ssl
import encodings.idna
from rich.console import Console

console = Console(highlight=False)

class StressThread (threading.Thread):

    def __init__(self, host, port, path, timeout, n, allow_ssl, self_signed, version):
        threading.Thread.__init__(self)
        self.user_agent = "PyStressTest/{}({} {} {})".format(version, platform.system(), os.name, platform.release())
        self.host = host
        self.port = port
        self.path = path
        self.timeout = timeout
        self.n = n
        self.allow_ssl = allow_ssl
        self.self_signed = self_signed
        self.success = False
        self.time = 0

    def run(self):
        try:
            print("Request {}: GET on {}".format(self.n, self.path))
            now = time.time()
            if self.allow_ssl:
                if self.self_signed:
                    c = http.client.HTTPSConnection(self.host, self.port, timeout=self.timeout, key_file=None, cert_file=None, context=ssl._create_unverified_context())
                else:
                    c = http.client.HTTPSConnection(self.host, self.port, timeout=self.timeout, key_file=None, cert_file=None)
            else:
                c = http.client.HTTPConnection(self.host, self.port, timeout=self.timeout)
            headers = {"User-Agent": self.user_agent}
            c.request(method="GET", url=self.path, headers=headers)
            res = c.getresponse()
            processed = round((time.time() - now) * 1000)
            self.print_result(res.status, res.reason, processed)
            self.time = processed
            if res.status < 400:
                self.success = True
        except Exception as e:
            console.print("Request {}: [bold red]{}[/]".format(self.n, e))
            print()
    
    def is_succeeded(self):
        return self.success

    def get_time(self):
        return self.time

    def print_result(self, code, reason, processed):
        if code >= 100 and code < 200:
            console.print("Request {}: [cyan]{} {}[/] (in [blue]{} ms[/])".format(self.n, code, reason, processed))
        elif code >= 200 and code < 300:
            console.print("Request {}: [green]{} {}[/] (in [blue]{} ms[/])".format(self.n, code, reason, processed))
        elif code >= 300 and code < 400:
            console.print("Request {}: [cyan]{} {}[/] (in [blue]{} ms[/])".format(self.n, code, reason, processed))
        elif code >= 400 and code < 500:
            console.print("Request {}: [orange]{} {}[/] (in [blue]{} ms[/])".format(self.n, code, reason, processed))
        else:
            console.print("Request {}: [red]{} {}[/] (in [blue]{} ms[/])".format(self.n, code, reason, processed))
