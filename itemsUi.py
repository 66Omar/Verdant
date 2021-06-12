from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton
from quality_dialog import QualityDialog


class QCustomQWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel = QLabel()
        self.textDownQLabel = QLabel()
        self.download = QPushButton()
        self.download.setFixedWidth(200)
        self.download.setFixedHeight(30)
        self.download.setText("Download")
        self.download.hide()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)

        self.allQHBoxLayout = QHBoxLayout()
        self.iconQLabel = QLabel()
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 0)
        self.allQHBoxLayout.addWidget(self.download, 1)

        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            QLabel {
            color: white;
            margin-left: 100px;
            font-size: 13px;
            }
        ''')
        self.textDownQLabel.setStyleSheet('''
            QLabel {
            color: white;
            margin-left: 100px;
            font-size: 13px;
            }
        ''')
        self.download.setStyleSheet('''
            QPushButton {
            margin-right: 100px;
            background: #00b300;
            border-radius: 12px;
            font: bold;
            }
            QPushButton::hover {
            margin-right: 100px;
            background: #00e600;
            border-radius: 12px;
            font: bold;
            }
            QPushButton::pressed {
            margin-right: 100px;
            background: #007600;
            border-radius: 12px;
            font: bold;
            }
        ''')

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)

    def showDownload(self):
        self.download.show()

    def get_text(self):
        return self.textUpQLabel.text()

    def get_text_down(self):
        return self.textDownQLabel.text()


class Items(QListWidget):
    def __init__(self, parent=None, **kwagrs):
        super(Items, self).__init__(parent)
        self.needed = kwagrs
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

        for name in kwagrs:
            show = False
            series = kwagrs[name]
            if 'series' in series:
                series = 'Series'
            else:
                series = 'Movie'
                show = True

            self.myQCustomQWidget = QCustomQWidget()
            self.myQCustomQWidget.setTextUp(name)
            self.myQCustomQWidget.setTextDown(series)
            if show:
                self.myQCustomQWidget.showDownload()
                self.myQCustomQWidget.download.clicked.connect(lambda: self.go_to_download())
            self.myQListWidgetItem = QListWidgetItem()
            self.myQListWidgetItem.setSizeHint(self.myQCustomQWidget.sizeHint())
            self.addItem(self.myQListWidgetItem)
            self.setItemWidget(self.myQListWidgetItem, self.myQCustomQWidget)
        self.itemDoubleClicked.connect(self.check_and_initialize)

    def go_to_download(self):
        if self.parent().parent().seasons_worker is None or not self.parent().parent().seasons_worker.isRunning():
            dialog = QualityDialog(self)
            dialog.exec_()
            if dialog.quality is not None:
                name = self.sender().parent().get_text()
                items = [self.needed[name]]
                self.parent().parent().name = name
                self.parent().parent().prepare_download_page(0, items, dialog.quality)

    def check_and_initialize(self, item):
        current_item = self.itemWidget(item).get_text_down()
        if str(current_item).lower() == 'series':
            self.parent().parent().init_seasons_worker(item)
