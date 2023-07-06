import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QLabel, QAbstractItemView, QMessageBox, QTreeWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDate, QTimer, QTimer, QTime, Qt
from PyQt5.uic import loadUi
import random, codecs

orders_data = {}

class Orders:
    def __init__(self):
        self.data = orders_data
    
    def orderInfo(self, orderNum, orderCode, name, date, time, subtotal, total, vat, modeOfPayment, M1, M2, M3, M4, M5, S1, S2, S3, S4, S5, D1, D2, D3, D4, D5, B1, B2, B3, B4, B5, status):
        self.data[orderNum] = {
            'orderCode' : orderCode, 'name' : name, 'date' : date, 'time' : time, 'total' : total, 
            'subtotal' : subtotal, 'vat' : vat, 'modeOfPayment' : modeOfPayment,
            'M1' : M1, 'M2' : M2, 'M3' : M3, 'M4': M4, 'M5': M5,
            'S1' : S1, 'S2' : S2, 'S3' : S3, 'S4': S4, 'S5': S5,
            'D1' : D1, 'D2' : D2, 'D3' : D3, 'D4': D4, 'D5': D5,
            'B1' : B1, 'B2' : B2, 'B3' : B3, 'B4': B4, 'B5': B5,
            'status' : status
        }

class OrderManager:
    def __init__(self):
        self.order = Orders()

    def add_order(self, orderNum, orderCode, name, date, time, subtotal, total, vat, modeOfPayment, M1, M2, M3, M4, M5, S1, S2, S3, S4, S5, D1, D2, D3, D4, D5, B1, B2, B3, B4, B5, status):
        self.order.orderInfo(orderNum, orderCode, name, date, time, subtotal, total, vat, modeOfPayment, M1, M2, M3, M4, M5, S1, S2, S3, S4, S5, D1, D2, D3, D4, D5, B1, B2, B3, B4, B5, status)

class foodDesc:
    def __init__(self):
        self.M1_prc = 220.00; self.M2_prc = 160.00; self.M3_prc = 180.00; self.M4_prc = 200.00; self.M5_prc = 190.00
        self.S1_prc = 80.00; self.S2_prc = 60.00; self.S3_prc = 75.00; self.S4_prc = 90.00; self.S5_prc = 35.00
        self.D1_prc = 100.00; self.D2_prc = 90.00; self.D3_prc = 80.00; self.D4_prc = 85.00; self.D5_prc = 90.00
        self.B1_prc = 30.00; self.B2_prc = 20.00; self.B3_prc = 55.00; self.B4_prc = 80.00; self.B5_prc = 40.00

        self.M1_name = "Pan Fried Salmon"; self.M2_name = "Crispy Baked Chicken"; self.M3_name = "Teriyaki Chicken Bowl"; self.M4_name = "Golden Shrimp"; self.M5_name = "Stuffed Chicken Breast"
        self.S1_name = "French Fries with Aioli"; self.S2_name = "Collard Greens"; self.S3_name = "Chipotle Mashed Potatoes"; self.S4_name = "Pesto Pasta Salad"; self.S5_name = "Steamed Rice"
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
            self.set_table_item(row_index, 2, price)
            self.set_table_item(row_index, 3, quantity)
            self.set_table_item(row_index, 4, amount)

            self.table.setRowHeight(row_index, 50)
            
    def set_table_item(self, row, column, value):
        if column == 1:
            image_label = QLabel()
            pixmap = QPixmap(value)
            image_label.setPixmap(pixmap)
            image_label.setScaledContents(True)
            self.table.setCellWidget(row, column, image_label)
        else:
            item = QTableWidgetItem(str(value))
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

        button_yes = msg_box.button(QMessageBox.Yes)
        button_no = msg_box.button(QMessageBox.No)
        
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
        self.addOrder = OrderManager()
        self.order = Orders()
        orderNum = 1
        try:
            with codecs.open(file_name, 'r', encoding='utf-8') as file:
                for line in file:
                    decrypted_data = self.decrypt(line.strip(), 20)
                    if decrypted_data:
                        data = decrypted_data.split(',')
                        self.addOrder.add_order(orderNum,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],data[17],data[18],data[19],data[20],data[21],data[22],data[23],data[24],data[25],data[26],data[27],data[28])
                        #print(data)
                        orderNum += 1
                    
        except IOError as ex:
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

    def gotoAddOrder(self):
        nxtForm = AddOrder()
        widget.addWidget(nxtForm)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoDisplayOrders(self):
        nxtForm = DisplayAllOrders()
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
        self.qtty_main1.setText('0')
    def add_m2(self):
        m2 = self.qtty_main2.toPlainText()
        self.check(m2, 'M2', self.food.M2_prc, 'food_pics/crissy baked chicken.PNG')
        self.qtty_main2.setText('0')
    def add_m3(self):
        m3 = self.qtty_main3.toPlainText()
        self.check(m3, 'M3', self.food.M3_prc, 'food_pics/teriyaki chicken bowl.PNG')
        self.qtty_main3.setText('0')
    def add_m4(self):
        m4 = self.qtty_main4.toPlainText()
        self.check(m4, 'M4', self.food.M4_prc, 'food_pics/golden shrimp.PNG')
        self.qtty_main4.setText('0')
    def add_m5(self):
        m5 = self.qtty_main5.toPlainText()
        self.check(m5, 'M5', self.food.M5_prc, 'food_pics/stuffed chicken breast.PNG')
        self.qtty_main4.setText('0')
    
    #add functions for side dishes
    def add_s1(self):
        s1 = self.qtty_side1.toPlainText()
        self.check(s1, 'S1', self.food.S1_prc, 'food_pics/French fries with aoili.PNG')
        self.qtty_side1.setText('0')
    def add_s2(self):
        s2 = self.qtty_side2.toPlainText()
        self.check(s2, 'S2', self.food.S2_prc, 'food_pics/Sautee Collard Greens.PNG')
        self.qtty_side2.setText('0')
    def add_s3(self):
        s3 = self.qtty_side3.toPlainText()
        self.check(s3, 'S3', self.food.S3_prc, 'food_pics/Chipotle Mashed Potatoes.PNG')
        self.qtty_side3.setText('0') 
    def add_s4(self):
        s4 = self.qtty_side4.toPlainText()
        self.check(s4, 'S4', self.food.S4_prc, 'food_pics/Pesto Pasta Salad.PNG')
        self.qtty_side4.setText('0') 
    def add_s5(self):
        s5 = self.qtty_side5.toPlainText()
        self.check(s5, 'S5', self.food.S5_prc, 'food_pics/Steamed rice.PNG')
        self.qtty_side5.setText('0') 

    #add fucntions for desserts
    def add_d1(self):
        d1 = self.qtty_dessert1.toPlainText()
        self.check(d1, 'D1', self.food.D1_prc, 'food_pics/tiramisu.PNG')
        self.qtty_dessert1.setText('0')
    def add_d2(self):
        d2 = self.qtty_dessert2.toPlainText()
        self.check(d2, 'D2', self.food.D2_prc, 'food_pics/cheesecake w berries.PNG')
        self.qtty_dessert2.setText('0')
    def add_d3(self):
        d3 = self.qtty_dessert3.toPlainText()
        self.check(d3, 'D3', self.food.D3_prc, 'food_pics/Creme caramel.PNG')
        self.qtty_dessert3.setText('0') 
    def add_d4(self):
        d4 = self.qtty_dessert4.toPlainText()
        self.check(d4, 'D4', self.food.D4_prc, 'food_pics/Blackberry pie.PNG')
        self.qtty_dessert4.setText('0') 
    def add_d5(self):
        d5 = self.qtty_dessert5.toPlainText()
        self.check(d5, 'D5', self.food.D5_prc, 'food_pics/Red Velvet cake.PNG')
        self.qtty_dessert5.setText('0')          
    
    #add functions fot beverages
    def add_b1(self):
        b1 = self.qtty_bev1.toPlainText()
        self.check(b1, 'B1', self.food.B1_prc, 'food_pics/soda water.PNG')
        self.qtty_bev1.setText('0')
    def add_b2(self):
        b2 = self.qtty_bev2.toPlainText()
        self.check(b2, 'B2', self.food.B1_prc, 'food_pics/bottled water.PNG')
        self.qtty_bev2.setText('0')
    def add_b3(self):
        b3 = self.qtty_bev3.toPlainText()
        self.check(b3, 'B3', self.food.B3_prc, 'food_pics/orange juice.PNG')
        self.qtty_bev3.setText('0')
    def add_b4(self):
        b4 = self.qtty_bev4.toPlainText()
        self.check(b4, 'B4', self.food.B4_prc, 'food_pics/milkshake.PNG')
        self.qtty_bev4.setText('0')
    def add_b5(self):
        b5 = self.qtty_bev5.toPlainText()
        self.check(b5, 'B5', self.food.B5_prc, 'food_pics/iced tea.PNG')
        self.qtty_bev5.setText('0')
    
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
        self.total_lbl.setText(str(self.order.data['subtotal']))
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
            widget.addWidget(nxtForm)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            self.show_warning_message_box("Please enter an order first.")
        
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
        "{:.2f}".format
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
            self.mssgBox.show_info_message_box("Order has been successfully saved.") 
            self.gotoMenu()
            
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

    def allocateTable(self):
        self.file.RetrieveOrder()
        if not self.order.data:
            self.mssgBox.show_info_message_box("No orders found.")
        else:
            overallTotal = float(0)
            for orderNum, order_data in self.order.data.items():    
                item = QTreeWidgetItem()  # Create a new QTreeWidgetItem
                for column, (key, value) in enumerate(order_data.items()):
                    item.setText(column, str(value))  # Set the text for each column
                    if key == 'total':
                        value = float(value)
                        overallTotal += value
                self.orderList.addTopLevelItem(item)  # Add the item to the tree widget
            self.TAOlbl_2.setText("{:.2f}".format(overallTotal))
    
    def display_selected_order(self):
        #"{:.2f}".format
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
