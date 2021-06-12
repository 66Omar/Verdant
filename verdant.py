import sys
import webbrowser
from seasonsUi import Seasons
from episodesUi import Episodes
from itemsUi import Items
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout
from searchUi import Ui as Search
from downloadUi import Downloads
from Ui.back_button import BackButton
from quality_dialog import QualityDialog
from Ui.auto_btn import AutoButton
from Ui.error_label import ErrorLabel
from Ui.get_selected_btn import GetSelected
from Workers.search_worker import SearchWorker
from Workers.seasons_worker import SeasonWorker
from Workers.episodes_worker import EpisodesWorker
from Workers.download_worker import DownloadWorker


class Ui(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.downloads = None
        self.setStyleSheet('''
                QMainWindow { 
                background: #161219;
                }''')
        self.setWindowTitle("Verdant")

        self.items = None
        self.seasons = None
        self.episodes = None

        self.items_but = None
        self.seasons_but = None
        self.episodes_but = None
        self.downloads_but = None
        self.auto_but = None
        self.get_selected = None

        self.label = None

        self.auto = True
        self.quality = 480  # Default Value

        self.search_worker = None
        self.seasons_worker = None
        self.episodes_worker = None
        self.second_episodes_worker = None
        self.download_worker = None

        self.name = None
        self.setFixedWidth(1000)
        self.setFixedHeight(650)
        self.main_win = QWidget()
        self.main_lo = QVBoxLayout()

        self.search_screen = Search(self)

        self.main_lo.setContentsMargins(0, 0, 0, 0)
        self.main_lo.addWidget(self.search_screen)
        self.main_win.setLayout(self.main_lo)
        self.setCentralWidget(self.main_win)

        self.search_screen.search_btn.clicked.connect(self.init_search_worker)

    def init_search_worker(self):
        if self.items is None:
            self.search_worker = SearchWorker(self.search_screen.getText())
            self.search_worker.start()
            self.search_worker.done.connect(self.items_page)

    def init_seasons_worker(self, item):
        if self.seasons is None:
            self.items.itemDoubleClicked.disconnect()
            self.items_but.setEnabled(False)
            current_item = self.items.itemWidget(item)
            selected_item = self.items.needed[current_item.get_text()]
            self.name = current_item.get_text()
            self.seasons_worker = SeasonWorker(selected_item)
            self.seasons_worker.start()
            self.seasons_worker.done.connect(self.seasons_page)

    def init_episodes_worker(self, item):
        if self.episodes is None:
            self.seasons.itemDoubleClicked.disconnect()
            self.seasons_but.setEnabled(False)
            current_item = self.seasons.itemWidget(item)
            season = self.seasons.needed[current_item.get_text()]
            self.name = current_item.get_text()
            self.episodes_worker = EpisodesWorker(season)
            self.episodes_worker.start()
            self.episodes_worker.done.connect(self.episodes_page)

    def items_page(self, items):
        self.hide_this(self.search_screen)
        self.items_but = BackButton()
        if len(items[0]) == 0 and items[1] == 0:
            self.label = ErrorLabel()
            self.show_this(self.items, self.items_but)
            self.show_error("No results found!")
        elif items[1] == 1:
            self.label = ErrorLabel()
            self.show_this(self.items, self.items_but)
            self.show_error("No internet connection!")
        else:
            if self.items is None:
                self.items = Items(self, **items[0])
                self.show_this(self.items, self.items_but)

        self.items_but.clicked.connect(self.back_to_search)

    def seasons_page(self, seasons):
        self.hide_this(self.items, self.items_but)
        self.seasons_but = BackButton()
        if len(seasons[0]) == 0 and seasons[1] == 0:
            self.show_this(self.seasons, self.seasons_but)
            self.show_error("No results found!")
        elif seasons[1] == 1:
            self.show_this(self.seasons, self.seasons_but)
            self.show_error("No internet connection!")
        else:
            if self.seasons is None:
                self.seasons = Seasons(self, **seasons[0])
                self.show_this(self.seasons, self.seasons_but)
                self.seasons.itemDoubleClicked.connect(self.init_episodes_worker)

        self.seasons_but.clicked.connect(self.back_to_items)

    def episodes_page(self, episodes):
        self.hide_this(self.seasons, self.seasons_but)
        self.episodes_but = BackButton()
        if len(episodes[0]) == 0 and episodes[1] == 0:
            self.show_this(self.episodes, self.episodes_but)
            self.show_error("No results found!")
        elif episodes[1] == 1:
            self.show_this(self.episodes, self.episodes_but)
            self.show_error("No internet connection!")
        else:
            if self.episodes is None:
                self.episodes = Episodes(self, *episodes[0])
                self.get_selected = GetSelected()
                self.show_this(self.episodes, button=self.episodes_but, download_button=self.get_selected)
                self.episodes.clear_downloads()
                if self.get_selected is not None:
                    self.get_selected.clicked.connect(self.episodes_quality)

        self.episodes_but.clicked.connect(self.back_to_seasons)

    def episodes_quality(self):
        dialog = QualityDialog(self)
        dialog.exec_()
        if dialog.quality is not None:
            self.prepare_download_page(2, self.episodes.get_downloads(), dialog.quality)

    def prepare_download_page(self, page, items, quality):
        self.quality = quality
        if page == 0:
            self.hide_this(self.items, self.items_but)
            self.download_page(items, 0)
        if page == 1:
            self.second_episodes_worker = EpisodesWorker(items[0])
            self.second_episodes_worker.start()
            self.second_episodes_worker.done.connect(self.download_page)
        if page == 2:
            self.hide_this(self.episodes, self.episodes_but, self.get_selected)
            self.download_page(items, 1)

    def download_page(self, items, state=None):
        self.downloads_but = BackButton()
        self.auto_but = AutoButton()
        if len(items) > 1 and isinstance(items[1], int):
            self.hide_this(self.seasons, self.seasons_but)
            self.downloads = Downloads(self.name, items[0], parent=self)
            self.show_this(self.downloads, self.downloads_but, self.auto_but)
        else:
            self.downloads = Downloads(self.name, items, parent=self)
            self.show_this(self.downloads, self.downloads_but, self.auto_but)
        self.auto_but.clicked.connect(self.auto_state)
        self.downloads_but.clicked.connect(lambda: self.back_to_episodes(state))
        QApplication.processEvents()
        list_items = self.downloads.get_download_links()
        self.download_worker = DownloadWorker(self.downloads, list_items, self.quality)
        self.download_worker.start()
        self.download_worker.update.connect(self.update_this)
        self.download_worker.send.connect(self.start_downloading)

    def auto_state(self):
        self.auto = self.auto_but.state

    def update_this(self, item):
        if self.downloads is not None:
            if item[1] == 0:
                self.downloads.itemWidget(item[0]).set_progress_text("Initialized")
            else:
                self.downloads.itemWidget(item[0]).set_progress_text("Finished")

    def start_downloading(self, string):
        if self.auto:
            webbrowser.open(string)

    def back_to_search(self):
        self.close_this(self.items, self.items_but, label=self.label, state=0)
        self.show_this(self.search_screen)

    def back_to_items(self):
        self.close_this(self.seasons, self.seasons_but, label=self.label, state=1)
        self.items.itemDoubleClicked.connect(self.items.check_and_initialize)
        self.show_this(self.items, self.items_but)

    def back_to_seasons(self):
        self.close_this(self.episodes, self.episodes_but, self.get_selected, label=self.label, state=2)
        self.seasons.itemDoubleClicked.connect(self.init_episodes_worker)
        self.show_this(self.seasons, self.seasons_but)

    def back_to_episodes(self, state=None):
        if self.download_worker is not None:
            if self.download_worker.driver is not None:
                self.download_worker.driver.quit()
        self.close_this(self.downloads, button=self.downloads_but,
                        download_button=self.auto_but, label=self.label, state=3)
        if state == 0:
            self.show_this(self.items, self.items_but)
        elif state == 1:
            self.show_this(self.episodes, self.episodes_but, self.get_selected)
        else:
            self.show_this(self.seasons, self.seasons_but)
        if self.download_worker is not None:
            self.download_worker.quit()
            self.download_worker.con = False
            if self.download_worker.driver is not None:
                self.download_worker.driver.quit()

    def hide_this(self, page, button=None, download_button=None):
        if button is not None:
            self.main_lo.removeWidget(button)
            button.hide()
        if page is not None:
            self.main_lo.removeWidget(page)
            page.hide()
        if download_button is not None:
            self.main_lo.removeWidget(download_button)
            download_button.hide()

    def show_this(self, page, button=None, download_button=None):
        if button is not None:
            self.main_lo.addWidget(button)
            button.show()
            button.setEnabled(True)
        if page is not None:
            self.main_lo.addWidget(page)
            page.show()
        if download_button is not None:
            self.main_lo.addWidget(download_button, alignment=Qt.AlignmentFlag.AlignRight)
            download_button.show()

    def close_this(self, page, button=None, download_button=None, label=None, state=None):
        if label is not None:
            label.close()
            label.deleteLater()
            self.label.deleteLater()
            self.label = None
        if page is not None:
            page.close()
            page.deleteLater()

        if button is not None:
            button.close()
            button.clicked.disconnect()
            button.deleteLater()

        if download_button is not None:
            download_button.close()
            download_button.clicked.disconnect()
            download_button.deleteLater()

        if state == 0:
            self.items = None
            self.items_but = None
        elif state == 1:
            self.seasons = None
            self.seasons_but = None
        elif state == 2:
            self.episodes = None
            self.episodes_but = None
            self.get_selected = None
        elif state == 3:
            self.downloads = None
            self.downloads_but = None
            self.auto_but = None

    def show_error(self, text):
        self.label.setText(text)
        self.main_lo.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.label.show()


try:
    app = QApplication(sys.argv)
    win = Ui()
    win.show()
    sys.exit(app.exec_())
except:
    if win.download_worker is not None:
        win.download_worker.quit()
        win.download_worker.con = False
        if win.download_worker.driver is not None:
            win.download_worker.driver.quit()
