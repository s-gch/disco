"""
    Settings dialog implementation
"""

from PySide2.QtWidgets import QDialog
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

import discogs.settings

def create_dialog(parent=None):
    ui_file = QFile('settings.ui')
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    loader.registerCustomWidget(SettingsDialog)
    win = loader.load(ui_file, parent)
    ui_file.close()

    return win

class SettingsDialog(QDialog):
    def setup(self):
        self.userName.setText(discogs.settings.instance().userName)
        self.userToken.setText(discogs.settings.instance().userToken)

    @Slot()
    def save_clicked(self):
        discogs.settings.instance().userName = self.userName.text()
        discogs.settings.instance().userToken = self.userToken.text()
        self.setResult(QDialog.Accepted)
        self.close()

    @Slot()
    def cancel_clicked(self):
        self.setResult(QDialog.Rejected)
        self.close()
