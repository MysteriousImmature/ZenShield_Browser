import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # Tab Widget to hold multiple tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.update_current_tab)

        # Set the tab widget as the central widget
        self.setCentralWidget(self.tabs)
        self.showMaximized()

        # Navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Back button
        back_btn = QAction(QIcon('icons/back.png'), 'Back', self)
        back_btn.setToolTip('Go back to the previous page')
        back_btn.triggered.connect(lambda: self.current_browser().back())
        navbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction(QIcon('icons/forward.png'), 'Forward', self)
        forward_btn.setToolTip('Go forward to the next page')
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        navbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction(QIcon('icons/reload.png'), 'Reload', self)
        reload_btn.setToolTip('Reload the current page')
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        navbar.addAction(reload_btn)

        # Home button
        home_btn = QAction(QIcon('icons/home.png'), 'Home', self)
        home_btn.setToolTip('Go to the homepage')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # New Tab button
        new_tab_btn = QAction(QIcon('icons/new_tab.png'), 'New Tab', self)
        new_tab_btn.setToolTip('Open a new tab')
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(QUrl('https://duckduckgo.com'), "New Tab"))
        navbar.addAction(new_tab_btn)

        # Close Tab button (replaces Stop button)
        close_tab_btn = QAction(QIcon('icons/stop.png'), 'Close Tab', self)
        close_tab_btn.setToolTip('Close the current tab')
        close_tab_btn.triggered.connect(lambda: self.close_current_tab(self.tabs.currentIndex()))
        navbar.addAction(close_tab_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        navbar.addWidget(self.progress)

        # Open the first tab
        self.add_new_tab(QUrl('https://duckduckgo.com'), 'New Tab')

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl('https://duckduckgo.com')

        # Create a new browser view for the tab
        browser = QWebEngineView()
        browser.setUrl(qurl)
        
        # Add new tab to the tabs widget and set it as the current tab
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # Connect signals for title, progress, and URL updates specific to this browser
        browser.loadProgress.connect(self.update_progress)
        browser.urlChanged.connect(self.update_url)
        browser.titleChanged.connect(lambda title: self.update_tab_title(i, title))

    def current_browser(self):
        return self.tabs.currentWidget()

    def close_current_tab(self, i=None):
        if i is None:
            i = self.tabs.currentIndex()
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def update_current_tab(self, i):
        browser = self.current_browser()
        if browser:
            # Update the URL bar for the new tab
            self.update_url(browser.url())

    def navigate_home(self):
        self.current_browser().setUrl(QUrl('https://duckduckgo.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http'):
            url = 'https://duckduckgo.com/?q=' + url.replace(' ', '+')
        self.current_browser().setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def update_progress(self, progress):
        self.progress.setValue(progress)

    def update_tab_title(self, index, title):
        # Set the title of the tab at the specified index
        self.tabs.setTabText(index, title if title else "New Tab")


app = QApplication(sys.argv)
QApplication.setApplicationName('Tabbed Browser')
window = MainWindow()
app.exec_()
