#!/usr/bin/env python3 -u
import os
import serial
from getch import _Getch
import threading
import time
import sys


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def ser_reset_on_start():
    global ser
    ser.dtr = False
    ser.rts = False


def ser_reset():
    global ser
    ser.dtr = True
    ser.rts = True
    time.sleep(0.1)
    ser.rts = False
    ser.dtr = False


class ListenOnSerialPort(threading.Thread):
    def __init__(self, keyboard_thread):
        threading.Thread.__init__(self)
        self.keyboard_thread = keyboard_thread

    def run(self):
        global serial_opened
        while True:
            if not self.keyboard_thread.input_active:
                if not serial_opened:
                    time.sleep(0.5)
                    continue
                try:
                    c = ser.read()
                except serial.serialutil.SerialException:
                    continue
                try:
                    ser_in = c.decode('utf-8')
                    print(ser_in, end='')
                except UnicodeDecodeError as e:
                    print("<{}>".format(c))


class ListenOnKeyboard(threading.Thread):
    input_active = False

    def run(self):
        global serial_opened
        while True:
            cmd_in = getch()
            print(cmd_in)
            if cmd_in == "i":  # if key 'i' is pressed
                self.input_active = True
                time.sleep(0.1)
                string = input(">> ")
                string += line_end
                ser.write(string.encode())
                self.input_active = False
            elif cmd_in == "c":
                if serial_opened:
                    serial_opened = False
                    ser.close()
                    print("Serial closed")
                else:
                    ser.open()
                    serial_opened = True
                    print("Serial opened")
            elif cmd_in == "C":
                if not serial_opened:
                    ser_reset()
                    print("Serial reset")
            elif cmd_in == "q":
                os._exit(1)


print("Press 'i' for sending data")
print("Press 'q' to quit")
print("For ESP8266 based boards pass true as third parameter")
if len(sys.argv) > 1:
	port = sys.argv[1]
else:
	port = input("port: ")
if len(sys.argv) > 2:
	baud = int(sys.argv[2])
else:
	baud = 9600
line_end = ''
if len(sys.argv) > 3:
	line_end = eval('"'+sys.argv[3]+'"')
print(F"LE=\"{''.join(hex(ord(i)) for i in line_end)}\"")

getch = _Getch()
print((port, baud))
ser = serial.Serial(port, baud)

if len(sys.argv) > 3 and str2bool(sys.argv[3]):
    ser_reset_on_start()
serial_opened = True

kb_listen = ListenOnKeyboard()
sp_listen = ListenOnSerialPort(kb_listen)
kb_listen.start()
sp_listen.start()
