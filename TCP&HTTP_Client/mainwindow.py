# coding=utf-8
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtNetwork

from PyQt4.QtCore import QString
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QPen
from PyQt4.QtNetwork import QHostAddress


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.serverIP = QHostAddress()
        self.port = 8010

        self.super_Vlayout = QtGui.QVBoxLayout()

        # value_layout
        self.value_layout = QtGui.QHBoxLayout()
        self.speed_value_lable = QtGui.QLabel(u"速度(step/s):")
        self.speed_value_text = QtGui.QLineEdit()
        self.step_value_lable = QtGui.QLabel(u"    步值(step):")
        self.step_value_text = QtGui.QLineEdit()
        self.value_layout.addWidget(self.speed_value_lable)
        self.value_layout.addWidget(self.speed_value_text)
        self.value_layout.addWidget(self.step_value_lable)
        self.value_layout.addWidget(self.step_value_text)

        # send_layout
        self.send_layout = QtGui.QHBoxLayout()
        self.send_button = QtGui.QPushButton(u"发送")
        self.send_button.setEnabled(False)
        self.send_button.setFixedWidth(100)
        self.send_layout.addStretch()
        self.send_layout.addWidget(self.send_button)
        self.send_layout.addStretch()

        # ip_layout
        self.ip_layout = QtGui.QHBoxLayout()
        self.ip_lable = QtGui.QLabel(u"IP地址: ")
        self.ip_value_text = QtGui.QLineEdit("192.168.1.128")
        self.ip_layout.addWidget(self.ip_lable)
        self.ip_layout.addWidget(self.ip_value_text)

        # port_layout
        self.port_layout = QtGui.QHBoxLayout()
        self.port_lable = QtGui.QLabel(u"端口号: ")
        self.port_value_text = QtGui.QLineEdit("8080")
        self.port_layout.addWidget(self.port_lable)
        self.port_layout.addWidget(self.port_value_text)

        # connect_layout
        self.connect_layout = QtGui.QHBoxLayout()
        self.connect_button = QtGui.QPushButton(u"连接")
        self.connect_button.setFixedWidth(100)
        self.connect_layout.addStretch()
        self.connect_layout.addWidget(self.connect_button)
        self.connect_layout.addStretch()

        self.super_Vlayout.addLayout(self.value_layout)
        self.super_Vlayout.addLayout(self.send_layout)
        self.super_Vlayout.addLayout(self.ip_layout)
        self.super_Vlayout.addLayout(self.port_layout)
        self.super_Vlayout.addLayout(self.connect_layout)

        self.setLayout(self.super_Vlayout)
        self.setWindowTitle("Client")
        self.setGeometry(700, 300, 300, 300)

        self.my_tcp_socket = QtNetwork.QTcpSocket(self)

        self.set_signal()

    def set_signal(self):
        self.send_button.clicked.connect(self.send_button_Handler)
        self.connect_button.clicked.connect(self.connect_button_Handler)
        self.connect(self.my_tcp_socket, SIGNAL("connected()"), self.slotConnected)
        self.connect(self.my_tcp_socket, SIGNAL("disconnected()"), self.slotDisconnected)
        self.connect(self.my_tcp_socket, SIGNAL("readyRead()"), self.dataReceived)

    def send_button_Handler(self):
        msg = self.speed_value_text.text() + ":" + self.step_value_text.text()
        self.my_tcp_socket.writeData(msg.toUtf8())

    def connect_button_Handler(self):
        if self.connect_button.text() == u"连接":
            self.serverIP.setAddress(self.ip_value_text.text())
            self.my_tcp_socket.connectToHost(self.serverIP.toString(), int(self.port_value_text.text()))
        else:
            self.my_tcp_socket.disconnectFromHost()

    def dataReceived(self):
        while self.my_tcp_socket.bytesAvailable() > 0:
            length = self.my_tcp_socket.bytesAvailable()
            msg = QString(self.my_tcp_socket.read(length))
            msg = msg.fromUtf8(msg)
            # self.ListWidgetContent.addItem(msg.fromUtf8(msg))

    def slotConnected(self):
        self.send_button.setEnabled(True)
        self.connect_button.setText(u"断开连接")

        # self.PushButtonLeave.setText(self.tr(u"断开链接"))

        # msg = self.userName + ":" + self.tr("进入聊天室")
        # length = self.tcpSocket.writeData(msg.toUtf8())
        # if length != msg.toUtf8().length():
        #     return

    def slotDisconnected(self):
        self.send_button.setEnabled(False)
        self.connect_button.setText(u"连接")

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        # mySize = self.size()
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        myLocation = self.geometry()
        pen.setWidth(1)
        pen.setStyle(Qt.CustomDashLine)
        pen.setDashPattern([1, 2, 1, 2])
        pen.setColor(QColor(55, 55, 55))
        qp.setPen(pen)
        qp.drawLine(0, myLocation.height()*0.4+4, myLocation.width(), myLocation.height()*0.4+4)
        qp.drawLine(0, myLocation.height()*0.4+3, myLocation.width(), myLocation.height()*0.4+3)
        qp.drawLine(0, myLocation.height()*0.4+2, myLocation.width(), myLocation.height()*0.4+2)
        pen.setWidth(3)
        pen.setDashPattern([1, 1, 1, 1])
        qp.setPen(pen)
        qp.drawLine(0, myLocation.height()*0.4-2, 5, myLocation.height()*0.4+3)
        qp.drawLine(0, myLocation.height()*0.4, 3, myLocation.height()*0.4+3)
        qp.drawLine(0, myLocation.height()*0.4+8, 5, myLocation.height()*0.4+3)
        qp.drawLine(0, myLocation.height()*0.4+6, 3, myLocation.height()*0.4+3)
        qp.drawLine(myLocation.width()-6, myLocation.height()*0.4+3, myLocation.width(), myLocation.height()*0.4-2)
        qp.drawLine(myLocation.width()-3, myLocation.height()*0.4+3, myLocation.width(), myLocation.height()*0.4)
        qp.drawLine(myLocation.width()-6, myLocation.height()*0.4+3, myLocation.width(), myLocation.height()*0.4+8)
        qp.drawLine(myLocation.width()-3, myLocation.height()*0.4+3, myLocation.width(), myLocation.height()*0.4+6)
