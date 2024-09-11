import qtpy.QtCore as QtCore
import qtpy.QtWidgets as QtWidgets


class SearchWidget(QtWidgets.QWidget):

    signal_run = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            parent: the parent widget
        """
        super(SearchWidget, self).__init__(parent)

        self._build()

    def _build(self):
        """Builds the widget."""
        main_layout = QtWidgets.QVBoxLayout()

        search_text_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Text")
        search_text_layout.addWidget(label)
        self._search_text_lineedit = QtWidgets.QLineEdit()
        search_text_layout.addWidget(self._search_text_lineedit)
        main_layout.addLayout(search_text_layout)

        self._ignore_case_checkbox = QtWidgets.QCheckBox("Ignore case")
        main_layout.addWidget(self._ignore_case_checkbox)

        self._run_pushbutton = QtWidgets.QPushButton("Run")
        main_layout.addWidget(self._run_pushbutton)

        main_layout.addStretch()

        self.setLayout(main_layout)

        self._run_pushbutton.clicked.connect(self.signal_run.emit)

    @property
    def ignore_case(self) -> bool:
        """Returns whether te search should ignore case.

        Returns:
            whether te search should ignore case
        """
        return self._ignore_case_checkbox.isChecked()

    @property
    def search_text(self) -> str:
        """Returns the search text.

        Returns:
            the search text
        """
        return self._search_text_lineedit.text()