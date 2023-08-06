"""Filter banners."""
from ..text import CardTextFilter


class BannerFilter(CardTextFilter):
    """Filters banners."""

    def __init__(self):
        pattern = (
            r"^%(tap)s: Add %(symbols)s, %(symbols)s, or %(symbols)s\.\n"
            r"%(symbols)s%(symbols)s%(symbols)s, %(tap)s, Sacrifice %(name)s: "
            r"Draw a card\.$"
        )
        super().__init__(pattern=pattern)
