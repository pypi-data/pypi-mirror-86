"""Filter management."""
from __future__ import annotations

from typing import List

from pydantic import BaseModel

from ..cards import Card
from ..colors import Color
from ..filters.base import FilterResult
from ..filters.composite import CompositeFilter


class FilterManager(BaseModel):
    """Filter lists of cards."""

    colors: List[Color]
    filters: CompositeFilter

    def filter_cards(self, cards: List[Card]) -> List[FilterResult]:
        """Filter a list of cards."""
        results = []

        for card in cards:

            res = self.filters.filter_card(card)

            if res.accepted_by is not None:
                results.append(res)

        return results
