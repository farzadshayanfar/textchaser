import cv2 as cv
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QImage, QPixmap, QCursor, QResizeEvent, QKeyEvent, QWheelEvent, QAction
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QMenu, QGraphicsPixmapItem, \
    QInputDialog, QGraphicsRectItem

from widgets import Worker

import project_resources


class FolderViewViewer(QGraphicsView):
    # Mouse button signals emit image scene (x, y) coordinates.
    # !!! For image (row, column) matrix indexing, row = y and column = x.
    leftMouseButtonPressed = Signal(float, float)
    rightMouseButtonPressed = Signal(float, float)
    leftMouseButtonReleased = Signal(float, float)
    rightMouseButtonReleased = Signal(float, float)
    leftMouseButtonDoubleClicked = Signal(float, float)
    rightMouseButtonDoubleClicked = Signal(float, float)

    updatePixampSig = Signal(QPixmap, QImage)

    def __init__(self, parent=None, file=None):
        QGraphicsView.__init__(self, parent)
        self.FolderViewHandle = parent
        self.threadPool = parent.threadPool
        self.tmpDirectory = parent.tmpDirectory

        self._pixmapItemHandle = QGraphicsPixmapItem()

        self._currentItem = None
        self._currentRotation = float(0)

        self.nameChanger = int(-1)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.manualBoxItem = QGraphicsRectItem()

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Context Menu
        self.contextMenu = QMenu()

        self.panAct = QAction("Pan")
        self.panAct.setIcon(QPixmap(project_resources.PanIconPath))
        self.panAct.triggered.connect(self.pan)
        self.panAct.setStatusTip("Pan across the image")

        self.zoomInAct = QAction("Zoom In")
        self.zoomInPixmap = QPixmap(project_resources.ZoomInIconPath)
        self.zoomInAct.setIcon(self.zoomInPixmap)
        self.zoomInCursor = QCursor(self.zoomInPixmap)
        self.zoomInAct.triggered.connect(self.zoomIn)
        self.zoomInAct.setStatusTip("Zoom in")

        self.zoomOutAct = QAction("Zoom Out")
        self.zoomOutPixmap = QPixmap(project_resources.ZoomOutIconPath)
        self.zoomOutAct.setIcon(self.zoomOutPixmap)
        self.zoomOutCursor = QCursor(self.zoomOutPixmap)
        self.zoomOutAct.triggered.connect(self.zoomOut)
        self.zoomOutAct.setStatusTip("Zoom out")

        self.resetZoomAct = QAction("Reset Zoom")
        self.resetZoomAct.setIcon(QPixmap(project_resources.ResetZoomIconPath))
        self.resetZoomAct.triggered.connect(self.resetZoom)
        self.resetZoomAct.setStatusTip("Reset zoom back to normal")

        self.cropAct = QAction("Crop Image")
        self.cropAct.setIcon(QPixmap(project_resources.CropIconPath))
        self.cropAct.triggered.connect(self.cropImage)
        self.cropAct.setStatusTip("Crop a rectangle of the image")
        self.scissorsPixmap = QPixmap(project_resources.ScissorsIconPath)
        self.scissorsCursor = QCursor(self.scissorsPixmap)

        self.rotateAct = QAction("Rotate Image")
        self.rotateAct.setIcon(QPixmap(project_resources.RotateIconPath))
        self.rotateAct.triggered.connect(self.rotateImage)
        self.rotateAct.setStatusTip("Rotate the image")

        self.instantExtractAct = QAction("Instant Extract")
        self.instantExtractAct.setIcon(QPixmap(project_resources.InstantExtractionIconPath))
        self.instantExtractAct.triggered.connect(self.extractSingleBox)
        self.instantExtractAct.setStatusTip("Extract text from a rectangle")

        self.grayScaleAct = QAction("Grayscale")
        self.grayScaleAct.setIcon(QPixmap(project_resources.GrayscaleIconPath))
        self.grayScaleAct.triggered.connect(self.makeItGray)
        self.grayScaleAct.setStatusTip("Grayscale the image")

        self.binarizeAct = QAction("Binarize")
        self.binarizeAct.setIcon(QPixmap(project_resources.BinarizeIconPath))
        self.binarizeAct.triggered.connect(self.makeItBinary)
        self.binarizeAct.setStatusTip("Binarize the image")

        self.colorMenu = QMenu("Set Color Space")
        self.colorMenu.setIcon(QPixmap(project_resources.ColorSpaceIconPath))
        self.colorMenu.addActions([self.grayScaleAct, self.binarizeAct])

        self.resetImageAct = QAction("Reset")
        self.resetImageAct.triggered.connect(self.resetImage)
        self.resetImageAct.setIcon(QPixmap(project_resources.ResetIconPath))
        self.resetImageAct.setStatusTip("Reset image to original (reverts all changes)")

        self.contextMenu.addActions([self.panAct, self.zoomInAct, self.zoomOutAct, self.resetZoomAct, self.cropAct,
                                     self.rotateAct, self.instantExtractAct])
        self.contextMenu.addMenu(self.colorMenu)
        self.contextMenu.addAction(self.resetImageAct)

        self.panFlag = False
        self.zoomInFlag = False
        self.zoomOutFlag = False
        self.cropFlag = False
        self.rotateFlag = False
        self.sExtractFlag = False

        self.wheelZoomPixmap = QPixmap(project_resources.MouseWheelIconPath)
        self.wheelZoomCursor = QCursor(self.wheelZoomPixmap)

        self.updatePixampSig.connect(self.setPixmapItem)

    def setItem(self, item):
        self._currentItem = item

    def item(self):
        return self._currentItem

    def originalPath(self):
        return self.item().originalPath()

    def currentImagePath(self):
        return self.item().currentPath()

    def setCurrentImagePath(self, path):
        self.item().setCurrentPath(path)

    def setCurrentRotation(self, d):
        self._currentRotation = d

    def currentRotation(self):
        return self._currentRotation

    def extractSingleBox(self):
        self.panFlag = False
        self.zoomInFlag = False
        self.zoomOutFlag = False
        self.cropFlag = False
        self.rotateFlag = False
        self.sExtractFlag = True

        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setCursor(Qt.CrossCursor)

    def pan(self):
        self.panFlag = True
        self.zoomInFlag = False
        self.zoomOutFlag = False
        self.cropFlag = False
        self.rotateFlag = False
        self.sExtractFlag = False

        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def zoomIn(self):
        self.panFlag = False
        self.zoomInFlag = True
        self.zoomOutFlag = False
        self.cropFlag = False
        self.rotateFlag = False
        self.sExtractFlag = False

        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setCursor(self.zoomInCursor)

    def zoomOut(self):
        self.panFlag = False
        self.zoomInFlag = False
        self.zoomOutFlag = True
        self.cropFlag = False
        self.rotateFlag = False
        self.sExtractFlag = False

        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setCursor(self.zoomOutCursor)

    def resetZoom(self):
        self.panFlag = False
        self.zoomInFlag = False
        self.zoomOutFlag = False
        self.cropFlag = False
        self.rotateFlag = False
        self.sExtractFlag = False

        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setCursor(Qt.ArrowCursor)
        self.updateViewer()

    def rotateImage(self):
        d, okPressed = QInputDialog.getDouble(self, "Rotate Image", "Value (from -360 to +360 degrees):",
                                              self._currentRotation, -360, 360, 3)
        if okPressed:
            worker = Worker(self.doRotateImage, d)
            self.threadPool.start(worker)

    def doRotateImage(self, d):
        self.setCurrentRotation(d)
        self.pixmapItem().setTransformOriginPoint(self.pixmapItem().pixmap().rect().center())
        self.pixmapItem().setRotation(d)
        output_add = self.tmpDirectory.name + str(self.nameChanger) + ".png"
        self.nameChanger -= 1
        # pixmap = self.grab(self.pixmapItem().boundingRect().toRect())
        # pixmap.save(output_add)
        # self.setCurrentImagePath(output_add)
        # self.updatePixampSig.emit(pixmap, QImage())
        # self.updateViewer()

    def cropImage(self):
        self.panFlag = False
        self.zoomInFlag = False
        self.zoomOutFlag = False
        self.cropFlag = True
        self.rotateFlag = False
        self.sExtractFlag = False

        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setCursor(self.scissorsCursor)

    def pixmapItem(self):
        if self._pixmapItemHandle:
            return self._pixmapItemHandle

    def setPixmapItem(self, pixmap=None, image=None):
        if image:
            pixmap = QPixmap.fromImage(image)
        self.scene.clear()
        self._pixmapItemHandle = self.scene.addPixmap(pixmap)
        self.setSceneRect(self.pixmapItem().boundingRect())  # Set scene size to image size.
        self.updateViewer()

    def loadItemImage(self, item):
        self.setItem(item)
        image = QImage(item.currentPath())
        self.updatePixampSig.emit(QPixmap(), image)
        self.updateViewer()

    def updateViewer(self):
        worker = Worker(self.fitInView, self.pixmapItem(), Qt.KeepAspectRatioByExpanding)
        self.threadPool.start(worker)

    def resize(self, arg__1: QSize):
        old_size = self.size()
        worker = Worker(self.resizeEvent, QResizeEvent(arg__1, old_size))
        self.threadPool.start(worker)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """ Maintain current zoom on resize.
        """
        self.updateViewer()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Control:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.setCursor(self.wheelZoomCursor)
        super(FolderViewViewer, self).keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.setCursor(Qt.ArrowCursor)
            self.panFlag = False
            self.zoomInFlag = False
            self.zoomOutFlag = False
            self.cropFlag = False
            self.rotateFlag = False
            self.sExtractFlag = False

        if event.key() == Qt.Key_Control:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            if self.panFlag:
                self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            elif self.zoomInFlag:
                self.setCursor(self.zoomInCursor)
            elif self.zoomOutFlag:
                self.setCursor(self.zoomOutCursor)
            elif self.cropFlag:
                self.setCursor(self.scissorsCursor)
            elif self.sExtractFlag:
                self.setCursor(Qt.CrossCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        super(FolderViewViewer, self).keyReleaseEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier and event.angleDelta().y() > 0:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.setCursor(self.wheelZoomCursor)
            self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
            self.scale(1.20, 1.20)
        elif modifiers == Qt.ControlModifier and event.angleDelta().y() < 0:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.setCursor(self.wheelZoomCursor)
            self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
            self.scale(0.83, 0.83)

    def mousePressEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        if event.button() == Qt.LeftButton and self.panFlag:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        elif event.button() == Qt.LeftButton and self.cropFlag:
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

        elif event.button() == Qt.LeftButton and self.sExtractFlag:
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

        self.leftMouseButtonPressed.emit(scenePos.x(), scenePos.y())
        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        """ Stop mouse pan or zoom mode (apply zoom if valid).
        """
        QGraphicsView.mouseReleaseEvent(self, event)
        scenePos = self.mapToScene(event.pos())
        if event.button() == Qt.LeftButton and self.cropFlag:
            worker = Worker(self.cropIt)
            self.threadPool.start(worker)

        elif event.button() == Qt.LeftButton and self.zoomInFlag:
            self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
            self.scale(1.20, 1.20)

        elif event.button() == Qt.LeftButton and self.zoomOutFlag:
            self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
            self.scale(0.83, 0.83)

        elif event.button() == Qt.LeftButton and self.sExtractFlag:
            worker = Worker(self.extractSelection)
            self.threadPool.start(worker)

        self.leftMouseButtonReleased.emit(scenePos.x(), scenePos.y())

    def cropIt(self):
        item_rect = self.pixmapItem().boundingRect()
        selection = self.scene.selectionArea().boundingRect().intersected(item_rect).toRect()
        pixmap = self.pixmapItem().pixmap().copy(selection)
        output_add = self.tmpDirectory.name + str(self.nameChanger) + ".png"
        self.nameChanger -= 1
        pixmap.save(output_add)
        self.setCurrentImagePath(output_add)
        self.updatePixampSig.emit(pixmap, QImage())

    def extractSelection(self):
        item_rect = self.pixmapItem().boundingRect()
        selection = self.scene.selectionArea().boundingRect().intersected(item_rect).toRect()
        pixmap = self.pixmapItem().pixmap().copy(selection)
        output_add = self.tmpDirectory.name + str(self.nameChanger) + ".png"
        self.nameChanger -= 1
        pixmap.save(output_add)
        self.FolderViewHandle.mainFormHandle.extractTextFromDocs(output_add, 1)

    def makeItBinary(self):
        worker = Worker(self.dotheBinarizing)
        self.threadPool.start(worker)

    def dotheBinarizing(self):
        self.setStatusTip("This image is binary")

        imgAdd = self.currentImagePath()
        outputAdd = self.tmpDirectory.name + str(self.nameChanger) + imgAdd[-5:]
        self.nameChanger -= 1
        img = cv.imread(imgAdd, 0)
        ret, th = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        cv.imwrite(outputAdd, th)
        self.setCurrentImagePath(outputAdd)
        pixmap = QPixmap(outputAdd)
        self.updatePixampSig.emit(pixmap, QImage())

    def makeItGray(self):
        worker = Worker(self.dotheGraying)
        self.threadPool.start(worker)

    def dotheGraying(self):
        self.setStatusTip("This image is gray scaled")

        imgAdd = self.currentImagePath()
        outputAdd = self.tmpDirectory.name + str(self.nameChanger) + imgAdd[-5:]
        self.nameChanger -= 1
        img = cv.imread(imgAdd)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        cv.imwrite(outputAdd, gray)
        self.setCurrentImagePath(outputAdd)
        pixmap = QPixmap(outputAdd)
        self.updatePixampSig.emit(pixmap, QImage())

    def resetImage(self):
        self.setCursor(Qt.ArrowCursor)
        pixmap = QPixmap(self.originalPath())
        self.updatePixampSig.emit(pixmap, QImage())
        self.setCurrentImagePath(self.originalPath())
        self.resetZoom()
        self.setCurrentRotation(0)

    def clear(self):
        self.updatePixampSig.emit(QPixmap(), QImage())

    def contextMenuEvent(self, event):
        self.contextMenu.exec_(event.globalPos())
