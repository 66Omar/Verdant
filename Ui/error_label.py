from PyQt5.QtWidgets import QLabel


class ErrorLabel(QLabel):
    def __init__(self):
        super(ErrorLabel, self).__init__()
        self.setStyleSheet('''
        QLabel{
        color: gray;
        font: 30px;
            }
        ''')
