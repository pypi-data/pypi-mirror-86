"""Filter original dual lands."""
from ..text import CardTextFilter


class OriginalDualLandFilter(CardTextFilter):
    """Filters original dual lands."""

    def __init__(self):
        pattern = r"^\(%(tap)s: Add %(symbols)s or %(symbols)s\.\)$"
        super().__init__(pattern=pattern)
