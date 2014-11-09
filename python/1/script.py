#!/usr/bin/env python
import sys
#sys.path.append('/usr/local/lib/python2.7/site-packages')
from WatermarkImage import WatermarkImage
from PyQt4 import QtGui, QtCore

global users_message



class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setGeometry(500,300,600,100)
        self.setWindowTitle('Koder informacji')

        exit = QtGui.QAction('Zakoncz program', self)
        exit.setShortcut('Ctrl+Q')

        self.connect(exit, QtCore.SIGNAL('triggered()'),
            QtCore.SLOT('close()'))

        menubar = self.menuBar()
        plik = menubar.addMenu('&Opcje')
        plik.addAction(exit)

        self.widget=MyWidget(self) 
        self.setCentralWidget(self.widget)

class MyWidget(QtGui.QWidget): 
    def __init__(self,parent):
        
        QtGui.QWidget.__init__(self, parent)
        self.label = QtGui.QLabel("Wpisz tekst do zakodowania:", self)
        self.label.setGeometry(10,0,150,30)

        self.labelek = QtGui.QLabel("", self)
        self.labelek.setGeometry(10,50,350,30)

        self.zatwierdz = QtGui.QLabel("", self)
        self.zatwierdz.setGeometry(450,0,20,30)

        self.obraztext = QtGui.QLabel("", self)
        self.obraztext.setGeometry(10,25,350,30)

        
        
        self.przyciskobraz = QtGui.QPushButton("Wybierz obraz",self)
        self.przyciskobraz.setGeometry(370,30,100,20)

        self.poletext = QtGui.QLineEdit(self) 
        self.poletext.setGeometry(160,5,200,20)

        self.przycisk = QtGui.QPushButton("Zatwierdz",self)
        self.przycisk.setGeometry(370,5,60,20)

        self.przycisk.clicked.connect(self.wpiszdostr) #jesli przycisk nacisniety
                                                    #skocz do wyswietl

        
        
    def wpiszdostr(self):
        self.zatwierdz.setText("Ok")
        newstring = self.poletext.text()
        global users_message
        users_message = str(newstring)
        self.przyciskobraz.clicked.connect(self.open)

    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                "Otworz grafike", '',"Grafika (*.bmp);;Wszystkie pliki (*)")
        
        self.obraztext.setText("Sciezka obrazu :     " + str(fileName))
        file_path = str(fileName)
        window = QtGui.QMessageBox()
        window.setGeometry(500, 200, 600, 600)
        window.setWindowTitle('Podglad Grafiki')
        window.setIconPixmap(QtGui.QPixmap(fileName))
        
       

#file_path = raw_input("Please enter file path")
#users_message = raw_input("Please enter your message")


        img = WatermarkImage(file_path, users_message)

        img_temporary = WatermarkImage(file_path, users_message)

        noise_optimal = 0
        max_error_rate = 10000
        for i in range(2,60):
            img_temporary.write_watermark(i)
            img_temporary.read_watermark()
            if img_temporary.error_rate < max_error_rate:
                max_error_rate = img_temporary.error_rate
                noise_optimal = i
            if max_error_rate == 0:
                break


        img.write_watermark(noise_optimal)


#####################################################################

#file_with_message_path = raw_input("Please enter file path")

#img_with_message_path = 'img_with_message.jpeg'

#img_to_decode = WatermarkImage()

#img_to_decode.set_img_with_message(img_with_message_path)

#img_to_decode.read_watermark()

        img.read_watermark()
#####################################################################
        img.write_all_images_to_files()
        odkodowany = img.message_detected
        self.labelek.setText("Pomyslnie odkodowano :     " + odkodowany)
        window.exec_()
        
apka = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(apka.exec_())
