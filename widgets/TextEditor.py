# -*- coding: utf-8 -*-

from PySide6 import QtPrintSupport
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QIcon, QContextMenuEvent, QFont, QTextCharFormat, QTextCursor, QTextListFormat, QImage, \
    QTextBlockFormat, QAction
from PySide6.QtWidgets import QToolBar, QMenu, QFrame, QTextEdit

from widgets.text_editor_objects import MarginDialog, WordCount, Find, Datetime, Table, LineSpacingDialog


class Editor(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.mainFormHandle = parent

        self.filename = ""

        self.changesSaved = True

        self.setMinimumSize(1, 1)
        self.setContentsMargins(0, 0, 5, 0)

        self.text = QTextEdit()
        self.text.setFrameShape(QFrame.Shape.NoFrame)
        # self.text.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        # Set the tab stop width to around 33 pixels which is
        # more or less 8 spaces
        # self.text.setTabStopWidth(33)
        self.setCentralWidget(self.text)
        self.docMargin = 20
        self.text.document().setDocumentMargin(self.docMargin)
        self.lineSpacing = float(2)
        block_format = QTextBlockFormat()
        block_format.setLineHeight(self.lineSpacing, 4)
        self.text.textCursor().setBlockFormat(block_format)

        self.initToolbar()
        self.initFormatbar()

        # If the cursor position changes, call the function that displays
        # the line and column number
        self.text.cursorPositionChanged.connect(self.cursorPosition)

        # We need our own context menu for tables
        self.text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.context)

        self.text.textChanged.connect(self.changed)

    def initToolbar(self):
        self.openAction = QAction(QIcon("res/icons/open.png"), "Open file", self)
        self.openAction.setStatusTip("Open existing document")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QAction(QIcon("res/icons/save.png"), "Save", self)
        self.saveAction.setStatusTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.printAction = QAction(QIcon("res/icons/print.png"), "Print document", self)
        self.printAction.setStatusTip("Print document")
        self.printAction.setShortcut("Ctrl+P")
        self.printAction.triggered.connect(self.printHandler)

        self.previewAction = QAction(QIcon("res/icons/preview.png"), "Page view", self)
        self.previewAction.setStatusTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")
        self.previewAction.triggered.connect(self.preview)

        self.findAction = QAction(QIcon("res/icons/find.png"), "Find and replace", self)
        self.findAction.setStatusTip("Find and replace words in your document")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(Find.Find(self).show)

        self.cutAction = QAction(QIcon("res/icons/cut.png"), "Cut to clipboard", self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.text.cut)

        self.copyAction = QAction(QIcon("res/icons/copy.png"), "Copy to clipboard", self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.text.copy)

        self.pasteAction = QAction(QIcon("res/icons/paste.png"), "Paste from clipboard", self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.text.paste)

        self.undoAction = QAction(QIcon("res/icons/undo.png"), "Undo last action", self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.text.undo)

        self.redoAction = QAction(QIcon("res/icons/redo.png"), "Redo last undone thing", self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.text.redo)

        dateTimeAction = QAction(QIcon("res/icons/calender.png"), "Insert current date/time", self)
        dateTimeAction.setStatusTip("Insert current date/time")
        dateTimeAction.setShortcut("Ctrl+D")
        dateTimeAction.triggered.connect(Datetime.DateTime(self).show)

        wordCountAction = QAction(QIcon("res/icons/count.png"), "See word/symbol count", self)
        wordCountAction.setStatusTip("See word/symbol count")
        wordCountAction.setShortcut("Ctrl+W")
        wordCountAction.triggered.connect(self.wordCount)

        tableAction = QAction(QIcon("res/icons/table.png"), "Insert table", self)
        tableAction.setStatusTip("Insert table")
        tableAction.setShortcut("Ctrl+T")
        tableAction.triggered.connect(Table.Table(self).show)

        imageAction = QAction(QIcon("res/icons/image.png"), "Insert image", self)
        imageAction.setStatusTip("Insert image")
        imageAction.setShortcut("Ctrl+Shift+I")
        imageAction.triggered.connect(self.insertImage)

        bulletAction = QAction(QIcon("res/icons/bullet.png"), "Insert bullet List", self)
        bulletAction.setStatusTip("Insert bullet list")
        bulletAction.setShortcut("Ctrl+Shift+B")
        bulletAction.triggered.connect(self.bulletList)

        numberedAction = QAction(QIcon("res/icons/number.png"), "Insert numbered List", self)
        numberedAction.setStatusTip("Insert numbered list")
        numberedAction.setShortcut("Ctrl+Shift+L")
        numberedAction.triggered.connect(self.numberList)

        self.toolbar = QToolBar("Options")
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)
        self.toolbar.setAccessibleName("editorOptionBar")
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolbar.setIconSize(QSize(20, 20))

        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

        self.toolbar.addAction(self.findAction)
        self.toolbar.addAction(dateTimeAction)
        self.toolbar.addAction(wordCountAction)
        self.toolbar.addAction(tableAction)
        self.toolbar.addAction(imageAction)

        self.toolbar.addAction(bulletAction)
        self.toolbar.addAction(numberedAction)

        self.addToolBarBreak()

    def initFormatbar(self):

        fontBox = QtWidgets.QFontComboBox(self)
        fontBox.setStatusTip("Set document font")
        fontBox.currentFontChanged.connect(lambda font: self.text.setCurrentFont(font))
        fontBox.setMaximumSize(195, 30)

        fontSize = QtWidgets.QSpinBox(self)
        fontSize.setStatusTip("Set font size")
        fontSize.setMaximumSize(60, 30)
        # Will display " pt" after each value
        fontSize.setSuffix(" pt")

        fontSize.valueChanged.connect(lambda size: self.text.setFontPointSize(size))

        fontSize.setValue(12)

        pageMarginAct = QAction(QIcon("res/icons/margin.png"), "Page margin", self)
        pageMarginAct.setStatusTip("Set page margins")
        pageMarginAct.triggered.connect(self.setPageMargin)

        lineSpacing = QAction(QIcon("res/icons/spacing.png"), "Line spacing", self)
        lineSpacing.setStatusTip("Set line spacing")
        lineSpacing.triggered.connect(self.setLineSpacing)

        fontColor = QAction(QIcon("res/icons/font-color.png"), "Change font color", self)
        fontColor.setStatusTip("Set font color")
        fontColor.triggered.connect(self.fontColorChanged)

        boldAction = QAction(QIcon("res/icons/bold.png"), "Bold", self)
        boldAction.setStatusTip("Make text bold")
        boldAction.triggered.connect(self.bold)

        italicAction = QAction(QIcon("res/icons/italic.png"), "Italic", self)
        italicAction.setStatusTip("Make text italic")
        italicAction.triggered.connect(self.italic)

        underlAction = QAction(QIcon("res/icons/underline.png"), "Underline", self)
        underlAction.setStatusTip("Make text underlined")
        underlAction.triggered.connect(self.underline)

        strikeAction = QAction(QIcon("res/icons/strike.png"), "Strike-out", self)
        strikeAction.setStatusTip("Strike through text")
        strikeAction.triggered.connect(self.strike)

        superAction = QAction(QIcon("res/icons/superscript.png"), "Superscript", self)
        superAction.setStatusTip("Superscript mode")
        superAction.triggered.connect(self.superScript)

        subAction = QAction(QIcon("res/icons/subscript.png"), "Subscript", self)
        subAction.setStatusTip("Subscript mode")
        subAction.triggered.connect(self.subScript)

        alignLeft = QAction(QIcon("res/icons/alignleft.png"), "Align left", self)
        alignLeft.setStatusTip("Align text left")
        alignLeft.triggered.connect(self.alignLeft)

        alignCenter = QAction(QIcon("res/icons/aligncenter.png"), "Align center", self)
        alignCenter.setStatusTip("Align text center")
        alignCenter.triggered.connect(self.alignCenter)

        alignRight = QAction(QIcon("res/icons/alignright.png"), "Align right", self)
        alignRight.setStatusTip("Align text right")
        alignRight.triggered.connect(self.alignRight)

        alignJustify = QAction(QIcon("res/icons/alignjustify.png"), "Align justify", self)
        alignJustify.setStatusTip("Align text justified")
        alignJustify.triggered.connect(self.alignJustify)

        indentAction = QAction(QIcon("res/icons/indent.png"), "Indent Area", self)
        indentAction.setStatusTip("Indent paragraph")
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.indent)

        dedentAction = QAction(QIcon("res/icons/dedent.png"), "Dedent Area", self)
        dedentAction.setStatusTip("Dedent paragraph")
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.dedent)

        backColor = QAction(QIcon("res/icons/highlight.png"), "Change background color", self)
        backColor.setStatusTip("Set text background color")
        backColor.triggered.connect(self.highlight)

        self.formatbar = self.addToolBar("Second Format Bar")
        self.formatbar.setMovable(False)
        self.formatbar.setAccessibleName("editorSecondFormatBar")
        self.formatbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.formatbar.setIconSize(QSize(20, 20))
        self.formatbar.addActions(
            [boldAction, italicAction, underlAction, strikeAction, superAction, subAction, alignLeft, alignCenter,
             alignRight, alignJustify,
             indentAction, dedentAction])
        self.addToolBarBreak()

        self.fontLayoutbar = self.addToolBar("Format")
        self.fontLayoutbar.setMovable(False)
        self.fontLayoutbar.setAccessibleName("editorFormatBar")
        self.fontLayoutbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.fontLayoutbar.setIconSize(QSize(20, 20))
        self.fontLayoutbar.addWidget(fontBox)
        self.fontLayoutbar.addWidget(fontSize)
        self.fontLayoutbar.addActions([fontColor, backColor, pageMarginAct, lineSpacing])

    def changed(self):
        self.changesSaved = False

    def closeEvent(self, event):

        if self.changesSaved:

            event.accept()

        else:

            popup = QtWidgets.QMessageBox(self)

            popup.setIcon(QtWidgets.QMessageBox.Warning)

            popup.setText("The document has been modified")

            popup.setInformativeText("Do you want to save your changes?")

            popup.setStandardButtons(QtWidgets.QMessageBox.Save |
                                     QtWidgets.QMessageBox.Cancel |
                                     QtWidgets.QMessageBox.Discard)

            popup.setDefaultButton(QtWidgets.QMessageBox.Save)

            answer = popup.exec_()

            if answer == QtWidgets.QMessageBox.Save:
                self.save()

            elif answer == QtWidgets.QMessageBox.Discard:
                event.accept()

            else:
                event.ignore()

    def context(self, pos):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table, if there is one
        table = cursor.currentTable()

        # Above will return 0 if there is no current table, in which case
        # we call the normal context menu. If there is a table, we create
        # our own context menu specific to table interaction
        if table:

            menu = QMenu(self)

            appendRowAction = QAction("Append row", self)
            appendRowAction.triggered.connect(lambda: table.appendRows(1))

            appendColAction = QAction("Append column", self)
            appendColAction.triggered.connect(lambda: table.appendColumns(1))

            removeRowAction = QAction("Remove row", self)
            removeRowAction.triggered.connect(self.removeRow)

            removeColAction = QAction("Remove column", self)
            removeColAction.triggered.connect(self.removeCol)

            insertRowAction = QAction("Insert row", self)
            insertRowAction.triggered.connect(self.insertRow)

            insertColAction = QAction("Insert column", self)
            insertColAction.triggered.connect(self.insertCol)

            mergeAction = QAction("Merge cells", self)
            mergeAction.triggered.connect(lambda: table.mergeCells(cursor))

            # Only allow merging if there is a selection
            if not cursor.hasSelection():
                mergeAction.setEnabled(False)

            splitAction = QAction("Split cells", self)

            cell = table.cellAt(cursor)

            # Only allow splitting if the current cell is larger
            # than a normal cell
            if cell.rowSpan() > 1 or cell.columnSpan() > 1:

                splitAction.triggered.connect(lambda: table.splitCell(cell.row(), cell.column(), 1, 1))

            else:
                splitAction.setEnabled(False)

            menu.addAction(appendRowAction)
            menu.addAction(appendColAction)

            menu.addSeparator()

            menu.addAction(removeRowAction)
            menu.addAction(removeColAction)

            menu.addSeparator()

            menu.addAction(insertRowAction)
            menu.addAction(insertColAction)

            menu.addSeparator()

            menu.addAction(mergeAction)
            menu.addAction(splitAction)

            # Convert the widget coordinates into global coordinates
            pos = self.mapToGlobal(pos)

            # Add pixels for the tool and formatbars, which are not included
            # in mapToGlobal(), but only if the two are currently visible and
            # not toggled by the user

            if self.toolbar.isVisible():
                pos.setY(pos.y() + 45)

            if self.fontLayoutbar.isVisible():
                pos.setY(pos.y() + 45)

            # Move the menu to the new position
            menu.move(pos)

            menu.show()

        else:

            event = QContextMenuEvent(QContextMenuEvent.Mouse, QPoint())

            self.text.contextMenuEvent(event)

    def removeRow(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's row
        table.removeRows(cell.row(), 1)

    def removeCol(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's column
        table.removeColumns(cell.column(), 1)

    def insertRow(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Insert a new row at the cell's position
        table.insertRows(cell.row(), 1)

    def insertCol(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Insert a new row at the cell's position
        table.insertColumns(cell.column(), 1)

    def toggleToolbar(self):

        state = self.toolbar.isVisible()

        # Set the visibility to its inverse
        self.toolbar.setVisible(not state)

    def toggleFormatbar(self):

        state = self.fontLayoutbar.isVisible()

        # Set the visibility to its inverse
        self.fontLayoutbar.setVisible(not state)

    def open(self):

        # Get filename and show only .writer files
        # PySide6 Returns a tuple in PySide6, we only need the filename
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', ".", "(*.writer)")[0]

        if self.filename:
            with open(self.filename, "rt") as file:
                self.text.setText(file.read())

    def save(self):

        # Only open dialog if there is no filename yet
        # PySide6 Returns a tuple in PySide6, we only need the filename
        if not self.filename:
            self.filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')[0]

        if self.filename:

            # Append extension if not there yet
            if not self.filename.endswith(".writer"):
                self.filename += ".writer"

            # We just store the contents of the text file along with the
            # format in html, which Qt does in a very nice way for us
            with open(self.filename, "wt") as file:
                file.write(self.text.toHtml())

            self.changesSaved = True

    def preview(self):

        # Open preview dialog
        preview = QtPrintSupport.QPrintPreviewDialog()
        preview.setWindowIcon(QIcon("res/icons/preview.png"))
        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.text.print_(p))

        preview.exec_()

    def printHandler(self):

        # Open printing dialog
        dialog = QtPrintSupport.QPrintDialog()

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.text.document().print_(dialog.printer())

    def cursorPosition(self):

        cursor = self.text.textCursor()

        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        # self.statusbar.showMessage("Line: {} | Column: {}".format(line,col))

    def wordCount(self):

        wc = WordCount.WordCount(self)

        wc.getText()

        wc.show()

    def insertImage(self):

        # Get image file name
        # PySide6 Returns a tuple in PySide6
        filename = \
            QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image', ".", "Images (*.png *.xpm *.jpg *.bmp *.gif)")[
                0]

        if filename:

            # Create image object
            image = QImage(filename)

            # Error if unloadable
            if image.isNull():

                popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                              "Image load error",
                                              "Could not load image file!",
                                              QtWidgets.QMessageBox.Ok,
                                              self)
                popup.show()

            else:

                cursor = self.text.textCursor()

                cursor.insertImage(image, filename)

    def fontColorChanged(self):

        # Get a color from the text dialog
        color = QtWidgets.QColorDialog.getColor()

        # Set it as the new text color
        self.text.setTextColor(color)

    def highlight(self):

        color = QtWidgets.QColorDialog.getColor()

        self.text.setTextBackgroundColor(color)

    def bold(self):

        if self.text.fontWeight() == QFont.Bold:

            self.text.setFontWeight(QFont.Normal)

        else:

            self.text.setFontWeight(QFont.Bold)

    def italic(self):

        state = self.text.fontItalic()

        self.text.setFontItalic(not state)

    def underline(self):

        state = self.text.fontUnderline()

        self.text.setFontUnderline(not state)

    def strike(self):

        # Grab the text's format
        fmt = self.text.currentCharFormat()

        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())

        # And set the next char format
        self.text.setCurrentCharFormat(fmt)

    def superScript(self):

        # Grab the current format
        fmt = self.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QTextCharFormat.AlignSuperScript)

        else:

            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)

        # Set the new format
        self.text.setCurrentCharFormat(fmt)

    def subScript(self):

        # Grab the current format
        fmt = self.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QTextCharFormat.AlignSubScript)

        else:

            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)

        # Set the new format
        self.text.setCurrentCharFormat(fmt)

    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.text.setAlignment(Qt.AlignJustify)

    def indent(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's end
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QTextCursor.Up if diff > 0 else QTextCursor.Down

            # Iterate over lines (diff absolute value)
            for n in range(abs(diff) + 1):
                # Move to start of each line
                cursor.movePosition(QTextCursor.StartOfLine)

                # Insert tabbing
                cursor.insertText("\t")

                # And move back up
                cursor.movePosition(direction)

        # If there is no selection, just insert a tab
        else:

            cursor.insertText("\t")

    def handleDedent(self, cursor):

        cursor.movePosition(QTextCursor.StartOfLine)

        # Grab the current line
        line = cursor.block().text()

        # If the line starts with a tab character, delete it
        if line.startswith("\t"):

            # Delete next character
            cursor.deleteChar()

        # Otherwise, delete all spaces until a non-space character is met
        else:
            for char in line[:8]:

                if char != " ":
                    break

                cursor.deleteChar()

    def dedent(self):

        cursor = self.text.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's last line
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QTextCursor.Up if diff > 0 else QTextCursor.Down

            # Iterate over lines
            for n in range(abs(diff) + 1):
                self.handleDedent(cursor)

                # Move up
                cursor.movePosition(direction)

        else:
            self.handleDedent(cursor)

    def bulletList(self):

        cursor = self.text.textCursor()

        # Insert bulleted list
        cursor.insertList(QTextListFormat.ListDisc)

    def numberList(self):

        cursor = self.text.textCursor()

        # Insert list with numbers
        cursor.insertList(QTextListFormat.ListDecimal)

    def setLineSpacing(self):
        LineSpacingDialog.LineSpacingDialog(parent=self).show()

    def setPageMargin(self):
        MarginDialog.MarginDialog(parent=self).show()

    def showTextFromBoxes(self, res_add, res_text, alignment_list):
        if alignment_list[0] == "center":
            self.alignEditorText(Qt.AlignHCenter)
        if res_add != str():
            self.text.insertHtml("""<p style="text-align: center;"><img src=%s /></p>""" % res_add)
        if alignment_list[1] == "left":
            self.alignEditorText(Qt.AlignLeft)
        self.text.append(res_text + "\n\n")

    def alignEditorText(self, alignment):
        cursor = self.text.textCursor()
        text_format = cursor.blockFormat()
        text_format.setAlignment(alignment)
        cursor.mergeBlockFormat(text_format)
        self.text.setTextCursor(cursor)
