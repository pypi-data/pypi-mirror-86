"""Filter cluestones."""
from ..text import CardTextFilter


class CluestoneFilter(CardTextFilter):
    """Filters cluestones."""

    def __init__(self):
        pattern = (
            r"^%(tap)s: Add %(symbols)s or %(symbols)s\.\n"
            r"%(symbols)s%(symbols)s, %(tap)s, Sacrifice %(name)s: Draw a card\.$"
        )
        super().__init__(pattern=pattern)
