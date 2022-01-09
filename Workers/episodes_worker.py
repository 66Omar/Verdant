from PyQt5.QtCore import QThread, pyqtSignal
from Scraping.episodes import get_episodes


class EpisodesWorker(QThread):
    state = pyqtSignal(int)
    done = pyqtSignal(list)

    def __init__(self, name):
        self.name = name
        super(EpisodesWorker, self).__init__()

    def run(self):
        items = []

        try:
            self.state.emit(0)
            items = get_episodes(self.name)
            status = 0
            self.state.emit(1)
        except:
            status = 1

        self.done.emit([items, status])
        self.state.emit(2)
