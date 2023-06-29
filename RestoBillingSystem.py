import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

#menu form
class menu(QDialog):
    def __init__(self):
        super(menu,self).__init__()
        loadUi("Menu.ui",self)
        self.addbttn.clicked.connect(self.gotoAddOrder)

    def gotoAddOrder(self):
        nxtForm = addOrder()
        widget.addWidget(nxtForm)
        widget.setCurrentIndex(widget.currentIndex()+1)

#add order form
class addOrder(QDialog):
    def __init__(self):
        super(addOrder,self).__init__()
        widget=QtWidgets.QStackedWidget()
        loadUi("AddOrder.ui",self)
        
app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
MainWindow=menu()
widget=QtWidgets.QStackedWidget()
widget.addWidget(MainWindow)
widget.setFixedWidth(1170)
widget.setFixedHeight(1090)
widget.show()
app.exec_()