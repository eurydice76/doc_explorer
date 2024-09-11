import glob
import os
import pathlib
import re
import sys
import typing

import qtpy.QtCore as QtCore
import qtpy.QtGui as QtGui
import qtpy.QtWidgets as QtWidgets

from ..__pkginfo__ import __version__
from ..kernel.search import search_engines
from ..widgets.files_widget import FilesWidget
from ..widgets.search_widget import SearchWidget


class MainView(QtWidgets.QMainWindow):

    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None):
        """Constructor.

        Args:
            parent: the parent widget
        """
        super(MainView, self).__init__(parent)

        self._build()

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose, True)

        self.setWindowTitle(f"doc_explorer ({__version__})")

    def _build(self):
        """Builds the main window."""
        self._tab_widget = QtWidgets.QTabWidget(self)
        self._tab_widget.setTabsClosable(True)
        self.setCentralWidget(self._tab_widget)

        self._files_dock_widget = QtWidgets.QDockWidget("Files", self)
        self._files_dock_widget.setAllowedAreas(
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea
        )
        self._files_dock_widget.setFloating(False)
        self._files_dock_widget.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetFloatable
            | QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable
        )
        self._files_widget = FilesWidget(self)
        self._files_dock_widget.setWidget(self._files_widget)

        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self._files_dock_widget
        )

        self._search_dock_widget = QtWidgets.QDockWidget("Search", self)
        self._search_dock_widget.setAllowedAreas(
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea
        )
        self._search_dock_widget.setFloating(False)
        self._search_dock_widget.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetFloatable
            | QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable
        )
        self._search_widget = SearchWidget(self)
        self._search_dock_widget.setWidget(self._search_widget)

        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self._search_dock_widget
        )

        self.resize(1000, 1000)

        self._files_dock_widget.setStyleSheet("QDockWidget::title"
                           "{"
                           "background : lightblue;"
                           "}"
                           )

        self._search_dock_widget.setStyleSheet("QDockWidget::title"
                           "{"
                           "background : lightblue;"
                           "}"
                           )

        self._search_widget.signal_run.connect(self.on_run)

    def _close(self):
        """Closes the application."""
        self.deleteLater()
        sys.exit(0)

    def closeEvent(self, event: QtGui.QCloseEvent = None):
        """Handler for the close event.

        Args:
            event: the close event
        """
        self._close()

    def on_quit_application(self):
        """Quits the application."""
        choice = QtWidgets.QMessageBox.question(
            self,
            "Quit",
            "Do you really want to quit?",
            QtWidgets.QMessageBox.StandardButton.Yes |
            QtWidgets.QMessageBox.StandardButton.No)
        if choice == QtWidgets.QMessageBox.StandardButton.Yes:
            self._close()

    def on_run(self):
        """Runs a new search."""
        selected_directories = self._files_widget.selected_directories
        if not selected_directories:
            return

        search_text = self._search_widget.search_text
        if not search_text:
            return

        ignore_case = re.IGNORECASE if self._search_widget.ignore_case else 0

        hits = []
        for directory in selected_directories:
            for f in pathlib.Path(directory).rglob("*.*"):
                ext = os.path.splitext(f)[1]
                if ext in search_engines:
                    try:
                        if search_engines[ext](search_text, f, ignore_case):
                            hits.append(str(f))
                    except PermissionError:
                        continue

        print(hits)
