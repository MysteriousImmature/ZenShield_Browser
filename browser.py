import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QToolBar, QAction,
    QLineEdit, QProgressBar, QDialog, QVBoxLayout, QListWidget,
    QPushButton, QHBoxLayout
)
from PyQt5.QtWebEngineWidgets import QWebEngineView


class HistoryDialog(QDialog):
    def __init__(self, history_list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Browsing History")
        self.resize(600, 400)

        self.list_widget = QListWidget()
        self.list_widget.addItems(history_list)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)

        clear_btn = QPushButton("Clear History")
        clear_btn.clicked.connect(self.clear_history)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(close_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)
        layout.addLayout(btn_layout)

    def on_item_double_clicked(self, item):
        url = item.text()
        self.parent().current_browser().setUrl(QUrl(url))
        self.close()

    def clear_history(self):
        self.list_widget.clear()
        self.parent().history.clear()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.history = []
        self._apply_light_theme()

        self.setWindowTitle("Modern Browser")
        self.resize(1200, 800)

        self._create_menu_bar()
        self._create_toolbar()
        self._create_tabs()

        # Open first tab
        self.add_new_tab(QUrl("https://duckduckgo.com"), "Home")
        self.show()

    def _apply_light_theme(self):
        """
        Apply a clean light Fusion theme with soft grey backgrounds
        and crisp dark text.
        """
        QApplication.setStyle("Fusion")
        light = QPalette()

        light.setColor(QPalette.Window, QColor(250, 250, 250))
        light.setColor(QPalette.WindowText, Qt.black)
        light.setColor(QPalette.Base, QColor(245, 245, 245))
        light.setColor(QPalette.AlternateBase, QColor(250, 250, 250))
        light.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        light.setColor(QPalette.ToolTipText, Qt.black)
        light.setColor(QPalette.Text, Qt.black)
        light.setColor(QPalette.Button, QColor(240, 240, 240))
        light.setColor(QPalette.ButtonText, Qt.black)
        light.setColor(QPalette.Highlight, QColor(42, 130, 218))
        light.setColor(QPalette.HighlightedText, Qt.white)

        QApplication.setPalette(light)

    def _create_menu_bar(self):
        menubar = self.menuBar()
        history_menu = menubar.addMenu("History")
        show_hist = QAction("Show History", self)
        show_hist.triggered.connect(self.show_history_dialog)
        history_menu.addAction(show_hist)

    def _create_toolbar(self):
        navbar = QToolBar()
        navbar.setMovable(False)
        self.addToolBar(navbar)

        icons = {
            'back':      "icons/back.svg",
            'forward':   "icons/forward.svg",
            'reload':    "icons/reload.svg",
            'home':      "icons/home.svg",
            'new_tab':   "icons/new_tab.svg",
            'close_tab': "icons/close_tab.svg",
        }

        # Navigation buttons
        back_act = QAction(QIcon(icons['back']), "Back", self)
        back_act.setToolTip("Back")
        back_act.triggered.connect(lambda: self.current_browser().back())
        navbar.addAction(back_act)

        forward_act = QAction(QIcon(icons['forward']), "Forward", self)
        forward_act.setToolTip("Forward")
        forward_act.triggered.connect(lambda: self.current_browser().forward())
        navbar.addAction(forward_act)

        reload_act = QAction(QIcon(icons['reload']), "Reload", self)
        reload_act.setToolTip("Reload")
        reload_act.triggered.connect(lambda: self.current_browser().reload())
        navbar.addAction(reload_act)

        home_act = QAction(QIcon(icons['home']), "Home", self)
        home_act.setToolTip("Home")
        home_act.triggered.connect(self.navigate_home)
        navbar.addAction(home_act)

        navbar.addSeparator()

        new_tab_act = QAction(QIcon(icons['new_tab']), "New Tab", self)
        new_tab_act.setToolTip("Open New Tab")
        new_tab_act.triggered.connect(
            lambda: self.add_new_tab(QUrl("https://duckduckgo.com"), "New Tab")
        )
        navbar.addAction(new_tab_act)

        close_tab_act = QAction(QIcon(icons['close_tab']), "Close Tab", self)
        close_tab_act.setToolTip("Close Tab")
        close_tab_act.triggered.connect(
            lambda: self.close_current_tab(self.tabs.currentIndex())
        )
        navbar.addAction(close_tab_act)

        # URL bar and progress
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setTextVisible(False)
        self.progress.setFixedWidth(120)
        navbar.addWidget(self.progress)

    def _create_tabs(self):
        self.tabs = QTabWidget(documentMode=True, tabsClosable=True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self._on_tab_changed)
        self.setCentralWidget(self.tabs)

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl("https://duckduckgo.com")
        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.loadFinished.connect(lambda _: self._record_history(browser.url()))
        browser.loadProgress.connect(self.progress.setValue)
        browser.urlChanged.connect(self._update_url_bar)
        browser.titleChanged.connect(lambda t: self.tabs.setTabText(i, t or "New Tab"))

    def current_browser(self):
        return self.tabs.currentWidget()

    def close_current_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def _on_tab_changed(self, index):
        br = self.current_browser()
        if br:
            self._update_url_bar(br.url())

    def navigate_home(self):
        self.current_browser().setUrl(QUrl("https://duckduckgo.com"))

    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        if not text.startswith(("http://", "https://")):
            text = "https://duckduckgo.com/?q=" + "+".join(text.split())
        self.current_browser().setUrl(QUrl(text))

    def _update_url_bar(self, qurl):
        self.url_bar.setText(qurl.toString())

    def _record_history(self, qurl):
        url = qurl.toString()
        if not self.history or self.history[-1] != url:
            self.history.append(url)

    def show_history_dialog(self):
        dlg = HistoryDialog(self.history, parent=self)
        dlg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
