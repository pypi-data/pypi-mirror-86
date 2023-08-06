# -*- coding:utf-8 -*-
import serial
import time
from enum import Enum


class mode(Enum):
    Long = b"0xA50x500xF5"
    Quick = b"0xA50x510xF6"
    High = b"0xA50x520xF7"
    Normal = b"0xA50x530xF8"
    Save = b"0xA50x250xCA"
    Continuous = b"0xA50x450xEA"
    QUERY = b"0xA50x150xBA"


class baudRate(Enum):
    B9600 = b"0xA50xAE0x53"
    B115200 = b"0xA50xAF0x54"


class TOF:

    def open(baudRate=9600):
        global ser
        ser = serial.Serial("/dev/ttyAMA0", baudRate)
        ser.flushInput()
        ser.write(mode.Continuous)
        ser.write()

    def save():
        ser.write(mode.Save)

    def setMode(mode):
        ser.write(mode)

    def setBaudRate(baudRate):
        ser.write(baudRate)

    def distance():
        if ser is not None:
            count = ser.inWaiting()
            if count != 0:
                recv = ser.read(count)
                dis = ((ord(recv[4]) << 8) | ord(recv[5]))
                return dis
        return -1
