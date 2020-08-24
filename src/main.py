#!/usr/bin/python3

import sys
import time
import platform
import os
from rich import box
from rich.console import Console
from rich.table import Table
from thread import StressThread

console = Console(highlight=False)
VERSION = "1.2"

def main():
    if ((len(sys.argv) >= 2) and (("--help" in sys.argv) or ("/?" in sys.argv))):    
        show_author()
        show_help()
        return
    elif ((len(sys.argv) >= 2) and ("--version" in sys.argv)):
        show_version()
        return

    host = get_args("-h", True, 1001, 1002)
    allow_ssl = get_flag("--ssl")
    port = int(get_args("--port", False, 1003, 1004, "80"))
    path = get_args("-p", True, 1005, 1006)
    thread_number = int(get_args("-t", False, 1007, 1008, "5"))
    timeout = int(get_args("-tm", False, 1009, 1010, "10"))
    one_by_one = get_flag("--one-by-one")

    self_signed = get_flag("--allow-self-signed")

    start(host, port, path, timeout, thread_number, allow_ssl, self_signed, one_by_one)

def start(host, port, path, timeout, thread_number, allow_ssl, self_signed, one_by_one = False):
    thread_array = []
    for i in range(0, thread_number):
        thread_array.append(StressThread(host, port, path, timeout, i, allow_ssl, self_signed, VERSION))
    for t in thread_array:
        if one_by_one:
            t.run()
        else:
            try:
                t.start()
            except:
                b = False
                while not b:
                    try:
                        t.start()
                        b = True
                    except:
                        time.sleep(1)
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
    tresult = Table(title="Result", box=box.ASCII)
    tresult.add_column("Failed", style="red")
    tresult.add_column("Succeeded", style="green")
    tresult.add_column("Total", style="cyan")
    tresult.add_row(str(total - succeeded), str(succeeded), str(total))
    # Min, Max and Average Time
    ttime = Table(box=box.ASCII)
    ttime.add_column("Minimum", style="green")
    ttime.add_column("Maximum", style="red")
    ttime.add_column("Average", style="cyan")
    ttime.add_row(str(Tmin), str(Tmax), str(Tavg))
    console.print(tresult)
    console.print(ttime)

def show_help():
    console.print("")
    console.print("Usage: [bold]<executable> -h host -p path [--port port] [-t number_of_thread] [-tm timeout_in_second] [--ssl [--allow-self-signed]][/]")
    console.print("Exemple: st.exe -h www.google.fr -p / -t 10")
    console.print("         python main.py -h www.google.fr -p / -t 10")
    console.print("")
    console.print("Available arguments:")
    console.print("  -h host               The server IP or domain name")
    console.print("  -p path               The path of the HTTP resource")
    console.print("  --port port           The server HTTP port")
    console.print("  -t thread             Number of threads")
    console.print("  -tm second            Timeout of the request")
    console.print("  --one-by-one          Send request one by one")
    console.print("  --ssl                 Use HTTPS/SSL")
    console.print("  --allow-self-signed   Allow self signed SSL certificate")
    console.print("  --help")
    console.print("  /?                    Show this page")
    console.print("  --version             Get information about the application and the system")

def show_author():
    console.print("[bold]Basic HTTP Stress test[/]")
    console.print("by Alexis Delhaie ([bold blue]@alexlegarnd[/])")

def show_version():
    show_author()
    console.print()
    console.print("Version: [bold]{}[/]".format(VERSION))
    console.print("Python version: [bold]{}[/]".format(sys.version))
    console.print("User-Agent: [bold]PyStressTest/{}({} {} {})[/]".format(VERSION, platform.system(), os.name, platform.release()))

def get_args(header, important, notfoundcode, valuenotfoundcode, default = ""):
    if (header in sys.argv):
        try:
            i = sys.argv.index(header)
            if (len(sys.argv) > (i + 1)):
                return sys.argv[i + 1]
            elif important:
                console.print("[red]Error[/]: argument {} found but not the value".format(header), style="bold")
                show_help()
                sys.exit(valuenotfoundcode)
        except ValueError:
            console.print("[red]Error[/]: argument {} not found".format(header), style="bold")
            if important:
                show_help()
                sys.exit(notfoundcode)
    else:
        if important:
            console.print("[red]Error[/]: argument {} not found".format(header), style="bold")
            show_help()
            sys.exit(notfoundcode)
    return default

def get_flag(header):
    return (header in sys.argv)


main()