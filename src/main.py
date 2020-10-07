#!/usr/bin/python3

import os
import platform
import sys
import time

from rich import box
from rich.console import Console
from rich.table import Table

import core
import thread
from parameters import Options
from thread import StressThread

console = Console(highlight=False)
VERSION = "1.4.2"
thread.console = console

def main():
    if ((len(sys.argv) >= 2) and (("--help" in sys.argv) or ("/?" in sys.argv))):    
        show_author()
        show_help()
        return
    elif ((len(sys.argv) >= 2) and ("--version" in sys.argv)):
        show_version()
        return

    options = Options()
    options.host = get_args("-h", True, 1001, 1002)
    options.allow_ssl = get_flag("--ssl")
    options.port = int(get_args("--port", False, 1003, 1004, ("80", "443")[options.allow_ssl]))
    options.path = get_args("-p", False, 1005, 1006, "/")
    options.request_number = int(get_args("-r", False, 1007, 1008, "5"))
    options.limit = int(get_args("--thread-count", False, 1007, 1008, "1500"))
    options.timeout = int(get_args("--timeout", False, 1009, 1010, "10"))
    options.one_by_one = get_flag("--one-by-one")
    options.no_limit = get_flag("--no-limit")
    options.self_signed = get_flag("--allow-self-signed")
    options.headers = get_headers()

    if options.no_limit and (options.request_number < options.limit):
        console.print("[orange3]Warning[/]: Too much thread, starting only {} threads".format(options.request_number), style="bold")
        options.limit = options.request_number

    if options.one_by_one and options.no_limit:
        console.print("[red]Error[/]: ambigous arguments, --one-by-one and --no-limit cannot be in the same command", style="bold")
        return

    start(options)

def start(options):
    thread_array = []
    for i in range(0, options.request_number):
        thread_array.append(StressThread(options, i, VERSION))
    if options.one_by_one:
        core.start_one_by_one(thread_array)
    elif options.no_limit:
        core.start_custom_limit(thread_array, options.limit)
    else:
        core.start(thread_array)
    show_stat(thread_array, (options.timeout * 1000))

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
    console.print("Exemple: st -h www.google.fr -p / -t 10")
    console.print("         py main.py -h www.google.fr -p / -t 10")
    console.print("")
    console.print("Available arguments:")
    console.print("  -h host                              The server IP or domain name")
    console.print("  -p path                              The path of the HTTP resource")
    console.print("  -r <number_of_request>               Number of request")
    console.print("  --port port                          The server HTTP port")
    console.print("  --timeout <seconds>                  Timeout of the request")
    console.print("  --thread-count <number_of_threads>   Number of request")
    console.print("  --one-by-one                         Send request one by one")
    console.print("  --no-limit                           Disable CPU physical threads limit")
    console.print("  --ssl                                Use HTTPS/SSL")
    console.print("  --allow-self-signed                  Allow self signed SSL certificate")
    console.print("  --header \"key=value\"                 Send a custom header (To add several headers, add several times the argument --header)")
    console.print("  --help")
    console.print("  /?                                   Show this page")
    console.print("  --version                            Get information about the application and the system")

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

def get_headers():
    headers = {}
    indices = [i for i, x in enumerate(sys.argv) if x == "--header"]
    for i in indices:
        if (len(sys.argv) > (i + 1)):
            h_raw = sys.argv[i + 1]
            key, value = h_raw.split('=', 1)
            headers[key] = value
    return headers

def get_flag(header):
    return (header in sys.argv)


main()
