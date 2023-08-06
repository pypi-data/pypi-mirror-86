"""Filter based on the card text.

It matches the card oracle text with a regex pattern.
"""
import re

from ..cards import Card
from .base import FilterResult
from .composite import CompositeFilter


class CardTextFilter(CompositeFilter):
    """Filters lands based on the oracle text."""

    pattern: str

    def filter_card(self, card: Card) -> FilterResult:
        regex = re.compile(self._process_pattern(self.pattern))
        res = bool(regex.match(card.oracle_text))
        if not res:
            return FilterResult(card=card)
        return FilterResult(card=card, accepted_by=self)

    @staticmethod
    def _process_pattern(pattern: str) -> str:
        """Format the pattern with helpers.

        Patterns support the ``name``, ``symbols``, ``tap``, ``basics``,
        and ``c`` formatting keys.
        """
        context = {
            "name": r"[\w\s']+",
            "symbols": r"\{(W|U|B|R|G)\}",
            "or-symbols": r"\{(W/U|W/B|B/R|B/G|U/B|U/R|R/G|R/W|G/W|G/U)\}",
            "tap": r"\{T\}",
            "basics": r"(Plains|Island|Swamp|Mountain|Forest)",
            "c": r"\{C\}",
        }
        return pattern % context
