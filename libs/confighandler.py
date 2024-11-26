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

# JSON configuration handler (idk why i made this)

import json

class ConfigHandler:
    def __init__(self):
        self.config = json.load(open('config.json'))
        self.theme = self.config['theme']

    def get_theme(self):
        return self.theme
    def get_json(self):
        return self.config
    def history_save(self):
        return self.config['history_save']