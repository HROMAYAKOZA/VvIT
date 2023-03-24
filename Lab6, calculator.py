import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox

class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()
        self.op=""
        self.vbox = QVBoxLayout(self) # параметры окна
        self.hbox_input = QHBoxLayout()
        self.hbox_first = QHBoxLayout()
        self.hbox_second = QHBoxLayout()
        self.hbox_third = QHBoxLayout()
        self.hbox_fourth = QHBoxLayout()
        self.hbox_result = QHBoxLayout()

        self.vbox.addLayout(self.hbox_input) # вертикальные уровни
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addLayout(self.hbox_second)
        self.vbox.addLayout(self.hbox_third)
        self.vbox.addLayout(self.hbox_fourth)
        self.vbox.addLayout(self.hbox_result)

        self.input = QLineEdit(self)
        self.hbox_input.addWidget(self.input)

        self.b_7 = QPushButton("7", self)
        self.hbox_first.addWidget(self.b_7)

        self.b_8 = QPushButton("8", self)
        self.hbox_first.addWidget(self.b_8)

        self.b_9 = QPushButton("9", self)
        self.hbox_first.addWidget(self.b_9)

        self.b_div = QPushButton("/", self)
        self.hbox_first.addWidget(self.b_div)

        self.b_4 = QPushButton("4", self)
        self.hbox_second.addWidget(self.b_4)

        self.b_5 = QPushButton("5", self)
        self.hbox_second.addWidget(self.b_5)

        self.b_6 = QPushButton("6", self)
        self.hbox_second.addWidget(self.b_6)

        self.b_mult = QPushButton("*", self)
        self.hbox_second.addWidget(self.b_mult)

        self.b_1 = QPushButton("1", self)
        self.hbox_third.addWidget(self.b_1)

        self.b_2 = QPushButton("2", self)
        self.hbox_third.addWidget(self.b_2)

        self.b_3 = QPushButton("3", self)
        self.hbox_third.addWidget(self.b_3)

        self.b_minus = QPushButton("-", self)
        self.hbox_third.addWidget(self.b_minus)

        self.b_res = QPushButton("C", self)
        self.hbox_fourth.addWidget(self.b_res)

        self.b_0 = QPushButton("0", self)
        self.hbox_fourth.addWidget(self.b_0)

        self.b_dot = QPushButton(".", self)
        self.hbox_fourth.addWidget(self.b_dot)

        self.b_plus = QPushButton("+", self)
        self.hbox_fourth.addWidget(self.b_plus)

        self.b_result = QPushButton("=", self)
        self.hbox_result.addWidget(self.b_result)

        self.b_plus.clicked.connect(lambda: self._operation("+"))
        self.b_minus.clicked.connect(lambda: self._operation("-"))
        self.b_mult.clicked.connect(lambda: self._operation("*"))
        self.b_div.clicked.connect(lambda: self._operation("/"))
        self.b_res.clicked.connect(self._reset)
        self.b_result.clicked.connect(self._result)

        self.b_1.clicked.connect(lambda: self._button("1"))
        self.b_2.clicked.connect(lambda: self._button("2"))
        self.b_3.clicked.connect(lambda: self._button("3"))
        self.b_4.clicked.connect(lambda: self._button("4"))
        self.b_5.clicked.connect(lambda: self._button("5"))
        self.b_6.clicked.connect(lambda: self._button("6"))
        self.b_7.clicked.connect(lambda: self._button("7"))
        self.b_8.clicked.connect(lambda: self._button("8"))
        self.b_9.clicked.connect(lambda: self._button("9"))
        self.b_0.clicked.connect(lambda: self._button("0"))
        self.b_dot.clicked.connect(lambda: self._button("."))

    def _button(self, param): # ввод цифры/дробного числа
        line = self.input.text()
        
        self.input.setText(line + param)

    def _operation(self, op): # сложегние/вычитание/умножение/деление
        if self.op != "":
            subr=self._subresult(self.op)
            if subr==0:
                return 0
            else:
                self.input.setText(self._subresult(self.op))
        temp = self.input.text()
        if temp.count(".")>1:
            QMessageBox.about(self, "Error", "More than one dot in a digit")
            self._reset()
            return 0
        if temp[0]=='.':
            QMessageBox.about(self, "Error", "Digit can't begin from dot")
            self._reset()
            return 0
        self.num_1 = float(temp)
        self.op = op
        if(self.num_1==int(self.num_1)):
            self.num_1=int(self.num_1)
        self.input.setText(str(self.num_1)+op)

    def _subresult(self,op): # несколько действий
        temp = self.input.text().replace(str(self.num_1),"",1).replace(op,"",1)
        if temp.count(".")>1:
            QMessageBox.about(self, "Error", "More than one dot in a digit")
            self._reset()
            return 0
        if temp[0]=='.':
            QMessageBox.about(self, "Error", "Digit can't begin from dot")
            self._reset()
            return 0
        self.num_2 = float(temp)
        if self.op == "+":
            self.ans = self.num_1 + self.num_2
        if self.op == "-":
            self.ans = self.num_1 - self.num_2
        if self.op == "*":
            self.ans = self.num_1 * self.num_2
        if self.op == "/":
            if(self.num_2==0):
                QMessageBox.about(self, "Error", "Divide by zero")
                self._reset()
                return 0
            else:
                self.ans = self.num_1 / self.num_2
        if(self.ans==int(self.ans)):
            return str(int(self.ans))
        return str(round(self.ans, 9))

    def _result(self): # равно
        temp = self.input.text().replace(str(self.num_1),"",1).replace(self.op,"",1)
        if temp.count(".")>1:
            QMessageBox.about(self, "Error", "More than one dot in a digit")
            self._reset()
            return 0
        if temp[0]=='.':
            QMessageBox.about(self, "Error", "Digit can't begin from dot")
            self._reset()
            return 0
        self.num_2 = float(temp)
        if self.op == "+":
            self.ans = self.num_1 + self.num_2
        if self.op == "-":
            self.ans = self.num_1 - self.num_2
        if self.op == "*":
            self.ans = self.num_1 * self.num_2
        if self.op == "/":
            if(self.num_2==0):
                QMessageBox.about(self, "Error", "Divide by zero")
                self._reset()
                return 0
            else:
                self.ans = self.num_1 / self.num_2
        if(self.ans==int(self.ans)):
            self.input.setText(self.input.text() + " = " + str(int(self.ans)))
        else:   
            self.input.setText(self.input.text() + " = " + str(round(self.ans, 9)))

    def _reset(self): # сброс
        self.num_1,self.num_2 = 0, 0
        self.op = ""
        self.input.setText("")
        self.ans=0

            
app = QApplication(sys.argv)

win = Calculator()
win.show()

sys.exit(app.exec_())