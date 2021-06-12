from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton
import webbrowser


class QCustomQWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel = QLabel()
        self.textDownQLabel = QLabel()
        self.thirdlabel = QLabel()
        self.thirdlabel.hide()

        self.progress = QLabel()
        self.progress.setFixedWidth(300)
        self.progress.setFixedHeight(30)
        self.download = QPushButton()
        self.download.setStyleSheet('''
                    QPushButton {
                    margin-right: 20px;
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

        self.download.setText("Download")
        self.download.setFixedWidth(140)
        self.download.setFixedHeight(30)

        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.textQVBoxLayout.addWidget(self.thirdlabel)
        self.download.hide()

        self.allQHBoxLayout = QHBoxLayout()
        self.iconQLabel = QLabel()
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout)
        self.container = QHBoxLayout()
        self.container.addWidget(self.progress)
        self.container.addWidget(self.download)
        self.allQHBoxLayout.addLayout(self.container)
        self.container.setSpacing(0)

        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            QLabel {
            color: white;
            margin-left: 100px;
            font-size: 14px;
            }
            ''')

        self.textDownQLabel.setStyleSheet('''
            QLabel {
                color: white;
                margin-top: 5px;
                margin-left: 100px;
                font-size: 12px;
                }
            ''')

        self.progress.setText("Queued")
        self.progress.setStyleSheet('''
            QLabel {
            color: #ffff80;
            font-size: 13px;
            font: bold;
            margin-left:180px;
            }

            ''')

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)

    def set_progress_text(self, text):
        self.progress.setText(text)

    def get_text_down(self):
        return self.textDownQLabel.text()

    def set_link(self, text):
        self.thirdlabel.setText(text)

    def get_link(self):
        return self.thirdlabel.text()

    def show_btn(self):
        self.download.show()


class Downloads(QListWidget):
    def __init__(self, name, items, parent=None):
        self.name = name
        super(Downloads, self).__init__(parent)
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
                
                QScrollBar:horizontal {
                background: #2f2f2f;
                height: 7px;
                margin: 0;
                }
                
                QScrollBar::handle:horizontal {
                background: #5b5b5b;
                }

                QScrollBar::add-line:horizontal {
                width: 0px;
                }

                QScrollBar::sub-line:horizontal {
                width: 0px;
                }
                QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                width: 0px;
                background: none;
                }
                
                ''')

        for name in items:

            self.myQCustomQWidget = QCustomQWidget()
            self.myQCustomQWidget.setTextUp(self.name)
            self.myQCustomQWidget.setTextDown(name)

            self.myQListWidgetItem = QListWidgetItem()
            self.myQListWidgetItem.setSizeHint(self.myQCustomQWidget.sizeHint())
            self.addItem(self.myQListWidgetItem)
            self.myQCustomQWidget.download.clicked.connect(self.start_down)
            self.setItemWidget(self.myQListWidgetItem, self.myQCustomQWidget)

    def get_download_links(self):
        items = []
        for x in range(self.count()):
            items.append(self.item(x))
        return items

    def start_down(self):
        link = self.sender().parent().get_link()
        webbrowser.open(link)