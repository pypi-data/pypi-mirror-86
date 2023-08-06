import subprocess
from colab_ssh import launch_ssh

def Connect(token, password):
  launch_ssh(token, password)
  import time 
  while True:
    time.sleep(300)