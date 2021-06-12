from PyQt5.QtCore import QThread, pyqtSignal
from Scraping.episodes import get_episodes


class EpisodesWorker(QThread):
    done = pyqtSignal(list)

    def __init__(self, name):
        self.name = name
        super(EpisodesWorker, self).__init__()

    def run(self):
        items = []

        try:
            items = get_episodes(self.name)
            status = 0
        except:
            status = 1

        self.done.emit([items, status])

