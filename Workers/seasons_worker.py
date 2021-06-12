from PyQt5.QtCore import QThread, pyqtSignal
from Scraping.get_item import get_seasons


class SeasonWorker(QThread):
    done = pyqtSignal(list)

    def __init__(self, name):
        self.name = name
        super(SeasonWorker, self).__init__()

    def run(self):
        items = {}

        try:
            items = get_seasons(self.name)
            status = 0
        except:
            status = 1

        self.done.emit([items, status])

