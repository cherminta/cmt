from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import * 
from functools import partial

class MyCal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Calculator")
        self.setFixedSize(360, 480)
        #mainlayout
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        #set central widget
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.mainLayout)
        #display and button
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        # display (number)
        self.display = QLineEdit()
        self.display.setStyleSheet('background-color : #EAEAEA')
        self.display.setFixedHeight(80)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)

        self.mainLayout.addWidget(self.display)
        
    def _createButtons(self):
        self.button = {}
        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()
        self.layout4 = QHBoxLayout()
        self.layout5 = QHBoxLayout()
        button = {'1', '2', '3', '/',
                  '4', '5', '6', '*',
                  '7', '8', '9', '-',
                  '=', '0', '.', '+',
                  'AC','C', '%'}
        for btn in button:
            self.button[btn] = QPushButton(btn)
            self.button[btn].setFixedHeight(60)
            if btn != '0':
                self.button[btn].setFixedWidth(80)
            else:
                self.button[btn].setFixedWidth(160)
            self.button[btn].setFont(QFont('Arial', 27))
        # set buttons' colour
        num = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.'}
        oper = {'+', '-', '*', '/', '='}
        func = {'AC', 'C', '%'}
        for i in num:
            self.button[i].setStyleSheet("background-color : #C3DFD8")
        for i in oper:
            self.button[i].setStyleSheet("background-color : #B5D6D6")
        for i in func:
            self.button[i].setStyleSheet("background-color : #C4DBC1")
        
        self.layout1.addWidget(self.button['AC'])
        self.layout1.addWidget(self.button['C'])
        self.layout1.addWidget(self.button['%'])
        self.layout1.addWidget(self.button['/'])
        self.layout2.addWidget(self.button['7'])
        self.layout2.addWidget(self.button['8'])
        self.layout2.addWidget(self.button['9'])
        self.layout2.addWidget(self.button['*'])
        self.layout3.addWidget(self.button['4'])
        self.layout3.addWidget(self.button['5'])
        self.layout3.addWidget(self.button['6'])
        self.layout3.addWidget(self.button['-'])
        self.layout4.addWidget(self.button['1'])
        self.layout4.addWidget(self.button['2'])
        self.layout4.addWidget(self.button['3'])
        self.layout4.addWidget(self.button['+'])
        self.layout5.addWidget(self.button['0'])
        self.layout5.addWidget(self.button['.'])
        self.layout5.addWidget(self.button['='])

        self.mainLayout.addLayout(self.layout1)
        self.mainLayout.addLayout(self.layout2)
        self.mainLayout.addLayout(self.layout3)
        self.mainLayout.addLayout(self.layout4)
        self.mainLayout.addLayout(self.layout5)

    def setDisplayText(self, text):
        # set and update the display's text
        self.display.setText(text)

    def displayText(self):
        # display's current text when click "=" 
        return self.display.text()
class CalculatorCtrl:
    """Calculator Controller."""
    def __init__(self, view):
        self._view = view
        # connect signals with buttons
        self._connectSignals()
        
        ### set all variables
        self.num = 0.0
        self.newNum = 0.0
        # sum of operator pressed(in case 1+1+1)
        self.sumOp = 0.0
        self.sumAll = 0.0
        self.operator = ''
        # having operator (when false can press number)
        self.opeSign = False
        # ensure if operator changed (in case 1+-2) 
        self.sumOpeSign = 0
        self._view.setDisplayText('0')

        # set font size
        self.font = self._view.display.font()
        self.font.setPointSize(50)
        self._view.display.setFont(self.font)
        
    def _connectSignals(self):
        """connect signals and buttons"""
        for Text, btn in self._view.button.items():
            # text is the button pressed 
            if Text not in {'=', 'C', 'AC', '+', '-', '*', '/', '.', '%'}:
                btn.clicked.connect(partial(self.Num, Text))
            elif Text in {'+', '-', '*', '/'}:
                btn.clicked.connect(partial(self.Operator, Text))

        self._view.button['='].clicked.connect(self.Equal)
        self._view.button['C'].clicked.connect(self.Clear)
        self._view.button['AC'].clicked.connect(self.AllClear)
        self._view.button['.'].clicked.connect(self.Point)
        self._view.button['%'].clicked.connect(self.Percent)
        
    def Num(self, text):
        # when input is number
        self.newNum = text
        numm = str(self.newNum)

        if self.opeSign == False:
            if self._view.display.text() == '0':
                self._view.setDisplayText(str(numm))
            else:
                self._view.setDisplayText(self._view.display.text() + str(numm))
        else:
            self._view.setDisplayText(numm)
            self.sumOpeSign = 0
            self.opeSign = False
        self.fontSize()
    
    def Operator(self, ope):
        # when input is + - * /
        self.sumOp += 1
        self.newNum = self._view.display.text()

        if self.sumOp > 1 and self.sumOpeSign == 0:
            if self.operator == '+':
                self.sumAll = float(self.num) + float(self.newNum)
            elif self.operator == '-':
                self.sumAll = float(self.num) - float(self.newNum)
            elif self.operator == '*':
                self.sumAll = float(self.num) * float(self.newNum)
            elif self.operator == '/':
                self.sumAll = float(self.num) / float(self.newNum)

            self._view.setDisplayText(str(self.sumAll))
            self.num  = self.sumAll

        else:
            self.num = self._view.display.text()
        
        self.operator = ope
        self.opeSign = True
        self.sumOpeSign += 1
        self.fontSize()

    def Point(self):
        # when input is .
        if self.opeSign == True:
            self._view.setDisplayText('0.')
            self.sumOpeSign = 0
            self.opeSign = False
        elif '.' not in self._view.display.text():
            self._view.setDisplayText(self._view.display.text() + '.')
           
    def Equal(self):
        # when = is pressed
        self.newNum = self._view.display.text()
        self.sumOp = 0

        if self.operator == '+':
            self.sumAll = float(self.num) + float(self.newNum)
        elif self.operator == '-':
            self.sumAll = float(self.num) - float(self.newNum)
        elif self.operator == '*':
            self.sumAll = float(self.num) * float(self.newNum)
        elif self.operator == '/':
            self.sumAll = float(self.num) / float(self.newNum)

        self._view.setDisplayText(str(self.sumAll))
        self.num  = self.sumAll
        self.opeSign = True 
        self.fontSize()

    def AllClear(self):
        # AC clear everything
        self.num = 0.0
        self.newNum = 0.0
        self.summ = 0.0
        self.sumAll = 0.0
        self.operator = ''
        self.opeSign = False

        self._view.setDisplayText('0')
        self.fontSize()

    def Clear(self):
        # clear num just pressed(num that appeared on display)
        self._view.setDisplayText('0')
        self.fontSize()

    def Percent(self):
        if self._view.displayText() != '0':
            percent = str(float(self._view.displayText()) / 100)
            self._view.setDisplayText(percent)
        self.fontSize()
        
    def fontSize(self):
        if len(str(self._view.display.text())) < 11:
            self.font.setPointSize(50)
        else:
            size = 50 - len(str(self._view.display.text()))
            self.font.setPointSize(size)
        self._view.display.setFont(self.font)

def main():
    """Main function"""
    mycalcu = QApplication([])
    # Show the calculator's GUI
    view = MyCal()
    view.setAttribute(Qt.WA_StyledBackground, True)
    view.setStyleSheet('background-color : #cbcbd4')
    view.show()
    # Create instances of the model and the controller
    CalculatorCtrl(view=view)
    mycalcu.exec_()

main()


