from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QDialogButtonBox


class QualityDialog(QDialog):
    def __init__(self, parent=None):
        super(QualityDialog, self).__init__(parent)
        self.setStyleSheet('''
        QDialog {
        background: #161219;
        }'''
        )
        self.quality = None
        self.setFixedWidth(int(self.parent().width() / 3))
        self.setFixedHeight(int(self.parent().height() / 4))
        self.setWindowTitle("Quality")
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.mainlayout = QVBoxLayout()
        self.sublayout = QHBoxLayout()
        self.label = QLabel("Select video quality: ")

        self.label.setStyleSheet('''
        QLabel {
        color: white;
        font: 15px;
        margin: 10px;
        }
        ''')

        self.combo = QComboBox()
        self.combo.addItem("144")
        self.combo.addItem("240")
        self.combo.addItem("360")
        self.combo.addItem("480")
        self.combo.addItem("720")
        self.combo.addItem("1080")

        self.sublayout.addWidget(self.label)
        self.sublayout.addWidget(self.combo)
        self.setLayout(self.mainlayout)
        self.mainlayout.addLayout(self.sublayout)
        self.layout().addWidget(self.buttonBox)

    def accept(self):
        self.quality = self.combo.currentText()
        super(QualityDialog, self).accept()

    def reject(self):
        self.quality = None
        super(QualityDialog, self).reject()
