import typing

import qtpy.QtCore as QtCore
import qtpy.QtWidgets as QtWidgets


class FilesTreeView(QtWidgets.QTreeView):

    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None):
        """Constructor.

        Args:
            parent: the parent widget
        """
        super(FilesTreeView, self).__init__(parent)
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)

        self._model = QtWidgets.QFileSystemModel()
        self._model.setRootPath(QtCore.QDir.rootPath())
        self._model.setFilter(QtCore.QDir.Filter.AllDirs | QtCore.QDir.Filter.NoDotAndDotDot)
        self.setModel(self._model)

        self.setSelectionMode(QtWidgets.QTreeView.SelectionMode.MultiSelection)
        self.setRootIndex(self._model.index(QtCore.QDir.rootPath()))

        for i in range(1, self._model.columnCount()):
            self.header().hideSection(i)
