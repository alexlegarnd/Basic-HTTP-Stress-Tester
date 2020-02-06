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
You can download the installer on [here for Windows](www.python.org/downloads/windows/) and [here for macOS](https://www.python.org/downloads/mac-osx/)

## Example and minimal arguments
```sh
python3 http_stress_test.py -h host [-p port] -pth path [-t number_of_thread] [-tm timeout_in_second]
```
Your command must have -h (host IP or domain) and -pth (path to the resource)

Example:
```sh
python3 http_stress_test.py -h www.google.fr -pth / -t 10
```

