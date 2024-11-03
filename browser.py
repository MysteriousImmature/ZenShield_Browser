import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
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

        # Back button
        back_btn = QAction(QIcon('icons/back.png'), 'Back', self)  # Use an icon for the back button
        back_btn.setToolTip('Go back to the previous page')
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction(QIcon('icons/forward.png'), 'Forward', self)  # Use an icon for the forward button
        forward_btn.setToolTip('Go forward to the next page')
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction(QIcon('icons/reload.png'), 'Reload', self)  # Use an icon for the reload button
        reload_btn.setToolTip('Reload the current page')
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # Home button
        home_btn = QAction(QIcon('icons/home.png'), 'Home', self)  # Use an icon for the home button
        home_btn.setToolTip('Go to the homepage')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # Stop button
        stop_btn = QAction(QIcon('icons/stop.png'), 'Stop', self)  # Use an icon for the stop button
        stop_btn.setToolTip('Stop loading the page')
        stop_btn.triggered.connect(self.browser.stop)
        navbar.addAction(stop_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        navbar.addWidget(self.progress)

        # Connect signals for progress and URL updates
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
