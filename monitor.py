#!/usr/bin/env python3
import os
import serial
from getch import _Getch
import threading
import time
import sys


class ListenOnSerialPort(threading.Thread):
    def __init__(self, keyboard_thread):
        threading.Thread.__init__(self)
        self.keyboard_thread = keyboard_thread

    def run(self):
        while True:
            if not self.keyboard_thread.input_active:
                line = ser.readline()
                try:
                    ser_in = line.decode('utf-8').strip('\n')
                    print(ser_in)
                except UnicodeDecodeError as e:
                    print("<<{}>>".format(line))


class ListenOnKeyboard(threading.Thread):
    input_active = False

    def run(self):
        while True:
            cmd_in = getch()
            print(cmd_in)
            if cmd_in == "i":  # if key 'i' is pressed
                self.input_active = True
                time.sleep(0.1)
                string = input(">> ")
                ser.write(string.encode())
                self.input_active = False
            elif cmd_in == "q":
                os._exit(1)


print("Press 'i' for sending data")
print("Press 'q' to quit")
if len(sys.argv) > 1:
	port = sys.argv[1]
else:
	port = input("port: ")
if len(sys.argv) > 2:
	baud = int(sys.argv[2])
else:
	baud = 9600

getch = _Getch()
print((port, baud))
ser = serial.Serial(port, baud)

kb_listen = ListenOnKeyboard()
sp_listen = ListenOnSerialPort(kb_listen)
kb_listen.start()
sp_listen.start()
