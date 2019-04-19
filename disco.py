#!/usr/bin/python
"""
    Application's main module
"""

import sys

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile, Slot, Signal, Qt

import discogs.interface
import discogs.settings
import discogs.cache

import settings
from collection_model import CollectionModel

class DiscoMainWindow(QMainWindow):
    signal1 = Signal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("DISCO")
        discogs.settings.instance().set_user_name('sauresguerkchen')
        discogs.settings.instance().set_user_token('DhUbVuJtlzApTZCMWDuPHZJnudJCIrKVSopwbyKS')
        self.collection = None

    def populate(self):
        self.collection = discogs.interface.instance().get_collection(0)
        model = CollectionModel(self.collection, self.collection_list)
        self.collection_list.setModel(model)
        self.collection_list.selectRow(0)
        self.collection_list.resizeColumnsToContents()
        self.collection_list.selectionModel().selectionChanged.connect(self.selection_changed)
        self.collection_list.horizontalHeader().sortIndicatorChanged.connect(self.sort_indicator_changed)
        self.collection_list.sortByColumn(1, Qt.AscendingOrder)


### Context menu
#        self.collection_list.customContextMenuRequested.connect(self.cm)
#        self.contextMenu = QMenu(self)
#        self.contextMenu.addAction(QAction('Show details', self))
#    def cm(self, point):
#       self.contextMenu.exec_(self.collection_list.mapToGlobal(point))

    def selection_changed(self, sel, desel):
        del sel
        del desel
        for index in self.collection_list.selectionModel().selectedRows():
            self.release_title.setText(self.collection_list.model().itemdata(index.row(), CollectionModel.INDEX_TITLE))
            self.release_artist.setText(self.collection_list.model().itemdata(index.row(), CollectionModel.INDEX_ARTIST))
            self.release_year.setText(str(self.collection_list.model().itemdata(index.row(), CollectionModel.INDEX_YEAR)))
            self.release_label.setText(self.collection_list.model().itemdata(index.row(), CollectionModel.INDEX_LABEL))

            orig_pix = self.collection_list.model().itemdata(index.row(), CollectionModel.INDEX_COVER)
            scaled_pix = orig_pix.scaled(self.release_cover.size(), Qt.KeepAspectRatio)
            self.release_cover.setPixmap(scaled_pix)

    def sort_indicator_changed(self, index, order):
        del order
        if index == 0:
            self.collection_list.horizontalHeader().setSortIndicator(self.collection_list.model().sort_column,
                                                                     self.collection_list.model().sort_order)

    @Slot()
    def show_settings(self):
        settings_window = settings.create_dialog(self)
        settings_window.setup()
        settings_window.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file = QFile("disco.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    loader.registerCustomWidget(DiscoMainWindow)
    window = loader.load(ui_file)
    ui_file.close()

    window.populate()
    window.show()
    sys.exit(app.exec_())
