import tempfile

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap, QStandardItem, QIcon, QFont, QCloseEvent, QAction
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QMainWindow, QLabel, QHeaderView, QSizePolicy, QProxyStyle, QStyleOption, QTableView, \
    QToolBar, QStatusBar, QWidget, QVBoxLayout, QAbstractItemView


class BoxView(QMainWindow):
    sendBox2EditorSig = Signal(str, str, list)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.mainFormHandle = parent
        self.tmpDirectory = tempfile.TemporaryDirectory()

        self.setWindowTitle("Box Insertion Form")
        self.setWindowIcon(QIcon("res/icons/boxInsertionForm.png"))
        self.setMinimumSize(330, 220)
        self.resize(QSize(360, parent.height()))

        self.noticeLabel = QLabel()
        self.noticeLabel.setMinimumSize(10, 10)
        self.noticeLabel.setText("""
        <p style="text-align: center;">&nbsp;<img src="res/icons/spreadsheet.png" width="130" height="140" /></p>
        <p style="text-align: center;"><em>This is the <strong>Box Insertion Form</strong></em> ;</p>
        <p style="text-align: center;"><em>in this window you can reorder the detected </em></p>
        <p style="text-align: center;"><em>boxes,&nbsp;</em><em>and you can edit the extracted text.&nbsp;</em></p>
        <p style="text-align: center;"><em>finally, you can filter box-text pairs that you want to insert.</em></p>
       """)
        self.noticeLabel.setWordWrap(True)

        self.slate = QWidget()
        self.slateLayout = QVBoxLayout(self.slate)
        self.slateLayout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.slate)
        self.table = InsertionFormTable(parent=self)
        self.slateLayout.addWidget(self.noticeLabel)
        self.slateLayout.addWidget(self.table)
        self.noticeLabel.setVisible(True)
        self.table.setVisible(False)

        self.toolBar = QToolBar()
        self.toolBar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolBar.setAccessibleName("mainToolBar")
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QSize(30, 30))

        self.settingsAct = QAction()
        self.settingsAct.setToolTip("Insertion settings including image size and alignment")
        self.settingsAct.setStatusTip("Insertion settings (image size, alignment, ...)")
        self.settingsAct.setIcon(QIcon("res/icons/viewerSettings.png"))

        self.grabAct = QAction("Capture boxes")
        self.grabAct.setStatusTip("Capture boxes (Now you are capturing incoming boxes)")
        self.grabAct.setIcon(QIcon("res/icons/grab.png"))
        self.grabAct.triggered.connect(self.grabOrNoGrabFcn)

        self.noGrabAct = QAction("Do not capture boxes")
        self.noGrabAct.setStatusTip("Capture boxes (Now you are not capturing incoming boxes)")
        self.noGrabAct.setIcon(QIcon("res/icons/hand.png"))
        self.noGrabAct.setVisible(False)
        self.noGrabAct.triggered.connect(self.grabOrNoGrabFcn)

        self.insertAllRowsAct = QAction("Insert all rows")
        self.insertAllRowsAct.setStatusTip(self.insertAllRowsAct.text())
        self.insertAllRowsAct.setIcon(QIcon("res/icons/addRows.png"))
        self.insertAllRowsAct.triggered.connect(self.table.insertAllRows)

        self.removeAllRowsAct = QAction("Remove all rows")
        self.removeAllRowsAct.setStatusTip(self.removeAllRowsAct.text())
        self.removeAllRowsAct.setIcon(QIcon("res/icons/delRows.png"))
        self.removeAllRowsAct.triggered.connect(self.table.removeAllRows)

        self.insertSelectedAct = QAction("Insert selected row")
        self.insertSelectedAct.setStatusTip(self.insertAllRowsAct.text())
        self.insertSelectedAct.setIcon(QIcon("res/icons/addRow.png"))
        self.insertSelectedAct.triggered.connect(self.table.insertSelected)

        self.removeSelectedAct = QAction("Remove selected row")
        self.removeSelectedAct.setStatusTip(self.removeSelectedAct.text())
        self.removeSelectedAct.setIcon(QIcon("res/icons/delRow.png"))
        self.removeSelectedAct.triggered.connect(self.table.removeSelected)

        self.spacerWidget = QWidget()
        self.spacerWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.toolBar.addActions([self.settingsAct, self.grabAct, self.noGrabAct])
        self.toolBar.addWidget(self.spacerWidget)
        self.toolBar.addActions([self.removeAllRowsAct, self.insertAllRowsAct, self.removeSelectedAct,
                                 self.insertSelectedAct])

        self.insertSelectedImage = QAction()
        self.insertSelectedRow = QAction()

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.sendBox2EditorSig.connect(self.mainFormHandle.Editor.showTextFromBoxes)

    def grabOrNoGrabFcn(self):
        if self.grabAct.isVisible():
            self.grabAct.setVisible(False)
            self.noGrabAct.setVisible(True)
        else:
            self.grabAct.setVisible(True)
            self.noGrabAct.setVisible(False)


class InsertionFormTable(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        self.InsertionFormHandle = parent
        # self.setSelectionBehavior(self.SelectRows)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setShowGrid(True)
        self.setWordWrap(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setDragDropOverwriteMode(False)
        self.setAlternatingRowColors(True)
        self.setTextElideMode(Qt.ElideLeft)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Set our custom style - this draws the drop indicator across the whole row
        self.setStyle(MyStyle())

        # Set our custom model - this prevents row "shifting"
        self.model = ItemModel(parent=self)
        self.setModel(self.model)

        hHeader = self.horizontalHeader()
        hHeader.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hHeader.setSectionResizeMode(1, QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        # self.setLineWidth(3)
        # self.setMidLineWidth(3)

    def checkRowCount(self):
        row_count = self.model.rowCount()
        if row_count == 0:
            self.setVisible(False)
            self.InsertionFormHandle.noticeLabel.setVisible(True)
        else:
            self.setVisible(True)
            self.InsertionFormHandle.noticeLabel.setVisible(False)

    def addBox(self, boxAdd, text):
        if boxAdd:
            boxPixmap = QPixmap(boxAdd)
            boxPixmap.scaled(300, 150, Qt.KeepAspectRatioByExpanding)
            boxItem = QStandardItem()
            boxItem.setData(boxPixmap, Qt.DecorationRole)
            boxItem.setEditable(False)
            boxItem.setDropEnabled(False)
        else:
            boxItem = QStandardItem("(no image \nwas inserted)")

        textItem = QStandardItem(text)
        textItem.setEditable(True)
        textItem.setDropEnabled(False)

        self.model.appendRow([boxItem, textItem])

        self.checkRowCount()

    def insertAllRows(self):
        row_count = self.model.rowCount()
        for row in range(row_count):
            pixmap = self.model.item(row, 0).data(Qt.DecorationRole)
            print(type(pixmap))
            res_add = self.InsertionFormHandle.tmpDirectory.name + \
                      str(self.InsertionFormHandle.mainFormHandle.nameChanger) + ".png"
            self.InsertionFormHandle.mainFormHandle.nameChanger += 1
            pixmap.save(res_add)
            text = self.model.item(row, 1).text()
            self.InsertionFormHandle.sendBox2EditorSig.emit(res_add, text, ["center", "left"])
        self.model.clear()

        self.checkRowCount()

    def removeAllRows(self):
        self.model.clear()
        self.checkRowCount()

    def insertSelected(self):
        indices = self.selectionModel().selectedRows()
        for index in sorted(indices):
            pixmap = self.model.item(index.row(), 0).data(Qt.DecorationRole)
            if pixmap:
                res_add = self.InsertionFormHandle.tmpDirectory.name + \
                          str(self.InsertionFormHandle.mainFormHandle.nameChanger) + ".png"
                self.InsertionFormHandle.mainFormHandle.nameChanger += 1
                pixmap.save(res_add)
                text = self.model.item(index.row(), 1).text()
                self.InsertionFormHandle.sendBox2EditorSig.emit(res_add, text, ["center", "left"])
            else:
                text = self.model.item(index.row(), 1).text()
                self.InsertionFormHandle.sendBox2EditorSig.emit(str(), text, ["center", "left"])
            self.model.removeRow(index.row())

        self.checkRowCount()

    def removeSelected(self):
        indices = self.selectionModel().selectedRows()
        for index in sorted(indices):
            self.model.removeRow(index.row())
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.checkRowCount()

    def closeEvent(self, event: QCloseEvent):
        self.setVisible(False)


class ItemModel(QStandardItemModel):
    def __init__(self, parent=None):
        QStandardItemModel.__init__(self, parent)
        self.setHorizontalHeaderLabels(["Detected Box", "Extracted Text"])
        self.TableHandle = parent

    def dropMimeData(self, data, action, row, col, parent):
        """
        Always move the entire row, and don't allow column "shifting"
        """
        return super().dropMimeData(data, action, row, 0, parent)


class MyStyle(QProxyStyle):

    def drawPrimitive(self, element, option, painter, widget=None):
        """
        Draw a line across the entire row rather than just the column
        we're hovering over.  This may not always work depending on global
        style - for instance I think it won't work on OSX.
        """
        if element == self.PE_IndicatorItemViewItemDrop and not option.rect.isNull():
            option_new = QStyleOption(option)
            option_new.rect.setLeft(0)
            if widget:
                option_new.rect.setRight(widget.width())
            option = option_new
        super().drawPrimitive(element, option, painter, widget)
