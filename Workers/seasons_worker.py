from PyQt5.QtCore import QThread, pyqtSignal
from Scraping.get_item import get_seasons


class SeasonWorker(QThread):
    state = pyqtSignal(int)
    done = pyqtSignal(list)

    def __init__(self, url, name):
        self.url = url
        self.name = name
        super(SeasonWorker, self).__init__()

    def run(self):
        items = {}

        try:
            self.state.emit(0)
            items = get_seasons(self.url, self.name)
            status = 0
            self.state.emit(1)
        except:
            status = 1

        self.done.emit([items, status])
        self.state.emit(2)
