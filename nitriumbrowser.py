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
# Main file


from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineDownloadItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from widgets.toolbar import WidgetToolbar
from widgets.tabs import TabWidget
from PyQt5.QtWebChannel import QWebChannel

# Imports libs (inclulded)
from libs.confighandler import ConfigHandler
from libs.theme_parser import ThemeParser
from libs.history import History
from libs.extensions_manager import ExtensionsManager
from libs.hashcheck import *

import traceback
import shared
from datetime import datetime
import sys
import os
        
class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        profile = QWebEngineProfile.defaultProfile()
        self.browser = QWebEngineView()

        profile.downloadRequested.connect(self.on_download_requested)
        
        self.setCentralWidget(self.browser)

        # Init GUI
        self.tabs = TabWidget()
        self.setCentralWidget(self.tabs)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Start Page
        if CONFG.config['check_hash']:
            if os.path.exists("nitriumbrowser.exe"):
                hashchk = hash_check('nitriumbrowser.exe')
            else:
                hashchk = hash_check('nitriumbrowser.py')
        else:
            hashchk = True
        
        if hashchk:
            start_page = EXT.check_for_start_page_extension()
            if start_page:
                self.tabs.add_new_tab(QUrl(start_page), "Start Page")
            else:
                self.go_to_home()
        else:
            self.tabs.add_new_tab(QUrl('file:///addons/html/browser_hash_invalid.html'), "Invalid Hash")

        self.set_status_tip(CONFG.get_json()['product_name'] + ' v' + CONFG.get_json()['version_number'] + ' release : ' + CONFG.get_json()['version'])
        self.toolbar = WidgetToolbar(self)


    '''--- IDK HOW TO NAME THIS ---'''
    def unknowhandler(self, url):
        if url == 'nitrium://settings':
            # load the settings page
            self.tabs.add_new_tab(QUrl('file:///addons/html/settings.html'), "Settings")
            
            return True
        elif url == 'nitrium://addons':
            self.tabs.add_new_tab(QUrl('file:///addons/html/addons.html'), "Addons")
            
            return True
        return False
    def go_to_home(self):
        self.tabs.add_new_tab(QUrl('https://www.google.com/'), "Google")

    def set_status_tip(self, text):
        self.status_bar.showMessage(text)

    def go_to_URL(self, url: QUrl):
        URL_ = url.toString()
        if self.unknowhandler(URL_):
            return
        if not URL_.startswith(('https://', 'http://')):
            search_url = 'https://duckduckgo.com/?q=' + URL_
            self.go_to_URL(QUrl(search_url))  
        else:
            if url.scheme() == '':  
                url.setScheme('https://')
            if CONFG.history_save():
                HISTRY.add(url.toString())
            self.tabs.add_new_tab(url, url.toString())
            self.update_AddressBar(url)

    def update_AddressBar(self, url):
        self.URLBar.setText(url.toString())
        self.URLBar.setCursorPosition(0)
    def on_download_requested(self, download_item: QWebEngineDownloadItem):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", download_item.path())

        if file_path:
            download_item.setPath(file_path)
            self.set_status_tip('Downloading into : ' + download_item.path())
            download_item.accept()
            # at the end 
            download_item.finished.connect(self.download_status_complete)
    def download_status_complete(self):
        self.set_status_tip('Download complete')


#Launch App
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)

        # Config loading
        CONFG = ConfigHandler() 
        HISTRY = History()
        
        # Theme loading
        THEME = ThemeParser(CONFG.get_theme())
        THEME.load_theme()
        shared.THEME = THEME
        shared.STARTUP_INFO['loadtheme'] = True
        app.setStyleSheet(THEME.get_style())

        # Addons loading

        EXT = ExtensionsManager()
        EXT.loads()
        shared.EXT = EXT
        shared.STARTUP_INFO['loadedextensions'] = True

        
        app.setApplicationName(CONFG.get_json()['product_name'])
        app.setWindowIcon(QIcon("libs/nitrium.ico"))

        # Arguments parsing
        if len(sys.argv) > 1:
            if sys.argv[1] == '--debug':
                app.setApplicationName(CONFG.get_json()['product_name'] + " [DEBUG ENABLED]")
                shared.DEBUG = True

        shared.CONFIG_V = CONFG
        shared.APP = app
        
        
        window = Window()
        window.show()
        app.exec_()
    

    # Crash handling
    except Exception as e:
        # show Qt error dialog
        FIX_ = ""
        if shared.STARTUP_INFO['loadedextensions']:
            FIX_ = "Its seems that some of installed extensions are not loaded correctly, please check your extensions folder"
        elif shared.STARTUP_INFO['loadtheme']:
            FIX_ = "Its seems that the theme is not loaded correctly, please check your theme file"
        try:
            with open(f'crashs/crash-{datetime.timestamp(datetime.now())}.txt', 'w') as f:
                f.write(f"Nitrium Browser has crashed ! here a complete detailed error log : \n \n --- CRASH LOG --- \n  \n Startup Data : {shared.STARTUP_INFO} \n Time : {datetime.now()} \n Error : {e} \n \n Traceback : \n \n {traceback.format_exc()} \n --- END OF CRASH LOG --- \n \n {FIX_} \n")
        except:
            pass
        QMessageBox.critical(None, "Error", f"Nitrium Browser has crashed ! here a complete detailed error log : \n \n --- CRASH LOG --- \n  \n Startup Data : {shared.STARTUP_INFO} \n Time : {datetime.now()} \n Error : {e} \n \n Traceback : \n \n {traceback.format_exc()} \n --- END OF CRASH LOG --- \n \n {FIX_} \n saved into crashs/crash-{datetime.timestamp(datetime.now())}.txt")
