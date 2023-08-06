"""Filter talismans."""
from ..text import CardTextFilter


class TalismanFilter(CardTextFilter):
    """Filters talismans."""

    def __init__(self):
        pattern = (
            r"^%(tap)s: Add %(c)s\.\n"
            r"%(tap)s: Add %(symbols)s or %(symbols)s\. "
            r"%(name)s deals 1 damage to you\.$"
        )
        super().__init__(pattern=pattern)
