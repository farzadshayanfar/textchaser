import enum


class Themes(enum.Enum):
    ZagrosLight = 0
    ZagrosDark = 1


zagros_light_qss = """
QWidget {
}

QWidget[accessibleName="centralWidget"] {
background-color: #ebebeb;
}

QMainWindow {
background-color: #ebebeb;
}

QMenuBar {
spacing: 5px;
padding: 5px 0px 0px 0px;
font-size: 11pt;
border: 0px;
margin-left: 5px;
}

QMenu {
padding: 5px 0px 5px 12px;
}

QToolBar::separator{
background-color: black;
height: 1px;
margin: 4px;
width: 1px;
}

QToolBar[accessibleName="mainToolBar"] {
padding: 2px 0px 3px 10px;
margin: 2px 0px 2px 0px;
spacing: 6px;
border: 0px;
}

QToolBar[accessibleName="editorFormatBar"] {
margin-left: 1px;
padding-left: 3px;
spacing: 8px;
border: 0px;
}

QToolBar[accessibleName="editorSecondFormatBar"] {
margin-left: 1px;
padding-left: 2px;
spacing: 8px;
border: 0px;
}

QToolBar[accessibleName="editorOptionBar"] {
margin-left: 1px;
padding-left: 2px;
spacing: 8px;
border: 0px;
}
        
QTextEdit {
background-color: white;
margin: 5px 0px 0px 3px;
border: 0px;
}

QTabWidget::pane {
    border: 1px solid #757575;
    background: white;
    margin-top: 0px;
}

QTabBar::tab {
    border: 1px solid #757575;
    border-bottom: 0px;
    icon-size: 25px;
    padding: 2px 0px 2px 2x;
    width: 145px;
    height: 25px;
}

QTabBar::tab:selected {
    background: white;
}

QTabBar::tab:!selected {
    background: silver;
}

QTabBar::tab:!selected:hover {
    background: #999;
}

QSplitter {
background-color: #dcdcdc;
margin: 0px;
padding: 0px;
}

QSplitter::handle:horizontal {
    image: url(widgets/themes_graphic_files/handle_horizontal.svg);
    width: 10px;
    padding: 0px;
    margin: 0px;
}

QSplitter::handle:vertical {
    image: url(widgets/themes_graphic_files/handle_vertical.svg);
    height: 10px;
    padding: 0px;
    margin: px;
}

QSplitter::handle:pressed {
    background: #dcddde;
}

QTreeView {
font-size: 9pt;
icon-size: 20px;
border: 1px solid #757575;
}

QStatusBar {
font-size: 9pt;
}

QScrollBar {
  font-size: 8pt;
}

QScrollBar:vertical {
  border-left: 2px solid #8993b3;
  width: 9px;
}

QScrollBar:horizontal {
  border-top: 2px solid #8993b3;
  height: 9px;
}

QScrollBar::handle {
  margin: -1px;
  background: #5a6cad;
  border: 1px solid #6f7dad;
}

QScrollBar::handle:vertical {
  min-height: 12px;
}

QScrollBar::handle:horizontal {
  min-width: 12px;
}

QScrollBar::handle:hover {
  background: #888;
}

QScrollBar::left-arrow,
QScrollBar::right-arrow,
QScrollBar::up-arrow,
QScrollBar::down-arrow,
QScrollBar::sub-line,
QScrollBar::add-line,
QScrollBar::add-page,
QScrollBar::sub-page {
  background: #f0ede1;
  height: 0;
  width: 0;
  border-radius: 0;
  border: 0;
}

QAbstractScrollArea::corner {
  height: 0;
  width: 0;
  background: #f0ede1;
}

QPushButton[accessibleName="status_button"] {
font-size: 8pt;
font-style: normal;
margin: 4px;
padding: 2px;
border: 1px solid #b5b5b5;
background-color: #ededed;
border-radius: 7px;
width: 80px;
height: 20px;
}

QPushButton[accessibleName="status_button"]:hover {
background-color: #e0e0e0;
}

QPushButton[accessibleName="status_button"]:checked {
background-color: #c2c2c2;
}
    
QLabel[accessibleName="status_label"] {
font-family: "Segoe UI", "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue";
font-size: 8pt;
font-style: normal;
margin: 4px 2px 0px 0px;
padding: 2px 0px 5px 4px;
border: 1px solid #b5b5b5;
border-bottom: 0px;
background-color: #ededed;
border-radius: 5px;
}

QLabel[accessibleName="status_label"]:hover {
background-color: #e0e0e0;
}

QProgressBar {
    font-family: "Segoe UI", "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue";
    font-size: 8pt;
    font-style: normal;
    margin: 4px 2px 0px 0px;
    padding: 0px;
    border: 1px solid #b5b5b5;
    background-color: #ededed;
    border-radius: 5px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #05B8CC;
    width: 20px;
}

"""