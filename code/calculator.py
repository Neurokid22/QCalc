from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizeGrip, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from ui_calculator import Ui_MainWindow


class CalculatorWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    # Init Class Variables
    firstNum = None
    userIsTypingSecondNum = False

    # --------- Class Initialisation ------------

    def __init__(self):

        # --------------Init Window -----------------

        super().__init__()
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.setWindowOpacity(0.95)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)        
        self.show()

        # -------------- End ------------------------   
        
            
        # -------------- Setting Functions To Window Buttons -----
        self.MaximizeWin.clicked.connect(self.maximize)
        self.MinimizeWin.clicked.connect(self.minimize)
        self.ExitWin.clicked.connect(QtWidgets.qApp.quit)
        self.MaximizeWin.setCheckable(True)
        self.oldPos = self.pos()
        # ------------------------- End --------------------------



        # -------------- List Of Buttons ------------
        keyPadBtns = [  self.key_0,
                        self.key_1, 
                        self.key_2,
                        self.key_3,
                        self.key_4,
                        self.key_5,
                        self.key_6,
                        self.key_7,
                        self.key_8, 
                        self.key_9,
                        self.key_decimal                   
        ]
        global operators
        operators = [
                        self.key_add,
                        self.key_subtract,
                        self.key_mulitpy,
                        self.key_divide,
                        self.key_equals
        ]
        
        special_operators = [
            self.key_percentage,
            self.key_negativeToggle,
            self.key_clear
        ]
        # -------------- End -------------------------
        

        # -------------- Button connections --------------- 
        for btn in (keyPadBtns):
            if btn == self.key_decimal:
                btn.clicked.connect(self.decimal_pressed)
            else:
                btn.clicked.connect(self.button_pressed)
                 
        for btn in special_operators:
            if btn == self.key_clear:
                btn.clicked.connect(self.clear_btn)
            else:
                btn.clicked.connect(self.unary_operations)

        for btn in operators:
            if btn != self.key_equals:
                btn.clicked.connect(self.binary_operation)
                btn.setCheckable(True)
            else:
                btn.clicked.connect(self.equals_operation)
        # ------------------- End -------------------------

    # ---------------- End ----------------------


    # --------------- Button Functions ----------
    def button_pressed(self): 
        buttons = self.sender()
    
        if ((self.key_add.isChecked() or self.key_divide.isChecked() or self.key_mulitpy.isChecked() or self.key_subtract.isChecked()) and (not self.userIsTypingSecondNum)):
            screen = format(float(buttons.text()), '.15g')
            self.userIsTypingSecondNum = True
        else:
            if (('.' in self.Screen.text()) and (buttons.text() == '0')):

                screen = format(self.Screen.text() + buttons.text(), '.15')
            else:
                screen = format(float(self.Screen.text() + buttons.text()), '.15g')

        self.Screen.setText(screen)

    def decimal_pressed(self):
        if '.' not in self.Screen.text():
            self.Screen.setText(self.Screen.text() + '.')
           
    def unary_operations(self):
        button = self.sender()
        number = float(self.Screen.text())
        if button.text() == '+/-':  
            calc = number * -1
           
        else:
            calc = number * 0.01

        self.Screen.setText(format(calc, '.15g'))  
            
    def binary_operation(self):
        button = self.sender()

        self.firstNum = float(self.Screen.text())

        button.setChecked(True)
        
    def equals_operation(self):
        self.operation_calc()
        self.userIsTypingSecondNum = False
        
    def clear_btn(self):
        self.key_add.setChecked(False)
        self.key_subtract.setChecked(False)
        self.key_divide.setChecked(False)
        self.key_mulitpy.setChecked(False)
       
        self.userIsTypingSecondNum = False
    
        self.Screen.setText('0')
    # ------------------- End -------------------


    # --------- Window Button Functions ---------
    def maximize(self):
        if (self.MaximizeWin.isChecked()):
            self.showMaximized()
            self.Container.setStyleSheet("QFrame { \n"
                    "background-color: rgb(113, 219, 182);\n"
                    "border-radius: 0px;\n"
                "}")

        else:
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            # resets original border
            self.Container.setStyleSheet("QFrame { \n"
                    "background-color: rgb(113, 219, 182);\n"
                    "border-radius: 15px;\n"
                "}") 
        
    def minimize(self):
        self.showMinimized()
    # ------------------ End --------------------


    # ------------------- Mouse Function For Moving Calculator ---------------
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    # ----------------------------------- End -------------------------------- 

    # ----------- Function handles calculation ----------------
    def operation_calc(self):

        second_number = float(self.Screen.text())

        if self.key_add.isChecked():
            labelNum = self.firstNum + second_number
            newLabel = format(labelNum, '.15g')
            self.Screen.setText(newLabel)
            self.key_add.setChecked(False)
            
        elif self.key_mulitpy.isChecked():
            labelNum = self.firstNum * second_number
            newLabel = format(labelNum, '.15g')
            self.Screen.setText(newLabel)
            self.key_mulitpy.setChecked(False)

        elif self.key_subtract.isChecked():
            labelNum = self.firstNum - second_number
            newLabel = format(labelNum, '.15g')
            self.Screen.setText(newLabel)
            self.key_subtract.setChecked(False)

        elif self.key_divide.isChecked():
            labelNum = self.firstNum / second_number
            newLabel = format(labelNum, '.15g')
            self.Screen.setText(newLabel)
            self.key_divide.setChecked(False)
   # ----------------------- End ------------------------------



if __name__ == "__main__":
    CalculatorWindow()