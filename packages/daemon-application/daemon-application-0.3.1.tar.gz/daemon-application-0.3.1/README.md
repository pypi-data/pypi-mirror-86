# daemon-application

Daemon application help functions.


## Install

```
pip install daemon-application
```

## Usage

**Example for raw apis**
```
import time
import threading
import signal
from daemon_application import daemon_start

stopflag = False

def main():
    def on_exit(*args, **kwargs):
        with open("backgroud.log", "a", encoding="utf-8") as fobj:
            print("process got exit signal...", file=fobj)
            print(args, file=fobj)
            print(kwargs, file=fobj)
        global stopflag
        stopflag = True
    signal.signal(signal.SIGTERM, on_exit)
    signal.signal(signal.SIGINT, on_exit)
    while not stopflag:
        time.sleep(1)
        print(time.time())

if __name__ == "__main__":
    print("start background application...")
    daemon_start(main, "background.pid", True)
```

**Example for DaemonApplication**

```
import time
from daemon_application import DaemonApplication

class HelloApplication(DaemonApplication):
    def main(self):
        while True:
            print("hello")
            time.sleep(1)

controller = HelloApplication().get_controller()

if __name__ == "__main__":
    controller()

```

## Release

### v0.3.1 2020/11/22

- Add DaemonApplication.

### v0.3.0 2020/11/21

- New wrapper.

### v0.2.1 2018/04/18

- Old releases.
