from PyQt5.QtWidgets import QPushButton


class GetSelected(QPushButton):
    def __init__(self):
        super(GetSelected, self).__init__()
        self.setFixedHeight(50)
        self.setFixedWidth(240)
        self.setText("Download")
        self.setStyleSheet('''
                            QPushButton {
                            margin-right: 70px;
                            margin-bottom: 10px;
                            background: #00b300;
                            border-radius: 12px;
                            font: bold;
                            }
                            QPushButton::hover {
                            background: #00e600;
                            border-radius: 12px;
                            font: bold;
                            }
                            QPushButton::pressed {
                            background: #007600;
                            border-radius: 12px;
                            font: bold;
                            }
                        ''')
