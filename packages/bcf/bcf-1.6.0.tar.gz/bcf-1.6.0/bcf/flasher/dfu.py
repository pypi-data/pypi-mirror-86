#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import __future__
import subprocess
import sys
import os
import platform
import time
import tempfile

dfu = "dfu-util"

dfu_help = '''
The device is probably not in DFU mode
    1. Make sure the USB cable is connected to your desktop (host).
    2. Press the BOOT button on Core Module and keep it pressed.
            BOOT button is on the right side and is marked with letter "B".
    3. Press the RESET button on Core Module while BOOT button is still held.
            RESET button is on the left side and is marked with letter "R".
    4. Release the RESET button.
    5. Release the BOOT button.
'''

dfu_help_install = '''
Please install dfu-util:
sudo apt install dfu-util
Or from https://sourceforge.net/projects/dfu-util/files/?source=navbar
'''

zadig_ini = '''
[general]
  # Start application in advanced mode (default = false)
  advanced_mode = false
  # Exit application upon successful driver installation (default = false)
  exit_on_success = true

[driver]
  # Select the following as the default driver to install:
  # WinUSB = 0, libusb0.sys = 1, libusbK.sys = 2, Custom = 3 (default = WinUSB)
  default_driver = 0

[device]
  VID = 0x0483
  PID = 0xDF11
  list_all = true

'''

help_url = "https://developers.bigclown.com/firmware/toolchain-guide#windows-dfu-driver-troubleshooting"


def call(cmd, title, reporthook):
    # print (' '. join([dfu] + cmd))
    try:
        proc = subprocess.Popen([dfu] + cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as identifier:
        raise Exception(dfu_help_install)

    t = 0
    procenta = 0
    out = b""
    while True:
        char = proc.stdout.read(1)
        if not char and proc.poll() is not None:
            break
        if char == b'\t':
            t = 1
            procenta = 0
        elif t:
            if t == 29 and char != b' ':
                procenta = int(char) * 100
            elif t == 30 and char != b' ':
                procenta += int(char) * 10
            elif t == 31:
                procenta += int(char)
            elif t == 32 and char == b'%':
                reporthook(title, procenta, 100)

            t += 1

        if not reporthook:
            sys.stdout.write(out.decode())

        out += char

    if isinstance(out, bytes):
        out = out.decode()

    if "Cannot open DFU device 0483:df11" in out:
        if sys.platform == 'win32':
            with open("zadig.ini", "w") as f:
                f.write(zadig_ini.replace('\r', '').replace('\n', '\r\n'))

            time.sleep(0.5)

            os.system("start zadig.exe")

            os.system("start " + help_url)

        raise Exception("Driver Error, more info here " + help_url)

    if "No DFU capable USB device available" in out:
        raise Exception(dfu_help)

    return out


def flash(filename_bin, reporthook, erase_eeprom=False):
    if erase_eeprom:
        eeprom_erase(reporthook)
        print()
        print("Please switch the core back to DFU mode")
        i = 9
        while i > 0:
            sys.stdout.write(str(i))
            sys.stdout.write('\r\r')
            sys.stdout.flush()
            time.sleep(1)
            if get_list_devices():
                print()
                break
            i -= 1

    cmd = ["-s", "0x08000000:leave", "-d", "0483:df11", "-a", "0", "-D", filename_bin]

    out = call(cmd, "Flash", reporthook)

    if "File downloaded successfully" not in out:
        raise Exception("Error \nlog: \n\n" + out)


def eeprom_erase(reporthook=None):

    fd, tmpfile = tempfile.mkstemp()
    f = os.fdopen(fd, "w+b")
    f.write(bytearray([0xff] * 6144))
    f.close()

    cmd = ["-s", "0x08080000:leave", "-d", "0483:df11", "-a", "2", "-D", tmpfile]

    for i in range(3):
        out = call(cmd, "Erase EEPROM", reporthook)

        if "Error during download get_status" in out:
            time.sleep(1)
        else:
            break

    os.unlink(tmpfile)

    if "File downloaded successfully" not in out:
        raise Exception("Error \nlog: \n\n" + out)


def eeprom_read(filename, address=0, length=6144, reporthook=None):
    start_address = 0x08080000 + address

    if os.path.exists(filename):
        os.unlink(filename)

    cmd = ["-s", hex(start_address) + ":leave", "-Z", str(length), "-d", "0483:df11", "-a", "2", "-U", filename]

    for i in range(3):
        out = call(cmd, "Read EEPROM", reporthook)

        if "Error during download get_status" in out:
            time.sleep(1)
        else:
            break

    if "Upload done." not in out:
        raise Exception("Error \nlog: \n\n" + out)


def get_list_devices():
    table = []
    try:
        proc = subprocess.Popen([dfu, '--list'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception:
        return table

    while 1:
        line = proc.stdout.readline()
        if not line and proc.poll() is not None:
            break
        line = line.decode()
        if line.startswith("Found DFU:"):
            serial = line.split()[-1]
            serial = 'dfu:' + serial[serial.find('"') + 1:-1]
            if serial not in table:
                table.append(serial)
    return table

# dfu-util -s 0x08080000 -d 0483:df11 -a 2 -U eeprom.bin
