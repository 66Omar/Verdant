from PyQt5.QtCore import pyqtSignal, QThread
from Scraping.prepare_download import get_download_link
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

os.environ['WDM_LOG_LEVEL'] = '0'


class DownloadWorker(QThread):
    state = pyqtSignal(int)
    finished = pyqtSignal()
    update = pyqtSignal(list)
    send = pyqtSignal(str)

    def __init__(self, parent, items, quality):
        super(DownloadWorker, self).__init__()
        self.items = items
        self.item_parent = parent
        self.quality = quality
        self.driver = None
        self.con = True

    def run(self):
        for each in self.items:
            if self.con is False:
                print('quitting')
                break
            self.driver = None
            self.update.emit([each, 0])
            self.state.emit(0)
            link = self.item_parent.itemWidget(each).get_text_down()
            load_time = 4.5
            got_link = False
            while not got_link:
                if self.con is False:
                    print('quitting')
                    break
                try:
                    chrome_options = Options()
                    chrome_options.add_argument("--window-size=1920x1080")
                    chrome_options.add_argument("--headless")

                    self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options,
                                                   service_args=["hide_console", ])

                    x = get_download_link(self, self.driver, link, load_time, str(self.quality))
                    if '.mp4' in x[1] or '[EgyBest]' in x[1] or self.quality in x[1]:
                        self.state.emit(1)
                        got_link = True
                        self.driver.quit()
                        if self.con:
                            self.state.emit(2)
                            self.update.emit([each, 1])
                            self.item_parent.itemWidget(each).show_btn()
                            self.item_parent.itemWidget(each).set_link(str(x[0]))
                            if self.item_parent.parent().parent().auto:
                                self.send.emit(str(x[0]))

                        print('finished')

                except Exception as e:
                    if self.con:
                        load_time += 0.33333333333
                        print(str(e.args) + "#123456")
                    if self.driver is not None:
                        self.driver.quit()
        self.driver = None
        self.finished.emit()
