from PyQt5.QtCore import QThread, pyqtSignal
from Scraping.searching import search_for


class SearchWorker(QThread):
    done = pyqtSignal(list)

    def __init__(self, name):
        super(SearchWorker, self).__init__()
        self.name = name

    def run(self):
        items = {}

        try:
            items = search_for(self.name)
            status = 0
        except:
            status = 1
        self.done.emit([items, status])

