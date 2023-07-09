import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QLabel, QAbstractItemView, QMessageBox, QTreeWidgetItem
from PyQt5.QtGui import QPixmap, QPainter, QPdfWriter, QPageSize
from PyQt5.QtCore import QDate, QTimer, QTimer, QTime, Qt
from PyQt5.uic import loadUi
from reportlab.pdfgen import canvas
import random, codecs

orders_data = {}

class Orders:
    def __init__(self):
        self.data = orders_data
    
    def orderInfo(self, orderNum, orderCode, name, date, time, total, subtotal, vat, modeOfPayment, M1, M2, M3, M4, M5, S1, S2, S3, S4, S5, D1, D2, D3, D4, D5, B1, B2, B3, B4, B5, status):
        self.data[orderNum] = {
            'orderCode' : orderCode, 'name' : name, 'date' : date, 'time' : time, 'total' : total, 
            'subtotal' : subtotal, 'vat' : vat, 'modeOfPayment' : modeOfPayment,
            'M1' : M1, 'M2' : M2, 'M3' : M3, 'M4': M4, 'M5': M5,
            'S1' : S1, 'S2' : S2, 'S3' : S3, 'S4': S4, 'S5': S5,
            'D1' : D1, 'D2' : D2, 'D3' : D3, 'D4': D4, 'D5': D5,
            'B1' : B1, 'B2' : B2, 'B3' : B3, 'B4': B4, 'B5': B5,
            'status' : status
        }
    
    def searchOrdersByDate(self, search_date):
        global orders_data 
        filtered_orders = {}
        for order_num, order_data in self.data.items():
            if order_data['date'] == search_date:
                filtered_orders[order_num] = order_data
        orders_data = filtered_orders

class foodDesc:
    def __init__(self):
        self.M1_prc = 220.00; self.M2_prc = 160.00; self.M3_prc = 180.00; self.M4_prc = 200.00; self.M5_prc = 190.00
        self.S1_prc = 80.00; self.S2_prc = 60.00; self.S3_prc = 75.00; self.S4_prc = 90.00; self.S5_prc = 35.00
        self.D1_prc = 100.00; self.D2_prc = 90.00; self.D3_prc = 80.00; self.D4_prc = 85.00; self.D5_prc = 90.00
        self.B1_prc = 30.00; self.B2_prc = 20.00; self.B3_prc = 55.00; self.B4_prc = 80.00; self.B5_prc = 40.00

        self.M1_name = "Pan Fried Salmon"; self.M2_name = "Crispy Baked Chicken"; self.M3_name = "Teriyaki Chicken Bowl"; self.M4_name = "Golden Shrimp"; self.M5_name = "Stuffed Chicken Breast"
        self.S1_name = "French Fries with Aioli"; self.S2_name = "Collard Greens"; self.S3_name = "Chipotle Mashed Potato"; self.S4_name = "Pesto Pasta Salad"; self.S5_name = "Steamed Rice"
        self.D1_name = "Tiramisu"; self.D2_name = "Cheesecake with Berries"; self.D3_name = "Creme Caramel"; self.D4_name = "Blackberry Pie"; self.D5_name = "Red Velvet Cake"
        self.B1_name = "Soda Water"; self.B2_name = "500mL Bottled Mineral Water"; self.B3_name = "Fresh Orange Juice"; self.B4_name = "Milkshake"; self.B5_name = "Iced Tea"

# allocating data in the table
class DataAdder():
    def __init__(self, table_widget):
        self.table = table_widget
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Prevent editing cells
        self.order = Orders()

    def add_data(self, food_code, food_picture, price, quantity, amount):
        existing_row_index = self.search_table(food_code, 0)

        if existing_row_index > -1:
            current_quantity = int(self.table.item(existing_row_index, 3).text())
            current_amount = float(self.table.item(existing_row_index, 4).text())

            new_quantity = current_quantity + quantity
            new_amount = current_amount + amount

            self.set_table_item(existing_row_index, 3, new_quantity)
            self.set_table_item(existing_row_index, 4, new_amount) 

            if food_code is not None:
                self.order.data[food_code] = new_quantity
        else:
            if food_code is not None:
                self.order.data[food_code] = quantity
            # Set data in each column
            row_index = self.table.rowCount()
            self.table.insertRow(row_index)
            self.set_table_item(row_index, 0, food_code)
            self.set_table_item(row_index, 1, food_picture)
            self.set_table_item(row_index, 2, "{:.2f}".format(price))
            self.set_table_item(row_index, 3, quantity)
            self.set_table_item(row_index, 4, amount)
            
            self.table.setRowHeight(row_index, 60)
            
    def set_table_item(self, row, column, value):
        if column == 1:
            image_label = QLabel()
            pixmap = QPixmap(value)
            image_label.setPixmap(pixmap)
            image_label.setScaledContents(True)
            self.table.setCellWidget(row, column, image_label)
        else:
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, column, item)

    def search_table(self, target_value, column):
        for row in range(self.table.rowCount()):
            item = self.table.item(row, column)
            if item is not None and item.text() == target_value:
                return row
        return -1

class MessageBox:
    def show_warning_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)

        button_ok = msg_box.button(QMessageBox.Ok)
        button_ok.clicked.connect(msg_box.reject)  # Prevent UI exit on 'OK' button click

        msg_box.exec_()
    
    def show_info_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Information")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)

        button_ok = msg_box.button(QMessageBox.Ok)
        button_ok.clicked.connect(msg_box.reject) 

        msg_box.exec_()
    
    def show_question_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)  # Updated line
        msg_box.setWindowTitle("Confirmation")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        if msg_box.exec_() == QMessageBox.Yes:  # Check the result of the message box
            return True
        else:
            return False


class FileHandling:
    def __init__(self):
        self.mssgBox = MessageBox()

    def appendOrder(self):
        file_name = "ordersData.txt"
        
        order_info = f"{orders_data['orderCode']},{orders_data['name']},{orders_data['date']},{orders_data['time']},"
        order_info += f"{orders_data['total']},{orders_data['subtotal']},{orders_data['vat']},{orders_data['modeOfPayment']},"
        order_info += f"{orders_data['M1']},{orders_data['M2']},{orders_data['M3']},{orders_data['M4']},{orders_data['M5']},"
        order_info += f"{orders_data['S1']},{orders_data['S2']},{orders_data['S3']},{orders_data['S4']},{orders_data['S5']},"
        order_info += f"{orders_data['D1']},{orders_data['D2']},{orders_data['D3']},{orders_data['D4']},{orders_data['D5']},"
        order_info += f"{orders_data['B1']},{orders_data['B2']},{orders_data['B3']},{orders_data['B4']},{orders_data['B5']},{orders_data['status']}"
        enc_data = self.encrypt(order_info, 20)
        try:
            with codecs.open(file_name, 'a', encoding='utf-8') as file:
                file.write(enc_data + '\n')
            
        except IOError as ex:
            self.mssgBox.show_warning_message_box("Error appending to the file.")
    
    def saveOrder(self):
        file_name = "ordersData.txt"
        try:
            with codecs.open(file_name, 'w', encoding='utf-8') as file:
                for order_num, order_data in orders_data.items():
                    order_info = f"{order_data['orderCode']},{order_data['name']},{order_data['date']},{order_data['time']},"
                    order_info += f"{order_data['total']},{order_data['subtotal']},{order_data['vat']},{order_data['modeOfPayment']},"
                    order_info += f"{order_data['M1']},{order_data['M2']},{order_data['M3']},{order_data['M4']},{order_data['M5']},"
                    order_info += f"{order_data['S1']},{order_data['S2']},{order_data['S3']},{order_data['S4']},{order_data['S5']},"
                    order_info += f"{order_data['D1']},{order_data['D2']},{order_data['D3']},{order_data['D4']},{order_data['D5']},"
                    order_info += f"{order_data['B1']},{order_data['B2']},{order_data['B3']},{order_data['B4']},{order_data['B5']},{order_data['status']}"
                    enc_data = self.encrypt(order_info, 20)
                    file.write(enc_data + '\n')
        except IOError as ex:
            self.mssgBox.show_warning_message_box("Error writing to the file.")

    def RetrieveOrder(self):
        file_name = "ordersData.txt"
        self.addOrder = Orders()
        orderNum = 1
        try:
            with codecs.open(file_name, 'r', encoding='utf-8') as file:
                for line in file:
                    decrypted_data = self.decrypt(line.strip(), 20)
                    if decrypted_data:
                        data = decrypted_data.split(',')
                        self.addOrder.orderInfo(orderNum,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],data[17],data[18],data[19],data[20],data[21],data[22],data[23],data[24],data[25],data[26],data[27],data[28])
                        orderNum += 1
        except:
            self.mssgBox.show_warning_message_box("Error reading the file.")

    def encrypt(self, text, shift):
        char_list = list(text)  # Convert the string to a list of characters
        for i in range(len(char_list)):
            char_list[i] = chr(ord(char_list[i]) + shift)  # Modify the character
        encrypted_text = ''.join(char_list)  # Convert the list back to a string
        return encrypted_text

    def decrypt(self, text, shift):
        char_list = list(text)  
        for i in range(len(char_list)):
            char_list[i] = chr(ord(char_list[i]) - shift)  
        decrypted_text = ''.join(char_list) 
        return decrypted_text


#menu form
class Menu(QDialog):
    def __init__(self):
        super(Menu,self).__init__()
        self.widget=QtWidgets.QStackedWidget()
        loadUi("Menu.ui",self)
        self.addbttn.clicked.connect(self.gotoAddOrder)
        self.displayBttn.clicked.connect(self.gotoDisplayOrders)
        self.adminbttn.clicked.connect(self.gotoAdmin)

    def gotoAddOrder(self):
        nxtForm = AddOrder()
        widget.addWidget(nxtForm)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoDisplayOrders(self):
        nxtForm = DisplayAllOrders()
        widget.addWidget(nxtForm)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoAdmin(self):
        nxtForm = Admin()
        widget.addWidget(nxtForm)
        widget.setCurrentIndex(widget.currentIndex()+1)

#add order form
class AddOrder(QDialog):
    def __init__(self):
        super(AddOrder,self).__init__()
        self.widget=QtWidgets.QStackedWidget()
        loadUi("AddOrder.ui",self)

        self.order = Orders()
        self.food = foodDesc()
        self.mssgBox = MessageBox()
        self.allocateData = DataAdder(self.ordersTable)
        self.displayDateTime()
        
        # Buttons for dish category selection 
        self.main.clicked.connect(lambda: self.dishPicker(1))
        self.sides.clicked.connect(lambda: self.dishPicker(2))
        self.desserts.clicked.connect(lambda: self.dishPicker(3))
        self.beverages.clicked.connect(lambda: self.dishPicker(4))

        # Food quantity selection 
        self.addBttn_main1.clicked.connect(self.add_m1)
        self.addBttn_main2.clicked.connect(self.add_m2)
        self.addBttn_main3.clicked.connect(self.add_m3)
        self.addBttn_main4.clicked.connect(self.add_m4)
        self.addBttn_main5.clicked.connect(self.add_m5)

        self.addBttn_side1.clicked.connect(self.add_s1)
        self.addBttn_side2.clicked.connect(self.add_s2)
        self.addBttn_side3.clicked.connect(self.add_s3)
        self.addBttn_side4.clicked.connect(self.add_s4)
        self.addBttn_side5.clicked.connect(self.add_s5)

        self.addBttn_dessert1.clicked.connect(self.add_d1)
        self.addBttn_dessert2.clicked.connect(self.add_d2)
        self.addBttn_dessert3.clicked.connect(self.add_d3)
        self.addBttn_dessert4.clicked.connect(self.add_d4)
        self.addBttn_dessert5.clicked.connect(self.add_d5)

        self.addBttn_bev1.clicked.connect(self.add_b1)
        self.addBttn_bev2.clicked.connect(self.add_b2)
        self.addBttn_bev3.clicked.connect(self.add_b3)
        self.addBttn_bev4.clicked.connect(self.add_b4)
        self.addBttn_bev5.clicked.connect(self.add_b5)

        self.deleteOrder.clicked.connect(self.delete_selected_row)
        self.proceed.clicked.connect(self.gotoUserInfo)
        
    def displayDateTime(self):
        now = QDate.currentDate()
        self.lblDate.setText(now.toString(Qt.DefaultLocaleLongDate))
        timer = QTimer(self)
        # adding action to timer
        timer.timeout.connect(self.showTime)
        # update the timer every second
        timer.start(1000)
    def showTime(self):
        # getting current time
        current_time = QTime.currentTime()
        # converting QTime object to string
        label_time = current_time.toString('hh:mm:ss')
        self.lblTime.setText(label_time)

    def dishPicker(self, x):
        if x == 1:
            self.orderStackedWidget.setCurrentWidget(self.mainPanel)
            self.main.setStyleSheet("QPushButton#main { background-color: rgb(188, 214, 249); }")
            self.sides.setStyleSheet("background-color: rgb(247, 236, 240)")
            self.desserts.setStyleSheet("background-color: rgb(247, 236, 240)")
            self.beverages.setStyleSheet("background-color: rgb(247, 236, 240)")
        elif x == 2:
            self.orderStackedWidget.setCurrentWidget(self.sidePanel)
            self.sides.setStyleSheet("QPushButton#sides { background-color: rgb(188, 214, 249); }")
            self.main.setStyleSheet("background-color: rgb(247, 236, 240)")
            self.desserts.setStyleSheet("background-color: rgb(247, 236, 240)")
            self.beverages.setStyleSheet("background-color: rgb(247, 236, 240)")
        elif x == 3:
            self.orderStackedWidget.setCurrentWidget(self.dessertPanel)
            self.desserts.setStyleSheet("QPushButton#desserts { background-color: rgb(188, 214, 249); }")
            self.main.setStyleSheet("background-color: rgb(247, 236, 240)")
            self.sides.setStyleSheet("background-color: rgb(247, 236, 240)")
            self.beverages.setStyleSheet("background-color: rgb(247, 236, 240)")
        elif x == 4:
            self.orderStackedWidget.setCurrentWidget(self.beveragePanel)
            self.beverages.setStyleSheet("QPushButton#beverages { background-color: rgb(188, 214, 249); }")
            self.main.setStyleSheet("background-color: rgb(247, 236, 240)")
            self.sides.setStyleSheet("background-color: rgb(247, 236, 240)")
            self.desserts.setStyleSheet("background-color: rgb(247, 236, 240)")

    #add functions for main dishes
    def add_m1(self):
        m1 = self.qtty_main1.toPlainText()
        self.check(m1, 'M1', self.food.M1_prc, 'food_pics/pan fried salmon.PNG')
        self.qtty_main1.setText('')
    def add_m2(self):
        m2 = self.qtty_main2.toPlainText()
        self.check(m2, 'M2', self.food.M2_prc, 'food_pics/crissy baked chicken.PNG')
        self.qtty_main2.setText('')
    def add_m3(self):
        m3 = self.qtty_main3.toPlainText()
        self.check(m3, 'M3', self.food.M3_prc, 'food_pics/teriyaki chicken bowl.PNG')
        self.qtty_main3.setText('')
    def add_m4(self):
        m4 = self.qtty_main4.toPlainText()
        self.check(m4, 'M4', self.food.M4_prc, 'food_pics/golden shrimp.PNG')
        self.qtty_main4.setText('')
    def add_m5(self):
        m5 = self.qtty_main5.toPlainText()
        self.check(m5, 'M5', self.food.M5_prc, 'food_pics/stuffed chicken breast.PNG')
        self.qtty_main5.setText('')
    
    #add functions for side dishes
    def add_s1(self):
        s1 = self.qtty_side1.toPlainText()
        self.check(s1, 'S1', self.food.S1_prc, 'food_pics/French fries with aoili.PNG')
        self.qtty_side1.setText('')
    def add_s2(self):
        s2 = self.qtty_side2.toPlainText()
        self.check(s2, 'S2', self.food.S2_prc, 'food_pics/Sautee Collard Greens.PNG')
        self.qtty_side2.setText('')
    def add_s3(self):
        s3 = self.qtty_side3.toPlainText()
        self.check(s3, 'S3', self.food.S3_prc, 'food_pics/Chipotle Mashed Potatoes.PNG')
        self.qtty_side3.setText('') 
    def add_s4(self):
        s4 = self.qtty_side4.toPlainText()
        self.check(s4, 'S4', self.food.S4_prc, 'food_pics/Pesto Pasta Salad.PNG')
        self.qtty_side4.setText('') 
    def add_s5(self):
        s5 = self.qtty_side5.toPlainText()
        self.check(s5, 'S5', self.food.S5_prc, 'food_pics/Steamed rice.PNG')
        self.qtty_side5.setText('') 

    #add fucntions for desserts
    def add_d1(self):
        d1 = self.qtty_dessert1.toPlainText()
        self.check(d1, 'D1', self.food.D1_prc, 'food_pics/tiramisu.PNG')
        self.qtty_dessert1.setText('')
    def add_d2(self):
        d2 = self.qtty_dessert2.toPlainText()
        self.check(d2, 'D2', self.food.D2_prc, 'food_pics/cheesecake w berries.PNG')
        self.qtty_dessert2.setText('')
    def add_d3(self):
        d3 = self.qtty_dessert3.toPlainText()
        self.check(d3, 'D3', self.food.D3_prc, 'food_pics/Creme caramel.PNG')
        self.qtty_dessert3.setText('') 
    def add_d4(self):
        d4 = self.qtty_dessert4.toPlainText()
        self.check(d4, 'D4', self.food.D4_prc, 'food_pics/Blackberry pie.PNG')
        self.qtty_dessert4.setText('') 
    def add_d5(self):
        d5 = self.qtty_dessert5.toPlainText()
        self.check(d5, 'D5', self.food.D5_prc, 'food_pics/Red Velvet cake.PNG')
        self.qtty_dessert5.setText('')          
    
    #add functions fot beverages
    def add_b1(self):
        b1 = self.qtty_bev1.toPlainText()
        self.check(b1, 'B1', self.food.B1_prc, 'food_pics/soda water.PNG')
        self.qtty_bev1.setText('')
    def add_b2(self):
        b2 = self.qtty_bev2.toPlainText()
        self.check(b2, 'B2', self.food.B1_prc, 'food_pics/bottled water.PNG')
        self.qtty_bev2.setText('')
    def add_b3(self):
        b3 = self.qtty_bev3.toPlainText()
        self.check(b3, 'B3', self.food.B3_prc, 'food_pics/orange juice.PNG')
        self.qtty_bev3.setText('')
    def add_b4(self):
        b4 = self.qtty_bev4.toPlainText()
        self.check(b4, 'B4', self.food.B4_prc, 'food_pics/milkshake.PNG')
        self.qtty_bev4.setText('')
    def add_b5(self):
        b5 = self.qtty_bev5.toPlainText()
        self.check(b5, 'B5', self.food.B5_prc, 'food_pics/iced tea.PNG')
        self.qtty_bev5.setText('')
    
    def check(self, qtty, code, price, pic):
        if code not in self.order.data:
            self.order.data[code] = 0
        if qtty.isdigit() and qtty != 0:
            qtty = int(qtty)
            self.order.data[code] += qtty
            subTotal = self.subAmount(price, qtty)
            self.allocateData.add_data(code, pic, price, qtty, subTotal)

    def subAmount(self, price, quantity):
        subTotal = price * quantity
        if 'subtotal' not in self.order.data:
            self.order.data['subtotal'] = 0
        self.order.data['subtotal'] += subTotal
        self.total_lbl.setText("{:.2f}".format(self.order.data['subtotal']))
        return subTotal

    def delete_selected_row(self):
        rows = self.ordersTable.rowCount()
        selected_row = self.ordersTable.currentRow()

        if rows == 0:
            self.mssgBox.show_warning_message_box("Empty order.")
        elif selected_row < 0:
            self.mssgBox.show_warning_message_box("Please select one order to be deleted.")
        else:
            sub = self.ordersTable.item(selected_row, 4)
            if sub is not None:
                sub = float(sub.text())
                self.order.data['subtotal'] -= sub
            self.total_lbl.setText("{:.2f}".format((self.order.data['subtotal'])))
            self.ordersTable.removeRow(selected_row)
            if selected_row < rows - 1:
                for row in range(selected_row, rows - 1):
                    for col in range(self.ordersTable.columnCount()):
                        item = self.ordersTable.item(row + 1, col)
                        if item is not None:
                            self.ordersTable.setItem(row, col, QTableWidgetItem(item.text()))
                    self.ordersTable.removeRow(rows - 1)
                    
    def gotoUserInfo(self):
        if self.ordersTable.rowCount() > 0:
            orderCode = random.randint(1000,9999)
            if 'orderCode' not in orders_data:
                self.order.data['orderCode'] = 0
            self.order.data['orderCode'] = orderCode
            self.gettingTotalAmount()
            nxtForm = UserInfo()
            nxtForm.ordersTable = self.ordersTable 
            widget.addWidget(nxtForm)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            self.mssgBox.show_warning_message_box("Please enter an order first.")
        
    def gettingTotalAmount(self):
        sub = float(self.order.data['subtotal'])
        tax = float(sub * 0.12)
        totalAmt = float(sub + tax)
        if 'vat' not in orders_data:
            self.order.data['vat'] = tax
        self.order.data['vat'] = "{:.2f}".format(tax)
        if 'total' not in orders_data:
            self.order.data['total'] = 0
        self.order.data['total'] = "{:.2f}".format(totalAmt)

#user information form
class UserInfo(QDialog):
    def __init__(self):
        super(UserInfo,self).__init__()
        self.widget=QtWidgets.QStackedWidget()
        loadUi("UserInfo.ui",self)
        self.displayDateTime()
        self.orderLabels()
        self.mssgBox = MessageBox()
        self.saveBttn.clicked.connect(self.save_print)
        self.comboBoxMOP.activated.connect(self.comBox)
        self.order = Orders()
        self.file = FileHandling()
        self.ordersTable = None
        
    def displayDateTime(self):
        now = QDate.currentDate()
        self.lblDate.setText(now.toString(Qt.DefaultLocaleLongDate))
        timer = QTimer(self)
        # adding action to timer
        timer.timeout.connect(self.showTime)
        # update the timer every second
        timer.start(1000)
    def showTime(self):
        # getting current time
        current_time = QTime.currentTime()
        # converting QTime object to string
        label_time = current_time.toString('hh:mm:ss')
        self.lblTime.setText(label_time)

    def orderLabels(self):
        self.lblOrderNum.setText(str(self.printValue('orderCode')))
        self.lblSubTotal.setText("{:.2f}".format(float(self.printValue('subtotal'))))
        self.lblVat.setText("{:.2f}".format(float(self.printValue('vat'))))
        self.lblTotal.setText("{:.2f}".format(float(self.printValue('total'))))

        self.lineEditM1.setText(str(self.printValue('M1')))
        self.lineEditM2.setText(str(self.printValue('M2')))
        self.lineEditM3.setText(str(self.printValue('M3')))
        self.lineEditM4.setText(str(self.printValue('M4')))
        self.lineEditM5.setText(str(self.printValue('M5')))

        self.lineEditS1.setText(str(self.printValue('S1')))
        self.lineEditS2.setText(str(self.printValue('S2')))
        self.lineEditS3.setText(str(self.printValue('S3')))
        self.lineEditS4.setText(str(self.printValue('S4')))
        self.lineEditS5.setText(str(self.printValue('S5')))

        self.lineEditD1.setText(str(self.printValue('D1')))
        self.lineEditD2.setText(str(self.printValue('D2')))
        self.lineEditD3.setText(str(self.printValue('D3')))
        self.lineEditD4.setText(str(self.printValue('D4')))
        self.lineEditD5.setText(str(self.printValue('D5')))

        self.lineEditB1.setText(str(self.printValue('B1')))
        self.lineEditB2.setText(str(self.printValue('B2')))
        self.lineEditB3.setText(str(self.printValue('B3')))
        self.lineEditB4.setText(str(self.printValue('B4')))
        self.lineEditB5.setText(str(self.printValue('B5')))
    
    def printValue(self, data):
        if data not in orders_data:
            orders_data[data] = 0
        return (orders_data[data])
    
    def comBox(self):
        mop = self.comboBoxMOP.currentText()
        if mop != "Cash":
            self.lineEditCash.setVisible(False)
            self.cash.setVisible(False)
            self.txtChange.setVisible(False)
            self.lblChange.setVisible(False)
        else:
            self.lineEditCash.setVisible(True)
            self.cash.setVisible(True)
            self.txtChange.setVisible(True)
            self.lblChange.setVisible(True)

    def save_print(self):
        name_len = len(self.lineEditName.text())
        cash_len = len(self.lineEditCash.text())
        mop = self.comboBoxMOP.currentText()
        amt = float(self.printValue('total'))

        if 'modeOfPayment' not in self.order.data:
            self.order.data['modeOfPayment'] = "none"
        self.order.data['modeOfPayment'] = mop

        if 'status' not in self.order.data:
            self.order.data['status'] = "none"
        self.order.data['status'] = "Pending"

        if mop == "Cash":
            if cash_len == 0:
                self.mssgBox.show_warning_message_box("Please enter cash.")
            else:
                cash = float(self.lineEditCash.text())
                if cash < amt:
                    self.mssgBox.show_warning_message_box("Insufficient cash.")
                    self.lineEditCash.setText('')
                else:
                    change = cash - amt
                    self.lblChange.setText("{:.2f}".format((change)))
                    if name_len == 0:
                        self.mssgBox.show_warning_message_box("Please enter name.")
                    else:       
                        cust_name = self.lineEditName.text()
                        currDate = QDate.currentDate().toString(Qt.ISODate)
                        currTime = str(self.lblTime.text())
                        if 'date' not in self.order.data:
                            self.order.data['date'] = "none"
                        self.order.data['date'] = currDate
                        if 'time' not in self.order.data:
                            self.order.data['time'] = "none"
                        self.order.data['time'] = currTime

                        if 'name' not in self.order.data:
                            self.order.data['name'] = "none"
                        self.order.data['name'] = cust_name
                        self.file.appendOrder()
                        self.print_receipt() 
                        self.mssgBox.show_info_message_box("Order has been successfully saved.") 
                        self.gotoMenu()
    
    def print_receipt(self):
        # Get order information
        order_code = self.printValue('orderCode')
        subtotal = self.printValue('subtotal')
        vat = self.printValue('vat')
        total = self.printValue('total')
        MoP = self.printValue('modeOfPayment')

        # Retrieve current date and time from class attributes
        currDate = self.lblDate.text()
        currTime = self.lblTime.text()

        # Retrieve customer name from lineEdit
        cust_name = self.lineEditName.text()
        
        # Generate receipt PDF
        filename = f"receipt_{order_code}.pdf"
        c = canvas.Canvas(filename)

        # Set font and size
        c.setFont("Helvetica", 12)

        # Write receipt header
        c.drawString(250, 750, "Order Receipt")
        c.drawString(50, 720, f"Order Code: {order_code}")
        c.drawString(50, 690, f"Date: {currDate}")
        c.drawString(50, 660, f"Time: {currTime}")
        c.drawString(50, 630, f"Customer Name: {cust_name}")

        # Write order details
        c.drawString(50, 600, "Order Details:")
        c.drawString(250, 170, f"{MoP}")
        c.drawString(250, 150, f"Subtotal: {subtotal}")
        c.drawString(250, 130, f"VAT:       {vat}")
        c.drawString(250, 110, f"Total:     {total}")

        # Write table data
        table_start_y = 580  # Starting y-coordinate for table data
        row_height = 20  # Height of each table row

        # Iterate over table rows
        for row in range(self.ordersTable.rowCount()):
            item_name = self.ordersTable.item(row, 0).text()
            quantity = self.ordersTable.item(row, 3).text()
            amount = self.ordersTable.item(row, 4).text()

            #Write item name, quantity, and amount
            c.drawString(100, table_start_y - row_height * row, f"{item_name}")
            c.drawString(200, table_start_y - row_height * row, f"Qty: {quantity}")
            c.drawString(300, table_start_y - row_height * row, f"Amount: {amount}")

        c.save()

        self.mssgBox.show_info_message_box("Receipt printed.")

    def gotoMenu(self):
        nxtForm = Menu()
        widget.addWidget(nxtForm)
        widget.setCurrentIndex(widget.currentIndex()+1)

#display all orders form
class DisplayAllOrders(QDialog):
    def __init__(self):
        super(DisplayAllOrders,self).__init__()
        self.widget=QtWidgets.QStackedWidget()
        loadUi("DisplayAllOrder.ui",self)
        self.order = Orders()
        self.file = FileHandling()
        self.mssgBox = MessageBox()
        self.allocateTable()
        self.orderList.itemSelectionChanged.connect(self.display_selected_order)
        self.pushbuttonUpdate.clicked.connect(self.updateStatus)
        self.pushbuttonDelete.clicked.connect(self.deleteOrder)
        self.pushbuttonMenu.clicked.connect(self.gotoMenu)
        self.search.textChanged.connect(self.perform_search)

    def allocateTable(self):
        self.file.RetrieveOrder()
        if not self.order.data:
            self.mssgBox.show_info_message_box("No orders found.")
        else:
            overallTotal = float(0)
            for orderNum, order_data in self.order.data.items():    
                item = QTreeWidgetItem()  # Create a new QTreeWidgetItem
                for column, (key, value) in enumerate(order_data.items()):
                    item.setTextAlignment(column, Qt.AlignCenter)
                    item.setText(column, str(value))  # Set the text for each column
                    if key == 'total':
                        value = float(value)
                        overallTotal += value
                self.orderList.addTopLevelItem(item)  # Add the item to the tree widget
            self.TAOlbl_2.setText("{:.2f}".format(overallTotal))
    
    def display_selected_order(self):
        selected_items = self.orderList.selectedItems()
        self.initialize_orderText()
        if len(selected_items) > 0:
            selected_item = selected_items[0]
            selected_order = [selected_item.text(column) for column in range(self.orderList.columnCount())]
            self.lblOrder.setText(str(selected_order[0]))
            self.lblName.setText(selected_order[1])
            self.lblDate.setText(selected_order[2])
            self.lblTime.setText(selected_order[3])
            self.lblSub.setText("{:.2f}".format(float(selected_order[4])))
            self.lblTotal.setText("{:.2f}".format(float(selected_order[5])))
            self.lblVat.setText("{:.2f}".format(float(selected_order[6])))
            self.lblMop.setText(selected_order[7])
            self.lineEditM1.setText(str(selected_order[8]))
            self.lineEditM2.setText(str(selected_order[9]))
            self.lineEditM3.setText(str(selected_order[10]))
            self.lineEditM4.setText(str(selected_order[11]))
            self.lineEditM5.setText(str(selected_order[12]))
            self.lineEditS1.setText(str(selected_order[13]))
            self.lineEditS2.setText(str(selected_order[14]))
            self.lineEditS3.setText(str(selected_order[15]))
            self.lineEditS4.setText(str(selected_order[16]))
            self.lineEditS5.setText(str(selected_order[17]))
            self.lineEditD1.setText(str(selected_order[18]))
            self.lineEditD2.setText(str(selected_order[19]))
            self.lineEditD3.setText(str(selected_order[20]))
            self.lineEditD4.setText(str(selected_order[21]))
            self.lineEditD5.setText(str(selected_order[22]))
            self.lineEditB1.setText(str(selected_order[23]))
            self.lineEditB2.setText(str(selected_order[24]))
            self.lineEditB3.setText(str(selected_order[25]))
            self.lineEditB4.setText(str(selected_order[26]))
            self.lineEditB5.setText(str(selected_order[27]))
            self.lblStatus.setText(selected_order[28])

    def initialize_orderText(self):
        self.lblOrder.setText('')
        self.lblName.setText('')
        self.lblDate.setText('')
        self.lblTime.setText('')
        self.lblSub.setText('')
        self.lblTotal.setText('')
        self.lblVat.setText('')
        self.lblMop.setText('')
        self.lblStatus.setText('')
        self.lineEditM1.setText('')
        self.lineEditM2.setText('')
        self.lineEditM3.setText('')
        self.lineEditM4.setText('')
        self.lineEditM5.setText('')
        self.lineEditS1.setText('')
        self.lineEditS2.setText('')
        self.lineEditS3.setText('')
        self.lineEditS4.setText('')
        self.lineEditS5.setText('')
        self.lineEditD1.setText('')
        self.lineEditD2.setText('')
        self.lineEditD3.setText('')
        self.lineEditD4.setText('')
        self.lineEditD5.setText('')
        self.lineEditB1.setText('')
        self.lineEditB2.setText('')
        self.lineEditB3.setText('')
        self.lineEditB4.setText('')
        self.lineEditB5.setText('')

    def updateStatus(self):
        selected_items = self.orderList.selectedItems()
        if len(selected_items) > 0:
            selected_item = selected_items[0]
            orderNum = self.orderList.indexOfTopLevelItem(selected_item) + 1
            if orderNum in self.order.data:
                if self.order.data[orderNum]['status'] == 'Pending':
                    self.order.data[orderNum]['status'] = 'Complete'
                    selected_item.setText(28, 'Complete')
                    self.lblStatus.setText("Complete")
                else:
                    self.order.data[orderNum]['status'] = 'Pending'
                    selected_item.setText(28, 'Pending')
                    self.lblStatus.setText("Pending")
            self.file.saveOrder()
            self.mssgBox.show_info_message_box("Status updated.")
        else:
            self.mssgBox.show_warning_message_box("Please select an order.")
    
    def deleteOrder(self):
        selected_items = self.orderList.selectedItems()
        if len(selected_items) > 0:
            selected_item = selected_items[0]
            orderNum = self.orderList.indexOfTopLevelItem(selected_item) + 1
            row_index = self.orderList.indexOfTopLevelItem(selected_item)
            reply = self.mssgBox.show_question_message_box("Are you sure to delete this order?")
            if reply:
                # Delete the selected item from the QTreeWidget
                self.orderList.takeTopLevelItem(row_index)
                if orderNum in self.order.data:
                    del self.order.data[orderNum]
                    self.file.saveOrder()
        else:
            self.mssgBox.show_warning_message_box("Please select an order.")
    
    def perform_search(self):
        self.initialize_orderText()
        text = self.search.text().lower().strip()

        if not text:
            self.orderList.clear()
            self.allocateTable()
            return
        
        for i in range(self.orderList.topLevelItemCount()):
            item = self.orderList.topLevelItem(i)
            item.setHidden(True)

            for column in range(item.columnCount()):
                if text in item.text(column).lower():
                    item.setHidden(False)
                    break

    def gotoMenu(self):
        nxtForm = Menu()
        widget.addWidget(nxtForm)
        widget.setCurrentIndex(widget.currentIndex()+1)

#admin form
class Admin(QDialog):
    def __init__(self):
        super(Admin,self).__init__()
        loadUi("Admin.ui",self)
        self.mssgbox = MessageBox()
        self.file = FileHandling()
        self.order = Orders()
        self.bttnLogin.clicked.connect(self.inputPassword)
        self.bttnBack.clicked.connect(self.gotoMenu)
    
    def inputPassword(self):
        if len(self.Password.text()) == 0:
            self.mssgbox.show_warning_message_box("Please enter a password.")
        else:
            inputPass = self.Password.text()
            if inputPass == 'admin ako': #correct password
                self.mssgbox.show_info_message_box("Correct password!")
                self.adminWidget.setCurrentWidget(self.pageDate)
                selected_defDate = self.dateChooser.selectedDate().toString(Qt.DefaultLocaleLongDate)
                self.date.setText(selected_defDate)
                self.dateChooser.selectionChanged.connect(self.selectDate)
                self.bttnContinue.clicked.connect(self.gotoDailySales)
            else:
                self.mssgbox.show_warning_message_box("Incorrect Password!")
                self.Password.setText('')

    def selectDate(self):
        selected_defDate = self.dateChooser.selectedDate().toString(Qt.DefaultLocaleLongDate)
        self.date.setText(selected_defDate)
    
    def gotoDailySales(self):
        self.file.RetrieveOrder()
        selected_ISOdate = self.dateChooser.selectedDate().toString(Qt.ISODate)
        selected_defDate = self.dateChooser.selectedDate().toString(Qt.DefaultLocaleLongDate)
        self.order.searchOrdersByDate(selected_ISOdate)
        if len(orders_data) > 0:
            nxtForm = DailySales(selected_defDate)
            widget.addWidget(nxtForm)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            self.mssgbox.show_warning_message_box("No orders found.")

    def gotoMenu(self):
        nxtForm = Menu()
        widget.addWidget(nxtForm)
        widget.setCurrentIndex(widget.currentIndex()+1)
       
#daily sales report form
class DailySales(QDialog):
    def __init__(self, date):
        super(DailySales,self).__init__()
        loadUi("DailySales.ui",self)
        self.daily_sales = {}
        self.food = foodDesc()
        self.msssgbox = MessageBox()
        self.lblDate.setText(date)
        self.gettingDailySales()
        self.bestSeller_main()
        self.bestSeller_side()
        self.bestSeller_dessert()
        self.bestSeller_bev()
        self.pushButtonMenu.clicked.connect(self.gotoMenu)
        self.orderCBox.activated.connect(self.gettingDailySales)
        self.pushButtonPrint.clicked.connect(self.print_to_pdf)
    
    def gettingDailySales(self):
        M1_total = 0; M2_total = 0; M3_total = 0; M4_total = 0; M5_total = 0
        S1_total = 0; S2_total = 0; S3_total = 0; S4_total = 0; S5_total = 0
        D1_total = 0; D2_total = 0; D3_total = 0; D4_total = 0; D5_total = 0
        B1_total = 0; B2_total = 0; B3_total = 0; B4_total = 0; B5_total = 0
        subTotal = 0; vat = 0; totalAmt = 0
        for order_num, order_data in orders_data.items():
            M1_total += int(order_data['M1'])
            M2_total += int(order_data['M2'])
            M3_total += int(order_data['M3'])
            M4_total += int(order_data['M4'])
            M5_total += int(order_data['M5'])

            S1_total += int(order_data['S1'])
            S2_total += int(order_data['S2'])
            S3_total += int(order_data['S3'])
            S4_total += int(order_data['S4'])
            S5_total += int(order_data['S5'])

            D1_total += int(order_data['D1'])
            D2_total += int(order_data['D2'])
            D3_total += int(order_data['D3'])
            D4_total += int(order_data['D4'])
            D5_total += int(order_data['D5'])

            B1_total += int(order_data['B1'])
            B2_total += int(order_data['B2'])
            B3_total += int(order_data['B3'])
            B4_total += int(order_data['B4'])
            B5_total += int(order_data['B5'])
            subTotal += float(order_data['subtotal'])
            vat += float(order_data['vat'])
            totalAmt += float(order_data['total'])

        self.daily_sales[1] = {
            'M1': M1_total, 'M2': M2_total, 'M3': M3_total, 'M4': M4_total, 'M5': M5_total,
            'S1': S1_total, 'S2': S2_total, 'S3': S3_total, 'S4': S4_total, 'S5': S5_total,
            'D1': D1_total, 'D2': D2_total, 'D3': D3_total, 'D4': D4_total, 'D5': D5_total,
            'B1': B1_total, 'B2': B2_total, 'B3': B3_total, 'B4': B4_total, 'B5': B5_total
        }
        
        self.salesTotal.setText("{:.2f}".format(totalAmt))
        self.salesAmt.setText("{:.2f}".format(subTotal))
        self.salesTax.setText("{:.2f}".format(vat))
        
        mop = self.orderCBox.currentText()
        if mop == 'Greatest to least number of sales':
            self.daily_sales = {k: dict(sorted(v.items(), key=lambda item: item[1], reverse=True)) for k, v in self.daily_sales.items()}
        else:
            self.daily_sales = {k: dict(sorted(v.items(), key=lambda item: item[1])) for k, v in self.daily_sales.items()} 
        
        self.allocateDSTable()

    def allocateDSTable(self):
        self.dailySales.clear()
        category_mapping = {
            'M1': {'name': self.food.M1_name, 'prc': "{:.2f}".format(self.food.M1_prc), 'category': 'Main Dish'
            },'M2': {'name': self.food.M2_name, 'prc': "{:.2f}".format(self.food.M2_prc), 'category': 'Main Dish'
            },'M3': {'name': self.food.M3_name, 'prc': "{:.2f}".format(self.food.M3_prc), 'category': 'Main Dish'
            },'M4': {'name': self.food.M4_name, 'prc': "{:.2f}".format(self.food.M5_prc), 'category': 'Main Dish'
            },'M5': {'name': self.food.M5_name, 'prc': "{:.2f}".format(self.food.M5_prc), 'category': 'Main Dish'
            },
            'S1': {'name': self.food.S1_name, 'prc': "{:.2f}".format(self.food.S1_prc), 'category': 'Side Dish'
            },'S2': {'name': self.food.S2_name,'prc': "{:.2f}".format(self.food.S2_prc),'category': 'Side Dish'
            },'S3': {'name': self.food.S3_name,'prc': "{:.2f}".format(self.food.S3_prc),'category': 'Side Dish'
            },'S4': {'name': self.food.S4_name,'prc': "{:.2f}".format(self.food.S4_prc),'category': 'Side Dish'
            },'S5': {'name': self.food.S5_name,'prc': "{:.2f}".format(self.food.S5_prc),'category': 'Side Dish'
            },
            'D1': {'name': self.food.D1_name,'prc': "{:.2f}".format(self.food.D1_prc),'category': 'Dessert'
            },'D2': {'name': self.food.D2_name,'prc': "{:.2f}".format(self.food.D2_prc),'category': 'Dessert'
            },'D3': {'name': self.food.D3_name,'prc': "{:.2f}".format(self.food.D3_prc),'category': 'Dessert'
            },'D4': {'name': self.food.D4_name,'prc': "{:.2f}".format(self.food.D4_prc),'category': 'Dessert'
            },'D5': {'name': self.food.D5_name,'prc': "{:.2f}".format(self.food.D5_prc),'category': 'Dessert'
            },
            'B1': {'name': self.food.B1_name,'prc': "{:.2f}".format(self.food.B1_prc),'category': 'Beverage'
            },'B2': {'name': self.food.B2_name,'prc': "{:.2f}".format(self.food.B2_prc),'category': 'Beverage'
            },'B3': {'name': self.food.B3_name,'prc': "{:.2f}".format(self.food.B3_prc),'category': 'Beverage'
            },'B4': {'name': self.food.B4_name,'prc': "{:.2f}".format(self.food.B4_prc),'category': 'Beverage'
            },'B5': {'name': self.food.B5_name,'prc': "{:.2f}".format(self.food.B5_prc),'category': 'Beverage'
            }
        }

        for column in range(7): 
            self.dailySales.setColumnWidth(column, 153)  # Set the width of each column
        
        for category, value in self.daily_sales[1].items():
            item = QTreeWidgetItem()
            salesAmt = float(self.salesAmt.text())

            for column in range(7): 
                item.setTextAlignment(column, Qt.AlignCenter)

            if category in category_mapping:
                amt = self.getTotal(value, category_mapping[category]['prc'])
                percentage = self.getPerc(float(amt), float(salesAmt))
                item.setText(0, category)
                item.setText(1, category_mapping[category]['name'])
                item.setText(2, category_mapping[category]['category'])
                item.setText(3, str(category_mapping[category]['prc']))
                item.setText(4, str(value))
                item.setText(5, amt)
                item.setText(6, percentage)

            self.dailySales.addTopLevelItem(item)
    
    def bestSeller_main(self):
        salesAmt = float(self.salesAmt.text())
        order = self.daily_sales[1]
        main = [order['M1'], order['M2'], order['M3'], order['M4'], order['M5']]
        bestMain = max(main)
        if order['M1'] == bestMain:
            pixmap = QPixmap('food_pics/pan fried salmon.png')
            self.lblMain.setText(self.food.M1_name)
            self.main_qtty.setText(str(order['M1']))
            amt = self.getTotal(order['M1'], self.food.M1_prc)
        elif order['M2'] == bestMain:
            pixmap = QPixmap('food_pics/crissy baked chicken.png')
            self.lblMain.setText(self.food.M2_name)
            self.main_qtty.setText(str(order['M2']))
            amt = self.getTotal(order['M2'], self.food.M2_prc)
        elif order['M3'] == bestMain:
            pixmap = QPixmap('food_pics/teriyaki chicken bowl.png')
            self.lblMain.setText(self.food.M3_name)
            self.main_qtty.setText(str(order['M3']))
            amt = self.getTotal(self.daily_sales['M3'], self.food.M3_prc)
        elif order['M4'] == bestMain:
            pixmap = QPixmap('food_pics/golden shrimp.png')
            self.lblMain.setText(self.food.M4_name)
            self.main_qtty.setText(str(order['M4']))
            amt = self.getTotal(order['M4'], self.food.M4_prc)
        elif order['M5'] == bestMain:
            pixmap = QPixmap('food_pics/stuffed chicken breast.png')
            self.lblMain.setText(self.food.M5_name)
            self.main_qtty.setText(str(order['M5']))
            amt = self.getTotal(order['M5'], self.food.M5_prc)
            
        self.main_sp.setText(self.getPerc(amt, salesAmt))
        self.pic_main.setPixmap(pixmap)

    def bestSeller_side(self):
        salesAmt = float(self.salesAmt.text())
        order = self.daily_sales[1]
        sides = [order['S1'], order['S2'], order['S3'], order['S4'], order['S5']]
        bestSide = max(sides)
        if order['S1'] == bestSide:
            pixmap = QPixmap('food_pics/French fries with aoili.png')
            self.lblSide.setText(self.food.S1_name)
            self.side_qtty.setText(str(order['S1']))
            amt = self.getTotal(order['S1'], self.food.S1_prc)
        elif order['S2'] == bestSide:
            pixmap = QPixmap('food_pics/Sautee Collard Greens.png')
            self.lblSide.setText(self.food.S2_name)
            self.side_qtty.setText(str(order['S2']))
            amt = self.getTotal(order['S2'], self.food.S2_prc)
        elif order['S3'] == bestSide:
            pixmap = QPixmap('food_pics/Chipotle Mashed Potatoes.png')
            self.pic_main.setPixmap(pixmap)
            self.side_qtty.setText(str(order['S3']))
            amt = self.getTotal(order['S3'], self.food.S3_prc)
        elif order['S4'] == bestSide:
            pixmap = QPixmap('food_pics/Pesto Pasta Salad.png')
            self.lblSide.setText(self.food.S4_name)
            self.side_qtty.setText(str(order['S4']))
            amt = self.getTotal(order['S4'], self.food.S4_prc)
        elif order['S5'] == bestSide:
            pixmap = QPixmap('food_pics/Steamed rice.png')
            self.lblSide.setText(self.food.S5_name)
            self.side_qtty.setText(str(order['S5']))
            amt = self.getTotal(order['S5'], self.food.S5_prc)
            
        self.side_sp.setText(self.getPerc(amt, salesAmt))
        self.pic_side.setPixmap(pixmap)
    
    def bestSeller_dessert(self):
        salesAmt = float(self.salesAmt.text())
        order = self.daily_sales[1]
        desserts = [order['D1'], order['D2'], order['D3'], order['D4'], order['D5']]
        bestDessert = max(desserts)
        if order['D1'] == bestDessert:
            pixmap = QPixmap('food_pics/tiramisu.png')
            self.lblDessert.setText(self.food.D1_name)
            self.dessert_qtty.setText(str(order['D1']))
            amt = self.getTotal(order['D1'], self.food.D1_prc)
        elif order['D2'] == bestDessert:
            pixmap = QPixmap('food_pics/cheesecake w berries.png')
            self.lblDessert.setText(self.food.D2_name)
            self.dessert_qtty.setText(str(order['D2']))
            amt = self.getTotal(order['D2'], self.food.D2_prc)
        elif order['D3'] == bestDessert:
            pixmap = QPixmap('food_pics/Creme caramel.png')
            self.lblDessert.setText(self.food.D3_name)
            self.dessert_qtty.setText(str(order['D3']))
            amt = self.getTotal(order['D3'], self.food.D3_prc)
        elif order['D4'] == bestDessert:
            pixmap = QPixmap('food_pics/Blackberry pie.png')
            self.lblDessert.setText(self.food.D4_name)
            self.dessert_qtty.setText(str(order['D4']))
            amt = self.getTotal(order['D4'], self.food.D4_prc)
        elif order['D5'] == bestDessert:
            pixmap = QPixmap('food_pics/Red Velvet cake.png')
            self.lblDessert.setText(self.food.D5_name)
            self.dessert_qtty.setText(str(order['D5']))
            amt = self.getTotal(order['D5'], self.food.D5_prc)
        
        self.dessert_sp.setText(self.getPerc(amt, salesAmt))
        self.pic_des.setPixmap(pixmap)
    
    def bestSeller_bev(self):
        salesAmt = float(self.salesAmt.text())
        order = self.daily_sales[1]
        bev = [order['B1'], order['B2'], order['B3'], order['B4'], order['B5']]
        bestBev = max(bev)
        if order['B1'] == bestBev:
            pixmap = QPixmap('food_pics/soda water.png')
            self.lblBeverage.setText(self.food.B1_name)
            self.bev_qtty.setText(str(order['B1']))
            amt = self.getTotal(order['B1'], self.food.B1_prc)
        elif order['B2'] == bestBev:
            pixmap = QPixmap('food_pics/bottled water.png')
            self.lblBeverage.setText(self.food.B2_name)
            self.bev_qtty.setText(str(order['B2']))
            amt = self.getTotal(order['B2'], self.food.B2_prc)
        elif order['B3'] == bestBev:
            pixmap = QPixmap('food_pics/orange juice.png')
            self.lblBeverage.setText(self.food.B3_name)
            self.bev_qtty.setText(str(order['B3']))
            amt = self.getTotal(order['B3'], self.food.B3_prc)
        elif order['B4'] == bestBev:
            pixmap = QPixmap('food_pics/milkshake.png')
            self.lblBeverage.setText(self.food.B4_name)
            self.bev_qtty.setText(str(order['B4']))
            amt = self.getTotal(order['B4'], self.food.B4_prc)
        elif order['B5'] == bestBev:
            pixmap = QPixmap('food_pics/iced tea.png')
            self.lblBeverage.setText(self.food.B5_name)
            self.bev_qtty.setText(str(order['B5']))
            amt = self.getTotal(order['B5'], self.food.B5_prc)
        
        self.bev_sp.setText(self.getPerc(amt, salesAmt))
        self.pic_bev.setPixmap(pixmap)
    
    def getTotal(self, qtty, price):
        totalAmt = float(price) * float(qtty)
        return ("{:.2f}".format(totalAmt))
    
    def getPerc(self, total, salesAmt):
        if total == 0 or salesAmt == 0:
            return "0%"
        else:
            sp = (float(total) / float(salesAmt)) * 100
            return "{:.2f}%".format(sp)
        
    def comBox(self):
        mop = self.orderCBox.currentText()
        self.dailySales.clear()
        if mop == "Greatest to least sales":
            self.daily_sales[1] = {k: dict(sorted(v.items(), key=lambda item: item[1], reverse=True)) for k, v in self.daily_sales.items()}
            self.allocateDSTable
        else:
            self.daily_sales[1] = {k: dict(sorted(v.items(), key=lambda item: item[1])) for k, v in self.daily_sales.items()} 
            self.allocateDSTable()

    def print_to_pdf(self):
        file_name = ("Daily Sales Report (" + self.lblDate.text() + ").pdf")

        dpi = self.logicalDpiX()
        page_size = QPageSize(self.size())

        printer = QPdfWriter(file_name)
        printer.setResolution(dpi)
        printer.setPageSize(page_size)

        painter = QPainter(printer)
        self.render(painter)
        painter.end()

        self.msssgbox.show_info_message_box("PDF file successfully created.")

    def gotoMenu(self):
        nxtForm = Menu()
        widget.addWidget(nxtForm)
        widget.setCurrentIndex(widget.currentIndex()+1)

app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
MainWindow=Menu()
widget=QtWidgets.QStackedWidget()
widget.addWidget(MainWindow)
widget.setFixedWidth(1170)
widget.setFixedHeight(750)
widget.show()
app.exec_()
