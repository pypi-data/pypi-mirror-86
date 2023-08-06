"""Filters filter lands."""
from ..text import CardTextFilter

# TODO: Add Shadowmoor/Eventide filter lands.


class FilterLandFilter(CardTextFilter):
    """Filters filter lands."""

    def __init__(self):
        pattern = r"^\{1\}, %(tap)s: Add %(symbols)s%(symbols)s\.$"
        super().__init__(pattern=pattern)
