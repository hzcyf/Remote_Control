# coding=utf-8
from __future__ import print_function
from time import sleep
from PyQt4.QtCore import QThread
from PyQt4.QtCore import pyqtSignal
from serial import Serial


class myserialreader(QThread):
    signal_cmd_complete = pyqtSignal(list)
    myserial = Serial()

    def __init__(self, parent=None):
        super(myserialreader, self).__init__(parent)
        self.__terminate = False
        self.myserial_open = False

    def open(self, settings=None):
        if settings is None:
            settings = {
                "port": "/dev/ttyACM0", "baund": 115200, "bytesize": 8,
                "parity": "N", "stopbits": 1, "timeout": 1}
        self.myserial = Serial(str(settings["port"]), settings["baund"], int(settings["bytesize"]),
                               str(settings["parity"]), int(settings["stopbits"]), int(settings["timeout"]))
        self.myserial.flushInput()
        self.myserial.flushOutput()
        self.myserial_open = True
        self.__terminate = False

    def terminate(self):
        print("__terminate")
        self.__terminate = True

    @property
    def __recv(self):
        recv_datastream = []
        while 1:
            if self.__terminate:
                break

            recv_data = self.myserial.read(1)
            if recv_data == '':
                sleep(0.1)
                continue
            print("cmd", end=': ')
            print(ord(recv_data), end=' ')
            recv_datastream.append(recv_data)
            while 1:
                n = self.myserial.inWaiting()
                if n > 0:
                    for i in range(n):
                        recv_data = self.myserial.read(1)
                        print(ord(recv_data), end=' ')
                        recv_datastream.append(recv_data)
                    sleep(0.02)
                else:
                    bk = True
                    break
            if bk:
                break
        return recv_datastream

    def close(self):
        if self.myserial.isOpen():
            self.myserial.close()

    def run(self):
        while 1:
            # data = []
            myrecv_data = self.__recv
            if self.__terminate:
                print("myserial.close")
                break
            # if not data:
            #     break

            # print myrecv_data
            # data = struct.unpack("s", myrecv_data[0])

            if len(myrecv_data) >= 4 and len(myrecv_data) == ord(myrecv_data[3]) + 5:
                # print ord(myrecv_data[3])
                self.signal_cmd_complete.emit(myrecv_data)  # 发送信号
        self.myserial.close()
        self.myserial_open = False
