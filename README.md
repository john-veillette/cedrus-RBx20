# Python controller for Cedrus RB-x20 button boxes

The RB-x20 series of button boxes aren't compatible with Cedrus's own [Python library](https://github.com/cedrus-opensource/pyxid), so you instead have to interact with them like normal serial devices. The `RBx20` class in this module will handle that for you, providing a simplified interface for collecting reaction times and other button responses. It depends on `pyserial` and `psychopy`.

For simplicity, only works with box set to ASCII protocol, which means the first switch must be down and the second must be up.

The other two switches on the box control the baud rate. The default (when both are down) is 19,200 Hz, which is also the default for the `cedrus.RBx20` class. Whatever you do, just make sure they match.

You'll need the serial number for your hardware to initialize the controller. You can print the hardware information for all the available serial ports with:

```
from cedrus import print_ports
print_ports()
```

Once you have the serial number for the hardware you want to communicate with, you can begin using your box as follows.

```
from cedrus import RBx20
serial_number = '<your serial number>'
box = RBx20(serial_number) # optional second argument is baudrate  
key, rt = box.waitKeys(timeout = 1.) # default is no timeout
```

The response times are relative to the last clock reset. The clock is reset and the buffer is cleared, by default, every time you run `box.waitKeys()` or `box.waitPress()` by default, but this behavior can be disabled like `box.waitKeys(reset = False)`.

If you're collecting RT measurements at the same time as your experiment code is doing something else, the accuracy of your timestamps may be affected by whatever else is going on in the main process. In that case, you may want to consider running `box.waitKeys` asyncronously (e.g. in another thread or process) to improve your RT measurements.

### Usage Note

If you're connecting via a USB-to-serial interface rather than a native serial port (which you probably are, cause who has serial ports anymore), you need to use a VCP driver instead of a D2xx driver. These two driver types can't be used in parallel for whatever reason, so you can't use `cedrus.RBx20` with any software that utilizes D2xx drivers.

Some software, annoyingly, will block VCP drivers system-wide upon install (like [RTBox](https://github.com/xiangruili/RTBox_py/blob/master/setup_ftd2xx.sh)). You may want to check to make sure this hasn't happened to your system at any point in the past. In Ubuntu, for example, you should check that the line `blacklist ftdi_sio` isn't in `/etc/modprobe.d/blacklist.conf`.
