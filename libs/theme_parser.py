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

# Theme parser (for .theme files)

import os

class ThemeParser:
    def __init__(self, theme_path):
        self.theme_path = theme_path
        self.theme_text = open(self.theme_path, 'r').read()
    def load_theme(self):
        # Exemple : 
        for i in self.theme_text.split('\n'):
            if i.startswith('#title'):
                self.title = i.split(':')[1].strip()
            elif i.startswith('#author'):
                self.author = i.split(':')[1].strip()
            elif i.startswith('#description'):
                self.description = i.split(':')[1].strip()
            elif i.startswith('[Style]'):
                # get the rest of the file 
                self.style = self.theme_text[self.theme_text.find('[Style]')+7:]
    def get_title(self):
        return self.title
    def get_author(self):
        return self.author
    def get_description(self):
        return self.description
    def get_style(self):
        return self.style
    def get_list(self):
        lst = []
        for filename in os.listdir('addons/themes'):
            if filename.endswith('.theme'):
                theme_id = filename.split(':')[0].strip()  
                lst.append(theme_id)
        return lst
                
                            
