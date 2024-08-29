import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://duckduckgo.com'))  # Default to DuckDuckGo
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        stop_btn = QAction('Stop', self)
        stop_btn.triggered.connect(self.browser.stop)
        navbar.addAction(stop_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        navbar.addWidget(self.progress)

        self.browser.loadProgress.connect(self.update_progress)
        self.browser.urlChanged.connect(self.update_url)

    def navigate_home(self):
        self.browser.setUrl(QUrl('https://duckduckgo.com'))  # Home button navigates to DuckDuckGo

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http'):
            # If the text does not start with 'http', treat it as a search query
            url = 'https://duckduckgo.com/?q=' + url.replace(' ', '+')
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def update_progress(self, progress):
        self.progress.setValue(progress)


app = QApplication(sys.argv)
QApplication.setApplicationName('Basic Browser')
window = MainWindow()
app.exec_()
