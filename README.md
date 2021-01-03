
# Basic HTTP Stress test
This is a little script wrote in Python 3. It's just for simulating multiple connection in same time.
## How to use it

 1. Install Python 3

Debian, Ubuntu
```sh
sudo apt install python3
```
Fedora
```sh
sudo dnf install python37
```
Redhat, CentOS
```sh
sudo yum install python3
```
Windows and macOS
You can download the installer on [here for Windows](https://www.python.org/downloads/windows/) and [here for macOS](https://www.python.org/downloads/mac-osx/)

## Example and minimal arguments
```sh
py main.py -h host -p path [--port port] [-t number_of_thread] [-tm timeout_in_second] [--ssl [--allow-self-signed]]
```
Your command must have -h (host IP or domain) and -p (path to the resource)

Example:
```sh
py main.py -h www.google.fr -p / -t 10
```
## Download
Portable version with Python 3.9 executable included : [Download here](https://alexisdelhaie.ovh/dlcenter/PyStressTest.7z) (for Windows only)
