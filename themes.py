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

QPushButton[accessibleName="StatusButton"] {
font-size: 8pt;
font-style: normal;
margin: 4px;
padding: 4px;
border: 1px solid #b5b5b5;
background-color: #ededed;
border-radius: 7px;
}

QPushButton[accessibleName="StatusButton"]:hover {
background-color: #e0e0e0;
}

QPushButton[accessibleName="StatusButton"]:checked {
background-color: #c2c2c2;
}
    
QLabel[accessibleName="StatusLabel"] {
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

QLabel[accessibleName="StatusLabel"]:hover {
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

mumbleDark = """
/*
 * Mumble Dark Theme
 * https://github.com/mumble-voip/mumble-theme
 *
 * Based on MetroMumble Theme by xPoke
 * https://github.com/xPoke
 *
 * Originally forked from Flat Mumble Theme by xPaw (xpaw.ru)
 *
 * Licensed under The Do What The Fuck You Want To Public License (WTFPL)
 */
/*
 * YOU SHOULD NOT MODIFY THIS FILE
 * Edit the files in the "source" folder instead.
 * See project README
 *
 */
ApplicationPalette {
  qproperty-window: #2e2e2e;
  qproperty-windowtext: #eee;
  qproperty-windowtext_disabled: #484848;
  qproperty-base: #191919;
  qproperty-alternatebase: #2d2d2d;
  qproperty-text: #d8d8d8;
  qproperty-text_disabled: #484848;
  qproperty-tooltipbase: #191919;
  qproperty-tooltiptext: #d8d8d8;
  qproperty-tooltiptext_disabled: #484848;
  qproperty-brighttext: #FFF;
  qproperty-brighttext_disabled: #484848;
  qproperty-highlight: #298ce1;
  qproperty-highlightedtext: #FFF;
  qproperty-highlightedtext_disabled: #484848;
  qproperty-button: #444;
  qproperty-buttontext: #d8d8d8;
  qproperty-buttontext_disabled: #484848;
  qproperty-link: #39a5dd;
  qproperty-linkvisited: #39a5dd;
  qproperty-light: #1c1c1c;
  qproperty-midlight: transparent;
  qproperty-mid: #1c1c1c;
  qproperty-dark: transparent;
  qproperty-shadow: #1c1c1c;
}

QObject,
QObject::separator,
QObject::handle,
QObject::tab-bar,
QObject::tab,
QObject::section {
  font-family: "Segoe UI", Frutiger, "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue", Arial, sans-serif;
  font-size: 10pt;
  margin: 0;
  padding: 0;
  outline: 0;
  border: 0;
  selection-background-color: #298ce1;
  selection-color: #FFF;
  alternate-background-color: transparent;
  color: #eee;
  border-radius: 2px;
}

QMainWindow,
QDockWidget {
  background-color: #2e2e2e;
}

QDialog,
QWizard *,
QCalendarWidget *,
#qswPages > QObject {
  background-color: #1D1D1D;
  color: #d8d8d8;
}

QObject:disabled,
QObject::item:disabled {
  color: #484848;
}

a {
  color: #39a5dd;
  text-decoration: none;
}

QObject::separator {
  height: 4px;
  width: 4px;
}

QObject::separator:hover {
  background: #333;
}

DockTitleBar {
  font-size: 7pt;
}

QToolTip,
QWhatsThis {
  font-size: 8pt;
  min-height: 1.3em;
  border: 1px solid #888;
  border-radius: 0;
  background-color: #191919;
  color: #d8d8d8;
}

QTextBrowser,
QTextEdit {
  background-color: #191919;
  color: #d8d8d8;
  border: 1px solid #1c1c1c;
}

QToolBar {
  background-color: #2e2e2e;
  spacing: 0;
  padding: 2px;
}

QToolButton {
  border: 1px solid transparent;
  border-radius: 2px;
  padding: 1px;
  margin: 1px;
}

QToolButton:on {
  background-color: #444;
  border: 1px solid #444;
}

QToolButton:hover {
  background-color: #3e4f5e;
  border: 1px solid #3e4f5e;
}

QToolButton:pressed {
  background-color: #484848;
}

QToolBar::separator {
  background: #555;
  height: 1px;
  margin: 4px;
  width: 1px;
}

QToolBar::separator:hover {
  background: #555;
  border: 0;
}

QToolButton#qt_toolbar_ext_button {
  min-width: 8px;
  width: 8px;
  padding: 1px;
  qproperty-icon: url(skin:controls/toolbar_ext.svg);
}

QToolBar::handle:horizontal {
  image: url(skin:controls/handle_horizontal.svg);
  width: 8px;
  padding: 4px;
}

QToolBar::handle:vertical {
  image: url(skin:controls/handle_vertical.svg);
  height: 8px;
  padding: 4px;
}

QMenuBar::item {
  background-color: transparent;
  padding: 4px 12px;
}

QMenuBar::item:selected {
  background: #298ce1;
  color: #FFF;
}

QMenuBar::item:pressed {
  background: #1979ca;
  color: #FFF;
}

QMenu {
  background: #2b2b2b;
  border: 1px solid #1c1c1c;
  color: #d8d8d8;
}

QMenu::item {
  border: 1px solid transparent;
  color: #d8d8d8;
  padding: 5px 16px;
  padding-left: 25px;
  border-radius: 2px;
}

QMenu::item:selected {
  background: #3e4f5e;
  border: 1px solid #3e4f5e;
}

QMenu::item:disabled {
  border: 1px solid transparent;
  background: transparent;
}

QMenu::separator {
  background: #555;
  height: 1px;
}

QMenu::indicator {
  padding-top: 2px;
  height: 25px;
  width: 25px;
}

QPushButton {
  background-color: #444;
  border: 1px solid #444;
  color: #d8d8d8;
  font-size: 11pt;
  padding: 3px 20px;
}

QPushButton:focus {
  background-color: #3e4f5e;
}

QPushButton:hover {
  background-color: #595959;
  border-color: #555;
}

QPushButton:hover:focus {
  background-color: #485d6f;
  border-color: #485d6f;
}

QPushButton:focus {
  border-color: #3e4f5e;
}

QPushButton:pressed,
QPushButton:pressed:focus {
  background-color: #298ce1;
  border-color: #298ce1;
  color: #FFF;
}

QGroupBox,
#qwMacWarning,
#qwInlineNotice {
  background-color: #2d2d2d;
  border: 1px solid #1c1c1c;
  color: #d8d8d8;
  font-size: 11pt;
  padding: 4px;
  padding-top: 1em;
}

QGroupBox::title {
  background-color: transparent;
  margin: 6px;
  margin-left: 8px;
  margin-right: 8px;
}

QListView {
  background-color: #191919;
  border: 1px solid #1c1c1c;
}

QListView::item {
  border-radius: 2px;
  border: 1px solid transparent;
  color: #d8d8d8;
  selection-color: #d8d8d8;
  padding: 2px 4px;
}

QListView::item:hover {
  background-color: #333;
  border: 1px solid #333;
}

QListView::item:selected {
  background-color: #3b3b3b;
  border: 1px solid #3b3b3b;
}

QListView::item:selected:active {
  background-color: #3e4f5e;
  border: 1px solid #3e4f5e;
}

QTreeView {
  background-color: #191919;
  color: #d8d8d8;
  selection-background-color: #191919;
  selection-color: #d8d8d8;
  border: 1px solid #1c1c1c;
}

QTreeView::item {
  min-width: 60px;
  border: 1px solid transparent;
  border-left: 0;
  border-right: 0;
  color: #d8d8d8;
  padding: 2px 4px;
  selection-color: #d8d8d8;
  border-radius: 0;
}

QTreeView::item:first,
QTreeView::item:only-one {
  border-left: 1px solid transparent;
  border-top-left-radius: 2px;
  border-bottom-left-radius: 2px;
}

QTreeView::item:last,
QTreeView::item:only-one {
  border-right: 1px solid transparent;
  border-top-right-radius: 2px;
  border-bottom-right-radius: 2px;
}

QTreeView::item:hover,
QTreeView::item:focus {
  background-color: #333;
  border-color: #333;
}

QTreeView::item:selected {
  background-color: #3b3b3b;
  border: 1px solid #3b3b3b;
  border-right: 0;
  border-left: 0;
}

QTreeView::item:selected:first,
QTreeView::item:selected:only-one {
  border-left: 1px solid #3b3b3b;
}

QTreeView::item:selected:last,
QTreeView::item:selected:only-one {
  border-right: 1px solid #3b3b3b;
}

QTreeView::item:selected:active {
  background-color: #3e4f5e;
  border: 1px solid #3e4f5e;
  border-right: 0;
  border-left: 0;
}

QTreeView::item:selected:active:first,
QTreeView::item:selected:active:only-one {
  border-left: 1px solid #3e4f5e;
}

QTreeView::item:selected:active:last,
QTreeView::item:selected:active:only-one {
  border-right: 1px solid #3e4f5e;
}

QTreeView::branch {
  border-image: none;
  image: none;
  margin-left: 3px;
  margin-top: 1px;
  padding-left: 3px;
}

QTreeView::branch:has-children:closed {
  image: url(skin:controls/branch_closed.svg);
}

QTreeView::branch:has-children:open {
  image: url(skin:controls/branch_open.svg);
}

QHeaderView {
  border-bottom: 1px solid #1c1c1c;
  border-radius: 0;
}

QHeaderView::section {
  border: 0;
  background-color: #2d2d2d;
  color: #d8d8d8;
  padding: 4px;
  padding-left: 8px;
  padding-right: 20px;
  border-radius: 0;
}

QHeaderView::down-arrow,
QHeaderView::up-arrow {
  margin: 1px;
  top: 1px;
  right: 5px;
  width: 14px;
}

QHeaderView::down-arrow {
  image: url(skin:controls/arrow_down.svg);
}

QHeaderView::up-arrow {
  image: url(skin:controls/arrow_up.svg);
}

QTabWidget::pane {
  background-color: #2d2d2d;
  border: 1px solid #1c1c1c;
}

QTabWidget::pane:top {
  margin-top: -1px;
  border-radius: 2px;
  border-top-left-radius: 0;
}

QTabWidget::pane:bottom {
  margin-bottom: -1px;
  border-radius: 2px;
  border-bottom-left-radius: 0;
}

QTabWidget::tab-bar {
  background-color: #1D1D1D;
}

QTabBar::tab {
  color: #ccc;
  background-color: #1e1e1e;
  padding: 6px 16px;
  border-radius: 0;
  border: 1px solid #1c1c1c;
  border-right: 0;
}

QTabBar::tab:last,
QTabBar::tab:only-one {
  border-right: 1px solid #1c1c1c;
}

QTabBar::tab:hover {
  background-color: #3e4f5e;
}

QTabBar::tab:disabled {
  color: #484848;
}

QTabBar::tab:selected {
  color: #d8d8d8;
  background-color: #2d2d2d;
}

QTabBar::tab:top {
  border-bottom: 0;
  margin-bottom: 1px;
}

QTabBar::tab:bottom {
  border-top: 0;
  margin-top: 1px;
}

QTabBar::tab:top:selected {
  padding-bottom: 7px;
  margin-bottom: 0;
}

QTabBar::tab:bottom:selected {
  padding-top: 7px;
  margin-top: 0;
}

QTabBar::tab:top:first,
QTabBar::tab:top:only-one {
  border-top-left-radius: 2px;
}

QTabBar::tab:top:last,
QTabBar::tab:top:only-one {
  border-top-right-radius: 2px;
}

QTabBar::tab:bottom:first,
QTabBar::tab:bottom:only-one {
  border-bottom-left-radius: 2px;
}

QTabBar::tab:bottom:last,
QTabBar::tab:bottom:only-one {
  border-bottom-right-radius: 2px;
}

QScrollBar {
  border-radius: 0;
  font-size: 10pt;
}

QScrollBar:vertical {
  border-left: 1px solid #1c1c1c;
  width: 1em;
}

QScrollBar:horizontal {
  border-top: 1px solid #1c1c1c;
  height: 1em;
}

QScrollBar::handle {
  margin: -1px;
  background: #666;
  border: 1px solid #1c1c1c;
}

QScrollBar::handle:vertical {
  min-height: 10px;
}

QScrollBar::handle:horizontal {
  min-width: 10px;
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
  background: #2e2e2e;
  height: 0;
  width: 0;
  border-radius: 0;
  border: 0;
}

QAbstractScrollArea::corner {
  border-left: 1px solid #1c1c1c;
  border-top: 1px solid #1c1c1c;
  height: 0;
  width: 0;
  border-radius: 0;
  border-top: 1px solid #1c1c1c;
  border-left: 1px solid #1c1c1c;
  background: #191919;
}

QLineEdit,
QComboBox,
QSpinBox,
QAbstractSpinBox {
  color: #d8d8d8;
  padding: 4px;
  min-height: 1em;
}

QComboBox,
QSpinBox,
QAbstractSpinBox {
  border: 1px solid #444;
  background-color: #444;
}

QLineEdit,
QTextEdit,
QPlainTextEdit,
QSpinBox,
QAbstractSpinBox,
QComboBox:editable {
  border: 1px solid #2e2e2e;
  background-color: #191919;
}

QSpinBox,
QAbstractSpinBox {
  min-width: 2.5em;
  padding-right: 10px;
}

QPushButton:disabled,
QLineEdit:disabled,
QTextEdit:disabled,
QPlainTextEdit:disabled,
QListWidget:disabled,
QTreeWidget:disabled,
QComboBox:disabled,
QSpinBox:disabled,
QAbstractSpinBox:disabled {
  border: 1px solid transparent;
  background-color: #282828;
}

QComboBox::drop-down,
QAbstractSpinBox::drop-down,
QSpinBox::drop-down,
QDateTimeEdit::drop-down {
  background-color: #191919;
  border: 0;
  margin-left: 4px;
  margin-right: 12px;
  margin-top: 5px;
}

QComboBox::down-arrow,
QDateTimeEdit::down-arrow {
  margin-top: -2px;
  image: url(skin:controls/arrow_down.svg);
  width: 14px;
}

QComboBox::down-arrow:disabled,
QDateTimeEdit::down-arrow:disabled {
  image: url(skin:controls/arrow_down_disabled.svg);
}

QToolButton[popupMode="1"],
QToolButton[popupMode="2"],
QPushButton[popupMode="1"],
QPushButton[popupMode="2"] {
  padding-right: 14px;
}

QToolButton::menu-arrow,
QToolButton::menu-indicator,
QPushButton::menu-arrow,
QPushButton::menu-indicator {
  image: url(skin:controls/arrow_down.svg);
  subcontrol-origin: padding;
  subcontrol-position: center right;
  top: 2px;
  right: 2px;
  width: 14px;
}

QSpinBox::down-button,
QAbstractSpinBox::down-button {
  padding-right: 4px;
  image: url(skin:controls/arrow_down.svg);
  width: 14px;
  padding-bottom: 1px;
}

QSpinBox::down-button:disabled,
QAbstractSpinBox::down-button:disabled {
  image: url(skin:controls/arrow_down_disabled.svg);
}

QSpinBox::up-button,
QAbstractSpinBox::up-button {
  padding-right: 4px;
  image: url(skin:controls/arrow_up.svg);
  width: 14px;
  padding-top: 1px;
}

QSpinBox::up-button:disabled,
QAbstractSpinBox::up-button:disabled {
  image: url(skin:controls/arrow_up_disabled.svg);
}

QComboBox QAbstractItemView {
  background-color: #191919;
  border: 1px solid #1c1c1c;
  color: #d8d8d8;
  border-radius: 0;
}

QLabel,
QCheckBox,
QAbstractCheckBox,
QTreeView::indicator,
QRadioButton {
  color: #d8d8d8;
  background: transparent;
}

QCheckBox::indicator,
QTreeView::indicator {
  background-color: #444;
  border: 1px solid #444;
  height: 13px;
  width: 13px;
  margin-top: 1px;
}

QMenu::indicator {
  width: 12px;
  left: 6px;
}

QCheckBox::indicator:checked,
QMenu::indicator:checked,
QTreeView::indicator:checked {
  image: url(skin:controls/checkbox_check_dark.svg);
}

QCheckBox::indicator:disabled,
QTreeView::indicator:disabled {
  border: 1px solid #2d2d2d;
  background-color: #282828;
}

QCheckBox::indicator:checked:disabled,
QTreeView::indicator:checked:disabled {
  border: 1px solid transparent;
  image: url(skin:controls/checkbox_check_disabled.svg);
}

QRadioButton::indicator {
  background: #444;
  border: 1px solid #444;
  border-radius: 7px;
  height: 12px;
  width: 12px;
}

QTreeView::indicator {
  background: #444;
}

QRadioButton::indicator:disabled {
  background-color: #282828;
  margin: 1px;
  border: 1px solid transparent;
}

QRadioButton::indicator:checked {
  image: url(skin:controls/radio_check_dark.svg);
}

QRadioButton::indicator:checked:disabled {
  image: url(skin:controls/radio_check_disabled.svg);
}

QSlider::groove {
  background: #393939;
  border: 1px solid #393939;
  border-radius: 2px;
  font-size: 3pt;
}

QSlider::groove:horizontal {
  height: 0.8em;
}

QSlider::groove:vertical {
  width: 0.8em;
}

QSlider::groove:disabled,
QSlider::sub-page:disabled {
  background: #282828;
  border: 1px solid transparent;
  border-radius: 2px;
}

QSlider::sub-page {
  background: #486d8d;
  border: 1px solid #486d8d;
  border-radius: 2px;
}

QSlider::handle {
  background: #777;
  border: 1px solid #222;
  border-radius: 3px;
  font-size: 4pt;
}

QSlider::handle:horizontal {
  margin: -5px -1px;
  width: 4.5em;
}

QSlider::handle:vertical {
  margin: -1px -5px;
  height: 4.5em;
}

QSlider::handle:focus {
  background-color: #6d96ba;
  border-color: #226;
}

QSlider::handle:hover {
  background-color: #999;
}

QSlider::handle:pressed {
  background-color: #bbb;
  border-color: #222;
}

QSlider::handle:disabled {
  background-color: #282828;
  border: 1px solid #282828;
}

QCheckBox::indicator:focus,
QTreeView::indicator:focus,
QRadioButton::indicator:focus,
QComboBox:focus {
  background-color: #3e4f5e;
}

QCheckBox::indicator:focus:hover,
QTreeView::indicator:focus:hover,
QRadioButton::indicator:focus:hover,
QComboBox:focus:hover {
  background-color: #485d6f;
  border-color: #485d6f;
}

QCheckBox::indicator:hover,
QTreeView::indicator:hover,
QRadioButton::indicator:hover,
QComboBox:hover {
  background-color: #595959;
  border-color: #555;
}

QLineEdit:focus,
QSpinBox:focus,
QAbstractSpinBox:focus,
QComboBox:editable:focus {
  background-color: #191919;
}

QLineEdit:focus:hover,
QSpinBox:focus:hover,
QAbstractSpinBox:focus:hover,
QComboBox:editable:focus:hover {
  border-color: #485d6f;
}

QLineEdit:hover,
QSpinBox:hover,
QAbstractSpinBox:hover,
QComboBox:editable:hover {
  background-color: #191919;
  border-color: #555;
}

QCheckBox::indicator:focus,
QTreeView::indicator:focus,
QRadioButton::indicator:focus,
QComboBox:focus,
QLineEdit:focus,
QTextEdit:focus,
QPlainTextEdit:focus,
QSpinBox:focus,
QAbstractSpinBox:focus,
QComboBox:editable:focus {
  border-color: #3e4f5e;
}

QFontDialog {
  min-width: 32em;
  min-height: 24em;
}

QColorDialog QColorLuminancePicker {
  background-color: transparent;
}

QMessageBox,
QDialogButtonBox {
  dialogbuttonbox-buttons-have-icons: 0;
}

/* Mumble Specifics */
LogTextBrowser,
#qdsChat {
  margin: 0 2px;
  min-height: 120px;
  min-width: 40px;
  border-color: #1c1c1c;
}

UserView {
  margin: 0 2px;
  min-height: 120px;
  min-width: 40px;
}

UserView::item {
  padding: 0;
  padding-top: -1px;
}

#qdwChat > QTextEdit {
  padding: -2px;
  margin: 0 2px;
  margin-bottom: 2px;
  font-size: 10pt;
}

#qtIconToolbar QComboBox {
  font-size: 8pt;
}

.log-time {
  background-color: transparent;
  color: #95a5a6;
  font-size: 9pt;
}

.log-server {
  background-color: transparent;
  color: #F9655D;
  font-weight: bold;
}

.log-channel {
  background-color: transparent;
  color: #e67e22;
  font-weight: bold;
}

.log-privilege {
  background-color: transparent;
  color: #c0392b;
  font-weight: bold;
}

.log-target {
  background-color: transparent;
  color: #27ae60;
  font-weight: bold;
}

.log-source {
  background-color: transparent;
  color: #27ae60;
  font-weight: bold;
}

QListView#qlwIcons {
  padding: 0;
  background-color: transparent;
  border: 0;
  font-size: 11pt;
  min-width: 165%;
  margin-left: 4px;
  margin-top: 12px;
}

QListView#qlwIcons::item {
  margin-bottom: 1px;
  padding: 5px 7px;
}

QListView#qlwIcons::item:hover {
  border-color: #333;
  background-color: #333;
}

QListView#qlwIcons::item:selected {
  background-color: #444;
  border: 1px solid #444;
}

QListView#qlwIcons::item:focus {
  background-color: #3e4f5e;
  border: 1px solid #3e4f5e;
}

QSlider {
  margin-left: 30px;
  margin-right: 30px;
}

#qswPages > * > * > QScrollBar {
  margin: 0;
}

#qswPages > * > QWidget {
  margin: 2px;
}

QListView::item QListWidgetItem,
QListView::item QLineEdit,
QTreeView::item QComboBox,
QTreeView::item QLineEdit {
  background: #444;
  margin: 0;
  padding-top: 0;
  padding-bottom: 0;
  padding-left: 4px;
  padding-right: 4px;
  font-size: 9pt;
}

QListView::item QListWidgetItem:hover,
QListView::item QLineEdit:hover,
QTreeView::item QComboBox:hover,
QTreeView::item QLineEdit:hover {
  background: #444;
}

AboutDialog > QTextBrowser,
AboutDialog QTextEdit {
  border: 0;
}

#qtbToolBar {
  border: 1px solid transparent;
  background: transparent;
}

#BanEditor {
  min-width: 600px;
}

#GlobalShortcutTarget {
  min-height: 600px;
}

ViewCert {
  min-height: 600px;
}

"""