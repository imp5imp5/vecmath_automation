import requests
import time
import os
import shutil
from sys import platform

server_addr = os.getenv("VECMATH_SERVER", default="")
if server_addr == "":
  print("ERROR: env VECMATH_SERVER not set")
  quit()

os.system("echo \"Started\"")
logfile = os.path.abspath(os.getcwd()) + "/.log"
redirect = " >> " + logfile + " 2>&1"
server_path = "http://" + server_addr + ":20202"


def get_worker_id():
  try:
    with open(r'.worker_id', 'rt') as f:
      version = f.readline()
      return str(int(version))
  except:
    v = str(int(time.time() * 1000) % 90000 + 100000)
    with open(r'.worker_id', 'wt') as f:
      f.write(v)
    return v


def send_log_to_server():
  try:
    files = {'file': open(logfile, 'rb')}
    r = requests.post(server_path + "/" + get_worker_id(), files=files)
    print(r)
  except:
    print("send_log_to_server() - failed")


def exe(s):
  return os.system(s + redirect)

def build():
  print("Worker ID: " + get_worker_id())
  os.system("echo \"\\nBuild Start\\n\"")

  if platform == "win32":
    os.system("rd /s/q vecmath_test")
    os.system("date /T > " + logfile)
    exe("echo %PROCESSOR_IDENTIFIER%")
  else:
    shutil.rmtree('./vecmath_test', ignore_errors=True)
    os.system("date > " + logfile)
    exe("lscpu")


  exe("git clone https://github.com/imp5imp5/vecmath_test.git")

  if platform == "win32":
    exe("cd vecmath_test && mkdir build && cd build && cmake .. " + redirect +
        " && cmake --build . --target vecmath_test --config Release " + redirect + " && cd .. && cd ..")
    exe("vecmath_test\\build\\Release\\vecmath_test.exe " + redirect)
  else:
    exe("cd vecmath_test && mkdir build && cd build && cmake .. " + redirect +
        " && cmake --build . --target vecmath_test --config Release " + redirect + " && cd .. && cd ..")
    exe("./vecmath_test/build/vecmath_test " + redirect)
    exe("stdbuf -oL echo \" \n\" " + redirect) # flush

  time.sleep(3)
  send_log_to_server()
  os.system("echo \"\\nBuild Done\\n\"")



build()

def request_version():
  try:
    r = requests.get(server_path + '/versions/vec_math_version.txt')
    if r.status_code == 200:
      return r.text
  except:
    return "error"

  return ""

v = request_version()
while True:
  time.sleep(6)
  cur_v = request_version()
  if cur_v != v:
    v = cur_v
    build()

