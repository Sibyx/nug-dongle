# nug-dongle

Simple network server based on [asyncio](https://docs.python.org/3/library/asyncio-protocol.html) module aimed to
execute commands from the nug-server KVM switch. Server accept decoded messages from RFB server which forward using
HID which acts like input device on connected computer. We use
[USB Gadget API for Linux](https://www.kernel.org/doc/html/v4.19/driver-api/usb/gadget.html) to act like a mouse or
keyboard.

This project is a part of my master thesis on the
[Faculty of Informatics and Information Technologies STU in Bratislava](https://www.fiit.stuba.sk/en.html) on the
subject of KVM switch implementation.

We use [Poetry](https://python-poetry.org/) as a package manager.

---
With ❤️☕️🥃🍀 Jakub Dubec 2022
