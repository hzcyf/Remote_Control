# coding=utf-8
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget
from PyQt4.QtNetwork import QHostAddress
from PyQt4.QtNetwork import QTcpServer
from PyQt4.QtNetwork import QTcpSocket

from cmdp import CommandProcessor


class MyMainWindow(QWidget, CommandProcessor):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        self.my_serialreader.open()

        # UI
        self.super_layout = QtGui.QVBoxLayout()

        # port layout
        self.port_layout = QtGui.QHBoxLayout()
        self.port_lable = QtGui.QLabel(u"端口号:")
        self.port_value_text = QtGui.QLineEdit("8080")
        self.port_layout.addWidget(self.port_lable)
        self.port_layout.addWidget(self.port_value_text)

        # create layout
        self.create_layout = QtGui.QHBoxLayout()
        self.create_button = QtGui.QPushButton(u"创建")
        self.create_button.setFixedWidth(80)
        self.create_layout.addStretch()
        self.create_layout.addWidget(self.create_button)
        self.create_layout.addStretch()

        # self.line = QtGui.QTextLine()
        # self.line.
        self.super_layout.addLayout(self.port_layout)
        # self.super_layout.addWidget(self.line)
        self.super_layout.addLayout(self.create_layout)

        self.setLayout(self.super_layout)
        self.setWindowTitle("server")
        self.setGeometry(700, 400, 200, 200)

        self.my_tcp_server = myServer()

        self.set_signal()

    def set_signal(self):
        self.create_button.clicked.connect(self.create_button_Handler)
        self.my_tcp_server.dataComing_server.connect(self.motorCtrl)

    def create_button_Handler(self):
        self.my_tcp_server.listen(QHostAddress.Any, int(self.port_value_text.text()))

    def motorCtrl(self, fields):
        self.send_speed(int(fields[0]), 0x01)
        self.send_step(int(fields[1]), 0x01)


class myServer(QTcpServer):
    dataComing_server = pyqtSignal(list)

    def __init__(self):
        super(myServer, self).__init__()
        self.tcpClientSocketList = []

    def incomingConnection(self, socketDescriptor):
        print("connect coming!!!!")
        print type(socketDescriptor)
        my_tcp_socket = mySocket()
        my_tcp_socket.dataComing.connect(self.send_up)
        self.connect(my_tcp_socket, SIGNAL("disconnected(int)"), self.Disconnected_Handler)
        my_tcp_socket.setSocketDescriptor(socketDescriptor)
        self.tcpClientSocketList.append(my_tcp_socket)

    # slot
    def Disconnected_Handler(self, descriptor):
        for i in xrange(len(self.tcpClientSocketList)):
            item = self.tcpClientSocketList[i]
            if item.socketDescriptor() == descriptor:
                self.tcpClientSocketList.remove[i]
                print("Disconnected")
                return
        return

    def send_up(self, fields):
        self.dataComing_server.emit(fields)


class mySocket(QTcpSocket):
    dataComing = pyqtSignal(list)

    def __init__(self):
        super(mySocket, self).__init__()
        self.readyRead.connect(self.dataReceive_Handler)

    def dataReceive_Handler(self):
        while self.bytesAvailable() > 0:
            length = self.bytesAvailable()
            msg = self.read(length)
            # print(msg)
            fields = msg.split(':')
            # for i in xrange(len(fields)):
            #     print(fields[i])
            self.dataComing.emit(fields)
