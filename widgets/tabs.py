"""
Nitrium Web Browser - A simple and lightweight web browser built with PyQt5.

Copyright (c) 2024 EletrixTime

This program is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).
You are free to:
  - Share: Copy and redistribute the material in any medium or format.
  - Adapt: Remix, transform, and build upon the material.

Under the following terms:
  - Attribution: You must give appropriate credit, provide a link to the license, and indicate if changes were made.
  - NonCommercial: You may not use the material for commercial purposes.
  - ShareAlike: If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

Full license details are available at:
https://creativecommons.org/licenses/by-nc-sa/4.0/

DISCLAIMER:
This software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

Enjoy using Nitrium! Feedback and contributions are welcome.
"""

from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl
from libs import theme_parser
import shared


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

    def add_new_tab(self, url: QUrl, title="Nouvel Onglet"):
        new_tab = QWidget()
        layout = QVBoxLayout()
        browser = QWebEngineView()
        browser.setUrl(url)
        browser.page().settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        
        # TODO : make a better way to do this
        if url.toString().startswith('file://'):
            THEMES_LST = shared.THEME.get_list()
            browser.loadFinished.connect(lambda: browser.page().runJavaScript(f'THEME = "{THEMES_LST}";core();'))
        
        layout.addWidget(browser)
        new_tab.setLayout(layout)
        index = self.addTab(new_tab, title)
        self.setCurrentIndex(index)
        shared.TABS.append(browser)
        # check for injection
        browser.titleChanged.connect(lambda title: self.setTabText(index, title))

        inject_js = shared.EXT.check_for_inject_code_js(url=url)
        if inject_js is not None:
            for script in inject_js:
                try:
                    with open(script["path"], 'r') as file:
                        k = file.read()
                    browser.loadFinished.connect(lambda: browser.page().runJavaScript(k))
                except Exception as e:
                    pass

    def close_tab(self, index):
        if self.count() > 1:
            shared.TABS.pop(index)
            self.removeTab(index)

    def reload(self):
        self.current_tab().reload()

    def current_tab(self):
        return self.widget(self.currentIndex())
