"""Generation presets management."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Optional

import yaml
from appdirs import user_config_dir
from pydantic import BaseModel, BaseSettings

from . import __app_name__, __version__

DEFAULT_CONFIG = __app_name__ + ".yml"


class GenerationPreset(BaseModel):
    """A `generate` command preset."""

    name: str
    filters: Optional[str] = None
    lands: Optional[int] = None
    occurrences: Optional[int] = None
    priorities: Optional[str] = None
    filler_weights: Optional[str] = None
    rocks: Optional[int] = None
    rock_filters: Optional[str] = None
    rock_priorities: Optional[str] = None
    sets: Optional[str] = None


class UserSettings(BaseSettings):
    """Application user settings."""

    # TODO: Is there any way to ignore this attribute during serialization ?
    path: Path
    presets: Dict[str, GenerationPreset] = {}
    active: Optional[str] = None

    class Config:  # pylint: disable=missing-class-docstring
        env_prefix = __app_name__ + "_"

    @classmethod
    def from_file(cls, path: Path) -> UserSettings:
        """Read settings from a YAML file."""
        with open(path) as handle:
            data = yaml.safe_load(handle)

        data["path"] = path
        return cls(**data)

    @staticmethod
    def default_path() -> Path:
        """Return the default configuration path."""
        return Path(user_config_dir(__app_name__, version=__version__)) / DEFAULT_CONFIG

    def save(self, path: Optional[Path] = None):
        """Save settings to file.

        If no file path is provided, saves to `UserSettings.default_path`.
        """
        path = path or self.path

        if not path.parent.is_dir():
            os.makedirs(path.parent)

        data = self.dict()
        data.pop("path")

        with open(path, "w") as handle:
            yaml.safe_dump(data, handle)
