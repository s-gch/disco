"""
    Qt model for collection
"""

from pathlib import Path

import requests
from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex, QSize
from PySide2.QtGui import QPixmap

class CollectionModel(QAbstractTableModel):

    INDEX_TITLE = 0
    INDEX_ARTIST = 1
    INDEX_COVER = 2
    INDEX_YEAR = 3
    INDEX_LABEL = 4
    INDEX_THUMB = 5

    def __init__(self, collection, parent=None):
        super(CollectionModel, self).__init__(parent)
        self.collection = collection
        self.sort_order = Qt.AscendingOrder
        self.sort_column = 1

    def rowCount(self, parent=QModelIndex()):
        del parent
        return len(self.collection.releases)

    def columnCount(self, parent=QModelIndex()):
        del parent
        #cover, title, artist
        return 3

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() == 1:
                return self.itemdata(index.row(), CollectionModel.INDEX_TITLE)
            if index.column() == 2:
                return self.itemdata(index.row(), CollectionModel.INDEX_ARTIST)
        if role == Qt.DecorationRole:
            if index.column() == 0:
                return self.itemdata(index.row(), CollectionModel.INDEX_THUMB)
        if role == Qt.SizeHintRole:
            if index.column() == 0:
                return QSize(100, 100)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section == 0:
                    return None
                if section == 1:
                    return 'Title'
                if section == 2:
                    return 'Artist'
        return None

    def itemdata(self, datarow, index):
        item = self.collection.releases[datarow]
        if item is None:
            return None
        if index == CollectionModel.INDEX_TITLE:
            return item.title
        if index == CollectionModel.INDEX_ARTIST:
            return item.artists[0].name
        if index == CollectionModel.INDEX_COVER:
            return load_cover(item.id, item.coverUrl)
        if index == CollectionModel.INDEX_YEAR:
            return item.year
        if index == CollectionModel.INDEX_LABEL:
            return item.labels[0].name
        if index == CollectionModel.INDEX_THUMB:
            return load_thumb(item.id, item.thumbUrl)
        return None

    def sort(self, column, order=Qt.AscendingOrder):
        reverse = (order != Qt.AscendingOrder)
        if column == 1:
            self.collection.releases = sorted(self.collection.releases, key=lambda release: release.title, reverse=reverse)
            self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount()-1, self.columnCount()-1))
            self.sort_order = order
            self.sort_column = 1
        if column == 2:
            self.collection.releases = sorted(self.collection.releases, key=lambda release: release.artists[0].name, reverse=reverse)
            self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount()-1, self.columnCount()-1))
            self.sort_order = order
            self.sort_column = 1

def load_thumb(release_id, url):
    name = 'cache/thumb_{}.jpg'.format(release_id)
    path = Path(name)
    if not path.is_file():
        with open(name, mode='wb') as thumb:
            img_data = requests.get(url).content
            thumb.write(img_data)
    return QPixmap(name)

def load_cover(release_id, url):
    name = 'cache/cover_{}.jpg'.format(release_id)
    path = Path(name)
    if not path.is_file():
        with open(name, mode='wb') as cover:
            img_data = requests.get(url).content
            cover.write(img_data)
    return QPixmap(name)
