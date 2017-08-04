import sys

from PyQt4.QtGui import QApplication

from mainwindow import MyMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = MyMainWindow()

    mainWindow.show()

    sys.exit(app.exec_())
