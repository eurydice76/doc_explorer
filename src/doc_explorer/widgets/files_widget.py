import typing

import qtpy.QtWidgets as QtWidgets

from ..views.files_tree_view import FilesTreeView


class FilesWidget(QtWidgets.QWidget):

    def __init__(self, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            parent: the parent widget
        """
        super(FilesWidget, self).__init__(parent)

        self._build()

    def _build(self):
        """Builds the widget."""
        main_layout = QtWidgets.QVBoxLayout()

        self._files_treeview = FilesTreeView(self)
        main_layout.addWidget(self._files_treeview)

        self.setLayout(main_layout)

    @property
    def selected_directories(self) -> typing.List[str]:
        """Returns the list of the selected directories.

        Returns:
            the list of selected directories
        """
        return [self._files_treeview.model().filePath(idx) for idx in self._files_treeview.selectedIndexes()]

