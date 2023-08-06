"""Filter horizon lands."""
from ..text import CardTextFilter


class HorizonLandFilter(CardTextFilter):
    """Filters horizon lands."""

    def __init__(self):
        pattern = (
            r"^%(tap)s, Pay 1 life: Add %(symbols)s or %(symbols)s\.\n"
            r"\{1\}, %(tap)s, Sacrifice %(name)s: Draw a card\.$"
        )
        super().__init__(pattern=pattern)
