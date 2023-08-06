"""Default values of the application.

Here you can find the default filters and priority lists for both lands and rocks.
"""
from typing import List

from .colors import Color
from .filter.data import FilterAlias
from .filters.colors import BasicLandReferencedFilter, ProducedManaFilter
from .filters.composite import CompositeFilter
from .filters.lands.battle import BattleLandFilter
from .filters.lands.check import CheckLandFilter
from .filters.lands.fetch import FetchLandFilter
from .filters.lands.original import OriginalDualLandFilter
from .filters.lands.reveal import RevealLandFilter
from .filters.lands.shock import ShockLandFilter
from .filters.rocks.crystal import CrystalFilter
from .filters.rocks.obelisk import ObeliskFilter
from .filters.rocks.signet import SignetFilter
from .filters.rocks.talisman import TalismanFilter


def default_lands() -> int:
    """Return the default number of lands to generate."""
    return 37


def default_occurrences() -> int:
    """Return the default number of occurrences of cards."""
    return 1


def default_land_filters(colors: List[Color]) -> CompositeFilter:
    """Build and return default land filters."""
    return (
        ProducedManaFilter(colors=colors)
        & (
            OriginalDualLandFilter()
            | ShockLandFilter()
            | BattleLandFilter()
            | CheckLandFilter()
            | RevealLandFilter()
        )
    ) | (
        BasicLandReferencedFilter(
            colors=colors,
            exclusive=False,
            minimum_count=1,
        )
        & FetchLandFilter()
    )


def default_land_priorities() -> List[FilterAlias]:
    """Return default land priorities."""
    return [
        FilterAlias.fetch,
        FilterAlias.original,
        FilterAlias.shock,
        FilterAlias.battle,
        FilterAlias.check,
        FilterAlias.reveal,
    ]


def default_rock_filters(colors: List[Color]) -> CompositeFilter:
    """Build and return default rock filters."""
    return ProducedManaFilter(colors=colors) & (
        SignetFilter() | TalismanFilter() | CrystalFilter() | ObeliskFilter()
    )


def default_rock_priorities() -> List[FilterAlias]:
    """Return default rock priorities."""
    return [
        FilterAlias.signet,
        FilterAlias.talisman,
        FilterAlias.crystal,
        FilterAlias.obelisk,
    ]


def default_sets() -> List[str]:
    """Return default set codes.

    This is used to build the Scryfall query and to filter cards.
    """
    return [
        "ala",
        "c13",
        "c20",
        "cm2",
        "cma",
        "cmr",
        "dom",
        "e01",
        "grn",
        "iko",
        "ktk",
        "mh1",
        "mm3",
        "mrd",
        "rna",
        "soi",
        "td2",
        "vma",
        "xln",
        "znc",
    ]
