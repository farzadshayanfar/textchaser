from importlib.abc import Traversable
from importlib.resources import files

import res.icons
import res.pretrained_models


models_path: Traversable = files(package=res.pretrained_models)
icons_path: Traversable = files(package=res.icons)

EastModelPath: str = str(models_path.joinpath("east.pb"))

AppIconPath: str = str(icons_path.joinpath("textchaser.png"))
AboutIconPath: str = str(icons_path.joinpath("about.png"))
ManualIconPath: str = str(icons_path.joinpath("manual.png"))
SettingsIconPath: str = str(icons_path.joinpath("app_settings.png"))
ExitIconPath: str = str(icons_path.joinpath("exit.png"))
TabIconPath: str = str(icons_path.joinpath("image.png"))
CloseTabsIconPath: str = str(icons_path.joinpath("close_tabs.png"))
SplashScreenImagePath: str = str(icons_path.joinpath("splashscreen_background.png"))
OpenFileIconPath: str = str(icons_path.joinpath("open_file.png"))
FileHistoryIconPath: str = str(icons_path.joinpath("file_history.png"))
ResetZoomIconPath: str = str(icons_path.joinpath("reset_zoom.png"))
PanIconPath: str = str(icons_path.joinpath("pan.png"))
ZoomInIconPath: str = str(icons_path.joinpath("zoom_in.png"))
ZoomOutIconPath: str = str(icons_path.joinpath("zoom_out.png"))
MouseWheelIconPath: str = str(icons_path.joinpath("mouse_wheel.png"))
CropIconPath: str = str(icons_path.joinpath("crop.png"))
ScissorsIconPath: str = str(icons_path.joinpath("scissors.png"))
RotateIconPath: str = str(icons_path.joinpath("rotate.png"))
InstantExtractionIconPath: str = str(icons_path.joinpath("instant_extraction.png"))
NavigationIconPath: str = str(icons_path.joinpath("navigation.png"))
ToolbarIconPath: str = str(icons_path.joinpath("toolbar.png"))
FolderViewIconPath: str = str(icons_path.joinpath("folder_view.png"))
ViewerAreaIconPath: str = str(icons_path.joinpath("viewer_area.png"))
EditorAreaIconPath: str = str(icons_path.joinpath("editor_area.png"))
BoxInsertionFormIconPath: str = str(icons_path.joinpath("box_insertion_form.png"))
GrayscaleIconPath: str = str(icons_path.joinpath("grayscale.png"))
BinarizeIconPath: str = str(icons_path.joinpath("binarize.png"))
ColorSpaceIconPath: str = str(icons_path.joinpath("color_space.png"))
ResetIconPath: str = str(icons_path.joinpath("reset.png"))
LanguageIconPath: str = str(icons_path.joinpath("lang.png"))
BoxingOptionsIconPath: str = str(icons_path.joinpath("boxing_options.png"))
ViewOptionsIconPath: str = str(icons_path.joinpath("view_options.png"))
StartIconPath: str = str(icons_path.joinpath("start.png"))
