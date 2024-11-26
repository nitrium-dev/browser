from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QToolBar, QAction, QLineEdit, QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
import shared


class WidgetToolbar:
    def __init__(self, parent):
        self.parent = parent  
        self.navigation_bar = QToolBar('Navigation Toolbar')
        self.parent.addToolBar(self.navigation_bar)

#        back_button = QAction("⬅", self.parent)
#        back_button.setStatusTip('Go to previous page you visited')
#        back_button.triggered.connect(self.forward)
#        self.navigation_bar.addAction(back_button)

        refresh_button = QAction("↻", self.parent)
        refresh_button.setStatusTip('Refresh this page')
        refresh_button.triggered.connect(self.refresh_current_tab)  # Connect to the refresh method
        self.navigation_bar.addAction(refresh_button)

 #       next_button = QAction("➡", self.parent)
 #       next_button.setStatusTip('Go to next page')
 #       next_button.triggered.connect(self.parent.browser.forward)
 #       self.navigation_bar.addAction(next_button)

        self.navigation_bar.addSeparator()

        # URL BAR
        self.parent.URLBar = QLineEdit()
        self.parent.URLBar.returnPressed.connect(
            lambda: self.parent.go_to_URL(QUrl(self.parent.URLBar.text()))
        )
        self.navigation_bar.addWidget(self.parent.URLBar)
        self.navigation_bar.addSeparator()
        self.navigation_bar.addSeparator()
        self.navigation_bar.addSeparator()

        addons_icons  = QAction("🧩", self.parent)
        addons_icons.setStatusTip('Open Addons Manager')
        addons_icons.triggered.connect(lambda: self.parent.go_to_URL(QUrl('nitrium://addons')))

        settings_button = QAction("⚙️", self.parent)
        settings_button.setStatusTip('Open Settings')
        settings_button.triggered.connect(lambda: self.parent.go_to_URL(QUrl('nitrium://settings')))
        self.navigation_bar.addAction(addons_icons)
        self.navigation_bar.addAction(settings_button)

    def refresh_current_tab(self):
        current_tab = self.parent.tabs.currentWidget()  
        if current_tab:
            # Make sure current_tab is a QWebEngineView
            browser = current_tab.findChild(QWebEngineView)  
            if browser:
                browser.reload()  
    def forward(self):
        current_tab = self.parent.tabs.currentWidget()  
        if current_tab:
            # Make sure current_tab is a QWebEngineView
            browser = current_tab.findChild(QWebEngineView)  
            if browser:
                browser.forward()
