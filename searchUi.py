from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect, QCoreApplication, Qt


class Ui(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui, self).__init__(parent)
        self.name = QLabel(self)
        self.search_btn = QPushButton(self)
        self.search_bar = QLineEdit(self)
        self.search_bar.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.style_views()
        self.adjust_views()



    def style_views(self):
        self.search_bar.setObjectName(u"search_bar")
        self.search_bar.setGeometry(QRect(150, 220, 550, 50))
        font = QFont()
        font.setPointSize(15)
        self.search_bar.setFont(font)
        self.search_bar.setStyleSheet(u".QLineEdit {\n"
                                      "border-radius: 25px;\n"
                                      "padding: 13px;\n"
                                      "}")
        self.search_btn.setObjectName(u"search_btn")
        self.search_btn.setGeometry(QRect(320, 330, 175, 50))
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(True)
        font1.setWeight(75)
        self.search_btn.setFont(font1)
        self.search_btn.setStyleSheet(u"QPushButton {\n"
                                      "	color: #ffffff;\n"
                                      "    background-color: #4682b4;\n"
                                      "    border-width: 2px;\n"
                                      "    border-radius: 25px;\n"
                                      "    padding: 6px;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover {\n"
                                      "    background-color: #588ebb;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:pressed {\n"
                                      "    background-color: #3f75a2;\n"
                                      "}\n"
                                      "")
        self.name.setObjectName(u"name")
        self.name.setGeometry(QRect(310, 70, 200, 71))
        font2 = QFont()
        font2.setFamily(u"Script MT Bold")
        font2.setPointSize(48)
        font2.setBold(True)
        font2.setWeight(75)
        self.name.setFont(font2)
        self.name.setStyleSheet(u"color:white;")

        self.search_bar.textChanged.connect(self.hint)


        self.search_bar.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search Egybest..", None))
        self.search_btn.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.search_btn.setShortcut(QCoreApplication.translate("MainWindow", u"Return", None))
        self.name.setText(QCoreApplication.translate("MainWindow", u"Verdant", None))

    def adjust_views(self):
        width = self.parent().width()
        self.name.setGeometry(int((width-self.name.width())/2), int(self.name.y()), int(self.name.width()), int(self.name.height()))
        self.search_btn.setGeometry(int((width - self.search_btn.width()) / 2), int(self.search_btn.y()), int(self.search_btn.width()),
                              int(self.search_btn.height()))
        self.search_bar.setGeometry(int((width - self.search_bar.width()) / 2), int(self.search_bar.y()),
                                    int(self.search_bar.width()),
                                    int(self.search_bar.height()))

    def hint(self):
        if self.search_bar.text() == "":
            font = QtGui.QFont("Bahnschrift SemiLight", 15)
            self.search_bar.setFont(font)
        else:
            font = QtGui.QFont("Arial", 16, QtGui.QFont.Bold)
            self.search_bar.setFont(font)

    def getText(self):
        return self.search_bar.text()