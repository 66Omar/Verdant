from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


class BackButton(QPushButton):
    def __init__(self):
        super(BackButton, self).__init__()
        self.icon = QIcon("Ui\\backarrow.png")
        self.setIcon(self.icon)
        self.setIconSize(QSize(50, 30))
        self.setStyleSheet('''
                        QPushButton {
                        background:#00FFFFFF;
                        margin-top: 15px;
                        margin-left: 25px;
                        }
                        QPushButton::hover {
                        background: #161219;
                        }
                        ''')
        self.setFixedWidth(80)
        self.setFixedHeight(60)
