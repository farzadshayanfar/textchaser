from importlib.abc import Traversable
from importlib.resources import files

import res.icons
import res.pretrained_models

icons_path: Traversable = files(package=res.icons)
AppIcon: str = str(icons_path.joinpath("textchaser.png"))
TabIcon: str = str(icons_path.joinpath("image.png"))