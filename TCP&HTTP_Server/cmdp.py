# coding=utf-8
from PyQt4 import QtGui
from time import sleep

from MySerial import myserialreader
import struct


class CommandProcessor:
    def __init__(self):
        pass

    my_cmd = {
        # cmd : len(data)
        0x00: 1,  # led
        0x01: 8,  # motor

    }

    motor_id = {
        # index : id
        0x01: 5,   # motor1
        0x02: 6,   # motor2
        0x04: 7,   # motor3
        0x08: 8,   # motor4
        0x10: 9,   # motor5
        0x20: 10,  # motor6
        0x40: 11,  # motor7
        0x80: 12   # motor8
    }

    my_serialreader = myserialreader()

    def create_cmd(self, cmd, data_buf):
        len_data = self.my_cmd.get(cmd)
        sum = 0x59 + cmd + len_data
        if sum >= 256:
            sum -= 256
        cmd_buf = [0xaa, 0xaf, cmd, len_data]

        for i in range(0, len_data):  # range(0,len_data) 中不包含 len_data
            cmd_buf.append(data_buf[i])
            sum += data_buf[i]
            if sum >= 256:
                sum -= 256
        cmd_buf.append(sum)
        print cmd_buf
        return cmd_buf

    def send_cmd(self, cmd, data_buf):
        cmd_buf = self.create_cmd(cmd, data_buf)
        if self.my_serialreader.myserial_open:
            for i in range(0, cmd_buf[3] + 5):
                self.my_serialreader.myserial.write(chr(cmd_buf[i]))
        else:
            QtGui.QMessageBox.information(self, "Tips", u"请先打开串口")

    def send_speed(self, speed, motor_index):
        keyword = 0x01
        while 1:
            if motor_index & keyword:
                data_buf = [self.motor_id.get(keyword), 4, 0x87, 0]
                speed_stream = struct.pack("i", speed)
                for i in range(4):
                    data_buf.append(ord(speed_stream[i]))
                    # print data_buf
                print ("set speed = " + str(speed))
                self.send_cmd(0x01, data_buf)
                sleep(0.1)
            if keyword == 0x80:
                break
            keyword <<= 1

    def send_step(self, step, motor_index):
        keyword = 0x01
        while 1:
            if motor_index & keyword:
                #           |motor_id|len of can data|TCW|global|
                data_buf = [self.motor_id.get(keyword), 4, 0x8A, 0]
                speed_stream = struct.pack("i", step)
                for i in range(4):
                    data_buf.append(ord(speed_stream[i]))
                print data_buf
                print ("set step = " + str(step))
                self.send_cmd(0x01, data_buf)
                sleep(0.1)
            if keyword == 0x80:
                break
            keyword <<= 1

    def get_state(self, motor_index, cmd):
        keyword = 0x01
        while 1:
            if motor_index & keyword:
                #           |motor_id|len of can data|TCW|global|
                data_buf = [self.motor_id.get(keyword), 0, cmd, 0]
                # speed_stream = struct.pack("i", step)
                for i in range(4):
                    data_buf.append(0)
                # print data_buf
                # print ("set step = " + str(step))
                self.send_cmd(0x01, data_buf)
                sleep(0.1)
            if keyword == 0x80:
                break
            keyword <<= 1
