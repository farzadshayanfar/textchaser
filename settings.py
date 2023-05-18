from pathlib import Path
import json
import enum

from PySide6.QtWidgets import QApplication

import themes


class Settings:
    SettingsDirectory: Path = Path.home().joinpath("/.cache/textchaser")
    SettingsFile: Path = SettingsDirectory.joinpath("textchaser.json")
    Fields: list[str] = ["theme"]

    def __init__(self, q_application: QApplication):
        # setting or retrieving cached settings from disk
        self.SettingsDirectory.mkdir(parents=True, exist_ok=True)
        self.SettingsFile.touch(exist_ok=True)
        contents: str = self.SettingsFile.read_text(encoding="utf-8")
        self._settingsDict: dict = dict() if contents == "" else json.loads(contents)
        self.__checkSettingsDict()

        # appearance settings
        self._application = q_application
        self._theme: themes.Themes = themes.Themes.ZagrosLight

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value: themes.Themes):
        self._theme = value
        if value == themes.Themes.ZagrosLight:
            self._application.setStyleSheet(sheet=themes.zagros_light_qss)
        elif value == themes.Themes.ZagrosDark:
            pass

    def __checkSettingsDict(self):
        pass
