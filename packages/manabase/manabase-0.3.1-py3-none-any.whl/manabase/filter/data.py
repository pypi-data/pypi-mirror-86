"""Filter related constants and data."""
from __future__ import annotations

from enum import Enum
from typing import Dict, Type

from ..filters.base import CardFilter
from ..filters.colors import BasicLandReferencedFilter, ProducedManaFilter
from ..filters.composite import CompositeFilter
from ..filters.lands.battle import BattleLandFilter
from ..filters.lands.bond import BondLandFilter
from ..filters.lands.bounce import BounceLandFilter
from ..filters.lands.check import CheckLandFilter
from ..filters.lands.cycling import CyclingLandFilter
from ..filters.lands.fast import FastLandFilter
from ..filters.lands.fetch import FetchLandFilter
from ..filters.lands.filter import FilterLandFilter
from ..filters.lands.horizon import HorizonLandFilter
from ..filters.lands.original import OriginalDualLandFilter
from ..filters.lands.pain import PainLandFilter
from ..filters.lands.reveal import RevealLandFilter
from ..filters.lands.scry import ScryLandFilter
from ..filters.lands.shock import ShockLandFilter
from ..filters.rocks.banner import BannerFilter
from ..filters.rocks.cluestone import CluestoneFilter
from ..filters.rocks.crystal import CrystalFilter
from ..filters.rocks.locket import LocketFilter
from ..filters.rocks.obelisk import ObeliskFilter
from ..filters.rocks.signet import SignetFilter
from ..filters.rocks.talisman import TalismanFilter


class FilterAlias(Enum):
    """Defines possible filter aliases in a filter string."""

    # Color filters
    producer = "producer"
    reference = "reference"

    # Land filters
    battle = "battle"
    bond = "bond"
    bounce = "bounce"
    check = "check"
    cycling = "cycling"
    fast = "fast"
    fetch = "fetch"
    filter = "filter"
    horizon = "horizon"
    original = "original"
    pain = "pain"
    reveal = "reveal"
    scry = "scry"
    shock = "shock"

    # Rock filters
    banner = "banner"
    cluestone = "cluestone"
    crystal = "crystal"
    locket = "locket"
    obelisk = "obelisk"
    signet = "signet"
    talisman = "talisman"

    @staticmethod
    def alias(filter_: CardFilter) -> FilterAlias:
        """Return the alias for ``filter_``.

        Raises:
            KeyError: If the filter has no alias.
        """
        return _FILTER_ALIAS_BY_CLASS_NAME[filter_.__class__.__name__]

    @staticmethod
    def filter_type(alias: FilterAlias) -> Type[CardFilter]:
        """Return a card filter type for a given alias."""
        return _FILTER_CLASS_BY_ALIAS[alias]


class FilterOperator(Enum):
    """Defines possible operators of a filter string."""

    and_ = "&"
    or_ = "|"
    xor = "^"
    invert = "~"


_FILTER_CLASS_BY_ALIAS: Dict[FilterAlias, Type[CompositeFilter]] = {
    FilterAlias.producer: ProducedManaFilter,
    FilterAlias.reference: BasicLandReferencedFilter,
    FilterAlias.battle: BattleLandFilter,
    FilterAlias.bond: BondLandFilter,
    FilterAlias.bounce: BounceLandFilter,
    FilterAlias.check: CheckLandFilter,
    FilterAlias.cycling: CyclingLandFilter,
    FilterAlias.fast: FastLandFilter,
    FilterAlias.fetch: FetchLandFilter,
    FilterAlias.filter: FilterLandFilter,
    FilterAlias.horizon: HorizonLandFilter,
    FilterAlias.original: OriginalDualLandFilter,
    FilterAlias.pain: PainLandFilter,
    FilterAlias.reveal: RevealLandFilter,
    FilterAlias.scry: ScryLandFilter,
    FilterAlias.shock: ShockLandFilter,
    FilterAlias.banner: BannerFilter,
    FilterAlias.cluestone: CluestoneFilter,
    FilterAlias.crystal: CrystalFilter,
    FilterAlias.locket: LocketFilter,
    FilterAlias.obelisk: ObeliskFilter,
    FilterAlias.signet: SignetFilter,
    FilterAlias.talisman: TalismanFilter,
}

_FILTER_ALIAS_BY_CLASS_NAME: Dict[str, FilterAlias] = {
    v.__name__: k for k, v in _FILTER_CLASS_BY_ALIAS.items()
}
