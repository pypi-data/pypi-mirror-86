"""Manabase CLI."""
import os
from pathlib import Path
from typing import Optional

import typer
from pydantic import BaseModel

from ..cache import CacheManager
from ..settings import UserSettings
from .cache import clear_cache
from .generate import generate
from .presets import app as presets


class AppContext(BaseModel):
    """CLI context object"""

    settings: UserSettings
    cache: CacheManager


app = typer.Typer()

app.add_typer(presets, name="presets")

app.command()(generate)
app.command()(clear_cache)


@app.callback()
def main(
    ctx: typer.Context,
    config: Optional[Path] = None,
    cache: Optional[Path] = None,
):
    """Landing rock solid mana bases for your decks.

    Manabase is a command-line tool that helps you generate a mana base for your
    Magic: The Gathering decks.

    It uses https://scryfall.com/ as its source of truth.
    """
    config_path: Path = config if config else UserSettings.default_path()

    if config_path.is_file():
        settings = UserSettings.from_file(config_path)
    else:
        settings = UserSettings(path=config_path)

    cache_path: Path = (
        cache if cache and cache.is_file() else CacheManager.default_path()
    )
    cache_manager = CacheManager(cache_path)

    context = AppContext(settings=settings, cache=cache_manager)

    ctx.obj = context
