#!/usr/bin/python
# program.py

import sys
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setGeometry(500,300,400,200)
        self.setWindowTitle('Program')

        exit = QtGui.QAction(QtGui.QIcon('grafika/exit.png'),
        'Wyjscie', self)
        exit.setShortcut('Ctrl+Q')

        self.connect(exit, QtCore.SIGNAL('triggered()'),
            QtCore.SLOT('close()'))

        menubar = self.menuBar()
        plik = menubar.addMenu('&Plik')
        plik.addAction(exit)

        self.widget=MyWidget(self)
        self.setCentralWidget(self.widget)

class MyWidget(QtGui.QWidget):
    def __init__(self,parent):
        QtGui.QWidget.__init__(self, parent)

        self.label = QtGui.QLabel("Przycisk:", self)
        self.label.setGeometry(10,0,40,30)

        ok = QtGui.QPushButton("Hej!",self)
        ok.setGeometry(10,30,60,20)

        cb1=QtGui.QCheckBox("pierwszy",self)
        cb1.setFocusPolicy(QtCore.Qt.NoFocus)
        cb1.move(120, 10)

        cb2=QtGui.QCheckBox("pierwszy",self)
        cb2.setFocusPolicy(QtCore.Qt.NoFocus)
        cb2.move(120, 30)

        cb3=QtGui.QCheckBox("pierwszy",self)
        cb3.setFocusPolicy(QtCore.Qt.NoFocus)
        cb3.move(120, 50)

        cb4=QtGui.QCheckBox("pierwszy",self)
        cb4.setFocusPolicy(QtCore.Qt.NoFocus)
        cb4.move(120, 70)

        combo = QtGui.QComboBox(self)
        combo.setGeometry(10,100,140,20)
        clist=['Horacy', 'Homer', 'Mozart', 'Czajkowski']

        tbox = QtGui.QLineEdit(self)
        tbox.setGeometry(10,130,140,20)

        radio1 = QtGui.QRadioButton("radio1",self)
        radio1.move(200,10)
        radio2 = QtGui.QRadioButton("radio2",self)
        radio2.move(200,30)
        radio3 = QtGui.QRadioButton("radio3",self)
        radio3.move(200,50)

apka = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(apka.exec_())
