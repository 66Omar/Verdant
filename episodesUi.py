from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QListWidget, QListWidgetItem, QCheckBox


downloads = []


class QCustomQWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        global downloads
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textName = QLabel()
        self.textUpQLabel = QLabel()
        self.textDownQLabel = QLabel()
        self.textDownQLabel.hide()
        self.check = QCheckBox()
        self.check.clicked.connect(self.check_state)

        self.textQVBoxLayout.addWidget(self.textName)
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)

        self.allQHBoxLayout = QHBoxLayout()
        self.allQHBoxLayout.addWidget(self.check, 0)

        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            QLabel {
            color: white;
            margin-left: 100px;
            font-size: 14px;
            }
            ''')
        self.textName.setStyleSheet('''
            QLabel {
            color: white;
            margin-top: 5px;
            margin-left: 100px;
            font-size: 14px;
            }
            ''')

        self.check.setStyleSheet('''
            QCheckBox {
            margin-left: 170px;
            }
            ''')

    def set_text_up(self, text):
        self.textUpQLabel.setText(text)

    def set_text_down(self, text):
        self.textDownQLabel.setText(text)

    def set_name(self, text):
        self.textName.setText(text)

    def check_state(self):
        if self.check.isChecked():
            if self.textDownQLabel.text() not in downloads:
                downloads.append(self.textDownQLabel.text())
        else:
            if self.textDownQLabel.text() in downloads:
                downloads.remove(self.textDownQLabel.text())

    def add(self):
        if self.check.isChecked():
            self.check.setChecked(False)
            if self.textDownQLabel.text() in downloads:
                downloads.remove(self.textDownQLabel.text())
        else:
            self.check.setChecked(True)
            if self.textDownQLabel.text() not in downloads:
                downloads.append(self.textDownQLabel.text())


class Episodes(QListWidget):
    def __init__(self, parent=None, *args):
        super(Episodes, self).__init__(parent)
        self.all_added = None
        self.setStyleSheet('''
        QListWidget {
        background: #161219;
        border: none;
        }
        QListWidget::item {
         border-bottom: 1px solid black; 
        }
        QListWidget::item:selected {
        background: rgb(128,128,255);
        }
        QListWidget::item:focus {
        background: rgb(128,128,255);
        }
        QScrollBar:vertical {
        background: #2f2f2f;
        width: 7px;
        margin: 0;
        }
        
        QScrollBar::handle:vertical {
        background: #5b5b5b;
        }
        
        QScrollBar::add-line:vertical {
        height: 0px;
        }
        
        QScrollBar::sub-line:vertical {
        height: 0px;
        }
    
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        height: 0px;
        background: none;
        }
        ''')

        for index, link in enumerate(args):
            self.myQCustomQWidget = QCustomQWidget()
            self.myQCustomQWidget.set_name(self.parent().name)
            self.myQCustomQWidget.set_text_up('Episode ' + str(index + 1))
            self.myQCustomQWidget.set_text_down(link)

            self.myQListWidgetItem = QListWidgetItem()
            self.myQListWidgetItem.setSizeHint(self.myQCustomQWidget.sizeHint())

            self.addItem(self.myQListWidgetItem)
            self.setItemWidget(self.myQListWidgetItem, self.myQCustomQWidget)

        self.itemClicked.connect(self.add_self)

    def add_self(self, current):
        current_item = self.itemWidget(current)
        current_item.add()

    def clear_downloads(self):
        global downloads
        downloads = []

    def get_downloads(self):
        global downloads
        return downloads
