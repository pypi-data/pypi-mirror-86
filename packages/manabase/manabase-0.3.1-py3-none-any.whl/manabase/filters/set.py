"""Filter based on the card set."""
from typing import List

from ..cards import Card
from .base import FilterResult
from .composite import CompositeFilter


class CardSetFilter(CompositeFilter):
    """Filters cards based on the set in which they appear."""

    sets: List[str]

    def filter_card(self, card: Card) -> FilterResult:
        if card.set in self.sets:
            return FilterResult(card=card, accepted_by=self)
        return FilterResult(card=card)
