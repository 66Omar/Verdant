from PyQt5.QtWidgets import QPushButton

class AutoButton(QPushButton):
    def __init__(self):
        super(AutoButton, self).__init__()
        self.setText("Auto Start")
        self.setFixedHeight(50)
        self.setFixedWidth(230)
        self.state = True
        self.setStyleSheet('''
        QPushButton {
            margin-right: 50px;
            margin-bottom: 15px;
            background: green;
            font: bold;
            color: white;
            border-radius: 15px;
            }
            ''')
        self.pressed.connect(self.change)

    def change(self):
        if self.state:
            self.setStyleSheet('''
            QPushButton {
            margin-right: 50px;
            margin-bottom: 15px;
            background: red;
            font: bold;
            color: white;
            border-radius: 15px;

            }
            ''')
            self.state = False
        else:
            self.setStyleSheet('''
            QPushButton {
                margin-right: 50px;
                margin-bottom: 15px;
                background: green;
                font: bold;
                color: white;
                border-radius: 15px;
                }
                ''')
            self.state = True
