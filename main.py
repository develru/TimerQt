'''
Created on 04.07.2013

@author: uidv3540
'''
from PySide.QtUiTools import QUiLoader
from PySide import QtCore, QtGui
import sys
import qrc_timer  # @UnusedImport @UnresolvedImport


class SimplyTimer():
    def __init__(self):
#         super(SimplyTimer, self).__init__()

        loader = QUiLoader()
        uiFile = QtCore.QFile('./timer.ui')
        uiFile.open(QtCore.QFile.ReadOnly)
        self._myWidget = loader.load(uiFile)
        uiFile.close()

        self._tryIcon = QtGui.QSystemTrayIcon(self._myWidget)
        icon = QtGui.QIcon(QtGui.QPixmap(':/Timer.png'))
        self._myWidget.setWindowIcon(icon)
        self._tryIcon.setIcon(icon)
        self._myWidget.uiStartButton.clicked.connect(self.start)
        self._myWidget.stopButton.clicked.connect(self.stop)
        self._tryIcon.activated.connect(self.onTryClicked)

        self.__timeEdit = self._myWidget.uiTimeEdit
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.timerHit)

        self._updateTimer = QtCore.QTimer()
        self._updateTimer.timeout.connect(self.update)

        self._tryIcon.show()
        self._myWidget.show()

    def start(self):
        self._mytime = self.__timeEdit.time()
        ms = (self._mytime.second() * 1000 + self._mytime.minute() * 60 * 1000 +
              self._mytime.hour() * 60 * 60 * 1000)
        self._sec = ms / 1000

        self._timer.setInterval(ms)
        self._updateTimer.setInterval(1000)

        self._timer.start()
        self._updateTimer.start()
        #self._myWidget.hide()

    def stop(self):
        self._timer.stop()
        self._updateTimer.stop()

    def onTryClicked(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            if self._myWidget.isHidden():
                self._myWidget.show()
            else:
                self._myWidget.hide()

    def update(self):
        self._sec -= 1
        #print(self._sec)
        self._mytime = self._mytime.addSecs(-1)
        if not self._myWidget.isHidden():
            self.__timeEdit.setTime(self._mytime)

    def timerHit(self):
        self._timer.stop()
        self._updateTimer.stop()
        if self._myWidget.isHidden():
            self._myWidget.show()
        self._mytime = self._mytime.addSecs(-1)
        self.__timeEdit.setTime(self._mytime)
        msg = QtGui.QMessageBox()
        msg.setText("Timer is done")
        msg.exec_()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    myTimer = SimplyTimer()

    sys.exit(app.exec_())
