import tempfile

import cv2 as cv
from PySide6.QtCore import Signal, QThreadPool, QSize, Qt
from PySide6.QtGui import QCloseEvent, QFont, QIcon, QKeySequence, QAction
from PySide6.QtWidgets import QMainWindow, QMenu, QToolBar, QSplitter, QMessageBox, QFileDialog, QApplication, \
    QToolButton, QStatusBar, QLabel, QVBoxLayout, QFrame
from pytesseract import pytesseract

import widgets
from scene_text_detectors import east_detector


class MainForm(QMainWindow):
    advSplashProgressSig: Signal = Signal(str)
    addTabSig: Signal = Signal(str)
    sendBox2EditorSig: Signal = Signal(str, str, list)
    sendBox2BIFSig: Signal = Signal(str, str)  # send text and box address to box insertion form
    sendCorners2ImageViewSig: Signal = Signal(list)
    boxedImage2ImageViewSig: Signal = Signal(str)
    advanceProgressSig: Signal = Signal(int, int)

    Title: str = "TextChaser"

    def __init__(self):
        super(MainForm, self).__init__()
        # region setting configurations
        splashScreen = widgets.SplashScreen(parent=self)
        self.advSplashProgressSig.emit("Setting Configurations ...")
        self.advSplashProgressSig.connect(splashScreen.advProgressFcn)
        self.sharedData = widgets.SharedData(mainFormHandle=self)
        # endregion setting configurations

        # region creating main form variables
        self.advSplashProgressSig.emit("Creating Main Form Variables ...")

        # loading pretrained models for text detection
        self._east = cv.dnn.readNet("res/pretrained_models/east.pb")

        self.threadPool = QThreadPool()
        self.tmpDirectory = tempfile.TemporaryDirectory()
        self.files: list = list()
        self.nameChanger: int = 0
        self.StopProcess: bool = False
        self.paddingValue: int = int()
        self.boxingDirection = widgets.BoxingOptions.Top2Bottom
        self.showWordBoxing = bool()
        self.selectedLangsList = list()
        self.defaultLanguage = str("eng")
        self.extractionLangIndex = int(23)
        self.segMode = int(3)

        # set tesseract binary path for pytesseract
        self.tesseractPath = "D:/Programs/Tesseract-OCR/tesseract.exe"
        pytesseract.tesseract_cmd = self.tesseractPath
        self.tesseractConfigString = f"-l {self.defaultLanguage} --oem 1 --psm {self.segMode}"

        self.boxDirection = str()
        self.setMinimumSize(400, 220)
        self.setWindowTitle(self.Title)
        self.setWindowIcon(self.sharedData.appIcon2)
        self._screenSize = self.screen().size()
        self.resize(self._screenSize.width() // 2, self._screenSize.height() // 2)
        self.cWidget = QFrame(self)
        self.cWidget.setAccessibleName("centralWidget")
        self.setCentralWidget(self.cWidget)
        self.cWidgetLayout = QVBoxLayout(self.cWidget)
        self.cWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.aVSplitter = QSplitter(self.cWidget)
        self.aVSplitter.setChildrenCollapsible(True)
        self.aVSplitter.setOrientation(Qt.Vertical)
        self.anHSplitter = QSplitter(self.cWidget)
        self.anHSplitter.setChildrenCollapsible(True)
        self.anHSplitter.setOrientation(Qt.Horizontal)

        self.welcomeLabel = QLabel()
        self.welcomeLabel.setMinimumSize(10, 10)
        self.welcomeLabel.setText("""
        <p style="text-align: center;">&nbsp;<img src="%s" width="150" height="160" /></p>
        <p style="text-align: center;"><em>Welcome to <strong>TextChaser</strong></em> ;</p>
        <p style="text-align: center;"><span style="background-color: #f7f7b7;">please toggle the <strong>
        Viewer Area</strong> to see the opened tabs</span></p>
        <p style="text-align: center;">Viewer__<span style="color: #003366;">Alt+I</span></p>
        <p style="text-align: center;">Editor__<span style="color: #003366;">Alt+C</span></p>
        <p style="text-align: center;">Browser__<span style="color: #003366;">Alt+N</span></p>
        """ % self.sharedData.appIconAdd2)

        self.welcomeLabel.setWordWrap(True)
        self.welcomeFont = QFont("Segoe UI", 11, 1, True)
        self.welcomeLabel.setFont(self.welcomeFont)
        self.welcomeLabel.setVisible(False)
        # endregion main form variables

        # region creating different areas
        self.advSplashProgressSig.emit("Creating Different Areas ...")
        self.FileBrowser = widgets.FileBrowser(parent=self)
        self.FileBrowser.setVisible(False)
        self.Editor = widgets.Editor(parent=self)
        self.Viewer = widgets.ViewArea(parent=self)
        self.BoxViewer = widgets.BoxView(parent=self)
        self.FolderViewer = widgets.FolderView(parent=self)
        self.FolderViewer.setVisible(False)
        # endregion creating different areas

        # region menubar
        self.advSplashProgressSig.emit("Creating Menu Bar ...")
        self.mMenuBar = self.menuBar()
        self.mMenuBar.setContextMenuPolicy(Qt.PreventContextMenu)

        self.appIconAct = QAction()
        self.appIconAct.setIcon(self.sharedData.appIcon2)
        self.appIconAct.triggered.connect(self.showAboutFcn)

        # region file menu
        self.fileMenu = QMenu("&File", self)
        self.openFileAct = QAction("Open file(s)", self)
        self.openFileAct.setStatusTip("Open image file(s)")
        self.openFileAct.setShortcut("Ctrl+O")
        self.openFileAct.setIcon(QIcon("res/icons/open.png"))
        self.openRecentFileSubMenu = QMenu("Open recent file(s)", self)
        self.openRecentFileSubMenu.setIcon(QIcon("res/icons/history2.png"))
        for file in self.sharedData.recentOpenFiles:
            action = QAction()
            action.setText(file)
            self.openRecentFileSubMenu.addAction(action)
        self.saveResAct = self.Editor.saveAction
        self.printResAct = self.Editor.printAction
        self.pageViewAct = self.Editor.previewAction
        self.closeAllTabsAct = QAction("Close all tabs")
        self.closeAllTabsAct.setStatusTip("Close all currently open tabs")
        self.closeAllTabsAct.setIcon(QIcon("res/icons/closeTabs.png"))
        self.settingsAct = QAction("Settings", self)
        self.settingsAct.setStatusTip("Show TextChaser settings")
        self.settingsAct.setIcon(QIcon("res/icons/appSettings.png"))
        self.exitAct = QAction("Exit", self)
        self.exitAct.setStatusTip("Exit the program")
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.setIcon(QIcon("res/icons/exit.png"))

        self.fileMenu.addAction(self.openFileAct)
        self.fileMenu.addMenu(self.openRecentFileSubMenu)
        self.fileMenu.addActions([self.saveResAct, self.printResAct, self.pageViewAct, self.closeAllTabsAct])
        self.fileMenu.addSeparator()
        self.fileMenu.addActions([self.settingsAct, self.exitAct])

        self.openFileAct.triggered.connect(self.openFileFcn)
        self.closeAllTabsAct.triggered.connect(self.closeAllTabsFcn)
        self.settingsAct.triggered.connect(self.showSettingsFcn)
        self.exitAct.triggered.connect(self.close)
        # endregion file menu

        # region edit menu
        self.editMenu = QMenu("&Edit", self)
        self.editorUndoAct = self.Editor.undoAction
        self.editorRedoAct = self.Editor.redoAction
        self.editorCutAct = self.Editor.cutAction
        self.editorCopyAct = self.Editor.copyAction
        self.editorPasteAct = self.Editor.pasteAction
        self.editorFindAct = self.Editor.findAction

        self.resetZoomAct = QAction("Reset Zoom")
        self.resetZoomAct.setStatusTip("Reset zoom level for current image")
        self.resetZoomAct.setIcon(QIcon("res/icons/resetZoom.png"))
        self.cropAct = QAction("Crop Image")
        self.cropAct.setStatusTip("Crop a section of current image")
        self.cropAct.setIcon(QIcon("res/icons/crop.png"))
        self.rotateAct = QAction("Rotate Image")
        self.rotateAct.setStatusTip("Rotate the current image")
        self.rotateAct.setIcon(QIcon("res/icons/rotate.png"))
        self.instantExtractAct = QAction("Instant Extract")
        self.instantExtractAct.setStatusTip("Extract a section from current image")
        self.instantExtractAct.setIcon(QIcon("res/icons/instantSelection.png"))
        self.colorMenu = QMenu("Set Color Space")
        self.colorMenu.setStatusTip("Convert color space")
        self.colorMenu.setIcon(QIcon("res/icons/colorSpace"))
        self.grayScaleAct = QAction("Grayscale")
        self.grayScaleAct.setStatusTip("Convert current image to gray space")
        self.grayScaleAct.setIcon(QIcon("res/icons/grayPalette.png"))
        self.binarizeAct = QAction("Binarize")
        self.binarizeAct.setStatusTip("Convert current image to binary space")
        self.binarizeAct.setIcon((QIcon("res/icons/binaryPalette.png")))
        self.colorMenu.addActions([self.grayScaleAct, self.binarizeAct])
        self.resetImageAct = QAction("Reset")
        self.resetImageAct.setStatusTip("Reset current image to orginal state")
        self.resetImageAct.setIcon(QIcon("res/icons/reset.png"))

        self.resetZoomAct.setDisabled(True)
        self.cropAct.setDisabled(True)
        self.rotateAct.setDisabled(True)
        self.instantExtractAct.setDisabled(True)
        self.colorMenu.setDisabled(True)
        self.resetImageAct.setDisabled(True)

        self.editMenu.addActions(
            [self.editorUndoAct, self.editorRedoAct, self.editorCopyAct, self.editorCopyAct, self.editorPasteAct,
             self.editorFindAct])
        self.editMenu.addSeparator()
        self.editMenu.addActions([self.resetZoomAct, self.rotateAct, self.cropAct, self.instantExtractAct])
        self.editMenu.addMenu(self.colorMenu)
        self.editMenu.addAction(self.resetImageAct)
        # endregion edit menu

        # region tools menu
        self.toolsMenu = QMenu("&Tools", self)
        self.languageOptionsAct = QAction("Language options")
        self.languageOptionsAct.setStatusTip("Set extraction language and page segmentation mode")
        self.languageOptionsAct.setIcon(QIcon("res/icons/lang2.png"))
        self.languageOptionsAct.triggered.connect(self.showLanguageOptions)

        self.boxingOptionsAct = QAction("Boxing options")
        self.boxingOptionsAct.setStatusTip("Set boxing direction and padding value")
        self.boxingOptionsAct.setIcon(QIcon("res/icons/boxingOptions.png"))
        self.boxingOptionsAct.triggered.connect(self.showBoxingOptions)

        self.boxingFormAct = QAction("Box view (for sorting boxes)")
        self.boxingFormAct.setStatusTip("Show box insertion form")
        self.boxingFormAct.setIcon(QIcon("res/icons/boxInsertionForm.png"))
        self.boxingFormAct.triggered.connect(self.showBoxInsertionArea)

        self.folderViewAct = QAction("Folder view (for batch processing)")
        self.folderViewAct.setStatusTip("batch processing of all the images in a directory")
        self.folderViewAct.setIcon(QIcon("res/icons/folderView.png"))
        self.folderViewAct.triggered.connect(self.showFolderView)

        self.toolsMenu.addActions([self.languageOptionsAct, self.boxingOptionsAct])
        self.toolsMenu.addSeparator()
        self.toolsMenu.addActions([self.boxingFormAct, self.folderViewAct])
        # endregion tools menu

        # region view menu
        self.viewMenu = QMenu("&View", self)
        self.toggleToolBarAct = QAction("Toolbar", self)
        self.toggleToolBarAct.setIcon(QIcon("res/icons/toolbar.png"))
        self.toggleToolBarAct.setCheckable(True)
        self.toggleToolBarAct.setChecked(True)
        self.toggleToolBarAct.triggered.connect(self.toggleToolBarFcn)

        self.toggleTreeAct = QAction("File browser")
        self.toggleTreeAct.setShortcut(QKeySequence("alt+n"))
        self.toggleTreeAct.setIcon(QIcon("res/icons/navigation.png"))
        self.toggleTreeAct.setCheckable(True)
        self.toggleTreeAct.setChecked(False)
        self.toggleTreeAct.triggered.connect(self.toggleTreeFcn)

        self.toggleViewerAct = QAction("Viewer")
        self.toggleViewerAct.setShortcut(QKeySequence("alt+i"))
        self.toggleViewerAct.setIcon(QIcon("res/icons/viewerArea.png"))
        self.toggleViewerAct.setCheckable(True)
        self.toggleViewerAct.setChecked(True)
        self.toggleViewerAct.triggered.connect(self.toggleViewerFcn)

        self.toggleEditorAct = QAction("Editor")
        self.toggleEditorAct.setShortcut(QKeySequence("alt+c"))
        self.toggleEditorAct.setIcon(QIcon("res/icons/editorArea.png"))
        self.toggleEditorAct.setCheckable(True)
        self.toggleEditorAct.setChecked(True)
        self.toggleEditorAct.triggered.connect(self.toggleEditorFcn)

        self.toggleOptionBarAct = QAction("Editor option bar")
        self.toggleOptionBarAct.setCheckable(True)
        self.toggleOptionBarAct.setChecked(True)
        self.toggleOptionBarAct.triggered.connect(self.toggleOptionBar)

        self.toggleFormatBarAct = QAction("Editor format bar")
        self.toggleFormatBarAct.setCheckable(True)
        self.toggleFormatBarAct.setChecked(True)
        self.toggleFormatBarAct.triggered.connect(self.toggleFormatBar)

        self.toggleFontBarAct = QAction("Editor font and layout bar")
        self.toggleFontBarAct.setCheckable(True)
        self.toggleFontBarAct.setChecked(True)
        self.toggleFontBarAct.triggered.connect(self.toggleFontBar)

        self.viewMenu.addActions(
            [self.toggleToolBarAct, self.toggleTreeAct, self.toggleViewerAct, self.toggleEditorAct])
        self.viewMenu.addSeparator()
        self.viewMenu.addActions([self.toggleOptionBarAct, self.toggleFormatBarAct, self.toggleFontBarAct])
        # endregion view menu

        # region help menu
        self.helpMenu = QMenu("&Help", self)
        self.manualAct = QAction("Open manual", self)
        self.manualAct.setStatusTip("Open TextChaser manual file")
        self.manualAct.setIcon(QIcon("res/icons/manual.png"))
        self.aboutAct = QAction("About", self)
        self.aboutAct.setStatusTip("Show information about the program")
        self.aboutAct.setIcon(QIcon("res/icons/about.png"))
        self.helpMenu.addActions([self.manualAct, self.aboutAct])
        self.aboutAct.triggered.connect(self.showAboutFcn)
        # endregion help menu

        self.mMenuBar.addAction(self.appIconAct)
        self.mMenuBar.addMenu(self.fileMenu)
        self.mMenuBar.addMenu(self.editMenu)
        self.mMenuBar.addMenu(self.toolsMenu)
        self.mMenuBar.addMenu(self.viewMenu)
        self.mMenuBar.addMenu(self.helpMenu)
        self.mMenuBar.addSeparator()
        # endregion menubar

        # region toolbar
        self.advSplashProgressSig.emit("Creating Tool Bar ...")

        self.toolbar = QToolBar("Main Toolbar", self)
        self.toolbar.setAccessibleName("mainToolBar")
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolbar.setIconSize(QSize(27, 27))
        self.toolbar.setMovable(False)

        self.viewToolBtn = QToolButton(self)
        self.viewToolBtn.setToolTip("Show or hide areas")
        self.viewToolBtn.setStatusTip("Toggle visiblity for specific areas")
        self.viewToolBtn.setIcon(QIcon("res/icons/viewOptions.png"))
        self.viewToolBtn.addActions(
            [self.toggleToolBarAct, self.toggleTreeAct,
             self.toggleViewerAct, self.toggleEditorAct,
             self.toggleOptionBarAct, self.toggleFormatBarAct,
             self.toggleFontBarAct])
        # self.viewToolBtn.setMenu(self.toggleAreaSubMenu)
        self.viewToolBtn.setPopupMode(QToolButton.MenuButtonPopup)
        self.viewToolBtn.clicked.connect(lambda: self.viewToolBtn.showMenu())

        self.startAct = QAction("Step start")
        self.startAct.setStatusTip("Start extraction process")
        self.startAct.setIcon(QIcon("res/icons/start.png"))
        self.startAct.triggered.connect(self.startProcess)

        self.detectionModBtn = widgets.SwitchButton()
        self.detectionModBtn.setStatusTip("Extraction mode: Scene or Document")

        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        self.toolbar.addActions([self.openFileAct, self.saveResAct, self.printResAct, self.pageViewAct])
        self.toolbar.addWidget(self.viewToolBtn)
        self.toolbar.addAction(self.closeAllTabsAct)
        self.toolbar.addSeparator()
        self.toolbar.addActions([self.languageOptionsAct, self.boxingOptionsAct, self.BoxViewer.grabAct,
                                 self.BoxViewer.noGrabAct])
        self.toolbar.addWidget(self.detectionModBtn)
        self.toolbar.addAction(self.startAct)

        # endregion toolbar

        # region statusbar
        self.advSplashProgressSig.emit("Creating Status Bar ...")

        self.statusbar = QStatusBar()
        self.statusbar.setMaximumHeight(38)
        self.statusbar.setContentsMargins(0, 0, 0, 0)
        self.setStatusBar(self.statusbar)
        self.treeStatusBtn = widgets.StatusButton("Browser")
        self.treeStatusBtn.setIcon(self.toggleTreeAct.icon())
        self.treeStatusBtn.setChecked(False)
        self.viewerStatusBtn = widgets.StatusButton("Viewer")
        self.viewerStatusBtn.setIcon(self.toggleViewerAct.icon())
        self.viewerStatusBtn.setChecked(True)
        self.editorStatusBtn = widgets.StatusButton("Editor")
        self.editorStatusBtn.setIcon(self.toggleEditorAct.icon())
        self.editorStatusBtn.setChecked(True)
        self.progressbar = widgets.ProgressBar(self)
        self.progressbar.setVisible(False)

        self.statusbar.addPermanentWidget(self.progressbar)
        self.statusbar.addPermanentWidget(self.treeStatusBtn)
        self.statusbar.addPermanentWidget(self.viewerStatusBtn)
        self.statusbar.addPermanentWidget(self.editorStatusBtn)

        self.treeStatusBtn.clicked.connect(self.toggleTreeFcn)
        self.viewerStatusBtn.clicked.connect(self.toggleViewerFcn)
        self.editorStatusBtn.clicked.connect(self.toggleEditorFcn)
        # endregion toolbar

        # region laying out
        self.advSplashProgressSig.emit("Managing Layout ...")

        self.anHSplitter.addWidget(self.FileBrowser)
        self.anHSplitter.addWidget(self.welcomeLabel)
        self.anHSplitter.addWidget(self.Viewer)
        self.anHSplitter.addWidget(self.Editor)
        self.anHSplitter.setSizes([100, 100, 200, 200])
        self.cWidgetLayout.addWidget(self.anHSplitter)
        # endregion laying out

        # region signals

        self.addTabSig.connect(self.Viewer.addTab)
        self.sendBox2EditorSig.connect(self.Editor.showTextFromBoxes)
        self.sendBox2BIFSig.connect(self.BoxViewer.table.addBox)
        self.advanceProgressSig.connect(self.progressbar.advance)
        # endregion signals

        self.advSplashProgressSig.emit("Binding Methods ...")
        splashScreen.close()

    # region methods

    def showLanguageOptions(self):
        widgets.LanguageOptions(parent=self).show()

    def showBoxingOptions(self):
        widgets.BoxingOptions(parent=self).show()

    def showFolderView(self):
        if not self.FolderViewer.isVisible():
            self.FolderViewer.setVisible(True)
        elif self.FolderViewer.isMinimized():
            self.FolderViewer.setWindowState(Qt.WindowNoState)
        else:
            self.FolderViewer.move(self.xc, self.yc)

    def showBoxInsertionArea(self):
        if not self.BoxViewer.isVisible():
            self.BoxViewer.setVisible(True)
        elif self.BoxViewer.isMinimized():
            self.BoxViewer.setWindowState(Qt.WindowNoState)
            self.BoxViewer.move(self.xc, self.yc)
        else:
            self.BoxViewer.activateWindow()

    def updateImageViewHandles(self, image_view):
        pass

    def openFileFcn(self):
        files = QFileDialog.getOpenFileNames(self, caption="Open Image File(s)", dir=".",
                                             filter="Image Files (*.png *.jpg *bmp *.tif)")[0]

        if not files:
            return

        file_length = len(files)
        tab_count = self.Viewer.tabWidget.count()
        if (file_length + tab_count > 30) or tab_count > 30:
            QMessageBox.information(self, "Info", "You can only have 30 files open at the same time.")
        elif file_length != 0:
            worker = widgets.Worker(self.showImages, files)
            self.threadPool.start(worker)
        else:
            pass

    def showImages(self, files):
        self.Viewer.tabWidget.setVisible(True)
        self.Viewer.welcomeLabel.setVisible(False)

        if isinstance(files, str):
            self.addTabSig.emit(files)
        else:
            files = [file.lower() for file in files]
            for file in files:
                self.addTabSig.emit(file)

    def closeAllTabsFcn(self):
        self.Viewer.closeAllTabs()

    def toggleToolBarFcn(self):
        if self.toolbar.isVisible():
            self.toolbar.setVisible(False)
        else:
            self.toolbar.setVisible(True)

    def toggleTreeFcn(self):
        if self.FileBrowser.isVisible():
            self.FileBrowser.setVisible(False)
            self.toggleTreeAct.setChecked(False)
            self.treeStatusBtn.setChecked(False)
            self.Viewer.vlayout.setContentsMargins(5, 0, 0, 0)
        else:
            self.FileBrowser.setVisible(True)
            self.toggleTreeAct.setChecked(True)
            self.treeStatusBtn.setChecked(True)
            self.Viewer.vlayout.setContentsMargins(0, 0, 0, 0)

    def toggleViewerFcn(self):
        if self.Viewer.isVisible():
            self.Viewer.setVisible(False)
            self.viewerStatusBtn.setChecked(False)
            self.toggleViewerAct.setChecked(False)
            self.Editor.setContentsMargins(9, 0, 11, 0)
        else:
            self.Viewer.setVisible(True)
            self.viewerStatusBtn.setChecked(True)
            self.toggleViewerAct.setChecked(True)
            self.welcomeLabel.setVisible(False)
            self.Editor.setContentsMargins(0, 0, 5, 0)

        if not self.Viewer.isVisible() and not self.Editor.isVisible():
            self.welcomeLabel.setVisible(True)

    def toggleEditorFcn(self):
        if self.Editor.isVisible():
            self.Editor.setVisible(False)
            self.editorStatusBtn.setChecked(False)
            self.toggleEditorAct.setChecked(False)
        else:
            self.Editor.setVisible(True)
            self.editorStatusBtn.setChecked(True)
            self.toggleEditorAct.setChecked(True)
            self.welcomeLabel.setVisible(False)

        if not self.Viewer.isVisible() and not self.Editor.isVisible():
            self.welcomeLabel.setVisible(True)

    def toggleOptionBar(self):
        if self.Editor.toolbar.isVisible():
            self.Editor.toolbar.setVisible(False)
            self.toggleOptionBarAct.setChecked(False)
        else:
            self.Editor.toolbar.setVisible(True)
            self.toggleOptionBarAct.setChecked(True)

    def toggleFormatBar(self):
        if self.Editor.formatbar.isVisible():
            self.Editor.formatbar.setVisible(False)
            self.toggleFormatBarAct.setChecked(False)
        else:
            self.Editor.formatbar.setVisible(True)
            self.toggleFormatBarAct.setChecked(True)

    def toggleFontBar(self):
        if self.Editor.fontLayoutbar.isVisible():
            self.Editor.fontLayoutbar.setVisible(False)
            self.toggleFontBarAct.setChecked(False)
        else:
            self.Editor.fontLayoutbar.setVisible(True)
            self.toggleFontBarAct.setChecked(True)

    def showSettingsFcn(self):
        pass

    def showAboutFcn(self):
        widgets.AboutDialog().show()

    def extractTextFromBoxes(self, file):
        self.advanceProgressSig.emit(10, 0)

        output_add = self.tmpDirectory.name + file[-5:]
        corner_list = east_detector.startDet(file, self._east, output_add)
        self.boxedImage2ImageViewSig.connect(self.Viewer.currentImageView.loadImageFromFile)
        self.boxedImage2ImageViewSig.emit(output_add)
        if not corner_list:
            return
        else:
            self.advanceProgressSig.emit(10, 0)
            directedBoxedImageList = self.applyDirection(corner_list, file)
            self.advanceProgressSig.emit(10, 0)
            step = self.progressbar.getStep(len(corner_list))
            for entry in directedBoxedImageList:
                res_text = pytesseract.image_to_string(entry, config=self.tesseractConfigString)
                res_add = self.tmpDirectory.name + str(self.nameChanger) + ".png"
                self.nameChanger += 1
                cv.imwrite(res_add, entry)
                self.advanceProgressSig.emit(step, 0)

                if self.BoxViewer.grabAct.isVisible():
                    self.sendBox2BIFSig.emit(res_add, res_text)

                else:
                    self.sendBox2EditorSig.emit(res_add, res_text, ["center", "center"])

        self.advanceProgressSig.emit(25, 1)

    def applyDirection(self, corner_list, original_file):
        original_image = cv.imread(original_file)
        directed_box_list = list()
        new_corner_list = list()

        for entry in corner_list:
            row_min = min(entry[0]) - self.paddingValue
            row_max = max(entry[0]) + self.paddingValue
            col_min = min(entry[1]) - self.paddingValue
            col_max = max(entry[1]) + self.paddingValue

            if self.boxingDirection == widgets.BoxingOptions.Left2Right:
                new_corner_list.append([col_min, row_min, col_max, row_max])

            elif self.boxingDirection == widgets.BoxingOptions.Right2Left:
                new_corner_list.append([col_max, col_min, row_max, row_min])

            elif self.boxingDirection == widgets.BoxingOptions.Top2Bottom:
                new_corner_list.append([row_min, col_min, row_max, col_max])

            elif self.boxingDirection == widgets.BoxingOptions.Bottom2Top:
                new_corner_list.append([row_max, col_min, col_max, row_min])

        if self.boxingDirection == widgets.BoxingOptions.Left2Right:
            new_corner_list.sort()
            for corners in new_corner_list:
                aBoxedImage = original_image[corners[1]:corners[3], corners[0]:corners[2]]
                directed_box_list.append(aBoxedImage)

        elif self.boxingDirection == widgets.BoxingOptions.Right2Left:
            new_corner_list.sort(reverse=True)
            for corners in new_corner_list:
                aBoxedImage = original_image[corners[3]:corners[2], corners[1]:corners[0]]
                directed_box_list.append(aBoxedImage)

        elif self.boxingDirection == widgets.BoxingOptions.Top2Bottom:
            new_corner_list.sort()
            for corners in new_corner_list:
                aBoxedImage = original_image[corners[0]:corners[2], corners[1]:corners[3]]
                directed_box_list.append(aBoxedImage)

        elif self.boxingDirection == widgets.BoxingOptions.Bottom2Top:
            new_corner_list.sort(reverse=True)
            for corners in new_corner_list:
                aBoxedImage = original_image[corners[3]:corners[0], corners[1]:corners[2]]
                directed_box_list.append(aBoxedImage)

        return directed_box_list

    def extractTextFromDocs(self, img_add, send_images_too=0):
        self.advanceProgressSig.emit(20, 0)

        res = pytesseract.image_to_string(image=img_add, config=self.tesseractConfigString)

        self.advanceProgressSig.emit(25, 0)

        if not self.BoxViewer.grabAct.isVisible() and not send_images_too:
            self.sendBox2EditorSig.emit(str(), res, ["center", "left"])

        elif not self.BoxViewer.grabAct.isVisible() and send_images_too:
            self.sendBox2EditorSig.emit(img_add, res, ["center", "left"])

        elif self.BoxViewer.grabAct.isVisible() and send_images_too:
            self.sendBox2BIFSig.emit(img_add, res)

        elif self.BoxViewer.grabAct.isVisible() and not send_images_too:
            self.sendBox2BIFSig.emit(str(), res)

        self.advanceProgressSig.emit(25, 1)

    def startProcess(self):
        if self.Viewer.tabWidget.count() == 0:
            QMessageBox.information(self, "Info", "You need to first open some image file(s).")
            return

        self.progressbar.setVisible(True)
        self.advanceProgressSig.emit(25, 0)

        img_add = self.Viewer.currentImageView.currentImagePath()
        if self.detectionModBtn.isChecked():
            worker = widgets.Worker(self.extractTextFromBoxes, img_add)
            self.threadPool.start(worker)
        else:
            worker = widgets.Worker(self.extractTextFromDocs, img_add)
            self.threadPool.start(worker)

    def closeEvent(self, event: QCloseEvent):
        qassert = QMessageBox.question(self, "Assertion", "Are You Sure You Want to Quit?",
                                       QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.Yes)
        if qassert == QMessageBox.Yes:
            self.tmpDirectory.cleanup()
            self.FolderViewer.tmpDirectory.cleanup()
            self.FolderViewer.guestTempDir.cleanup()

            self.deleteLater()
            event.accept()
            QApplication.quit()
        elif qassert == QMessageBox.No:
            event.ignore()

    # endregion methods