"""Filter lockets."""
from ..text import CardTextFilter


class LocketFilter(CardTextFilter):
    """Filters lockets."""

    def __init__(self):
        pattern = (
            r"^%(tap)s: Add %(symbols)s or %(symbols)s\.\n"
            r"%(or-symbols)s%(or-symbols)s%(or-symbols)s%(or-symbols)s, "
            r"%(tap)s, Sacrifice %(name)s: Draw two cards\.$"
        )
        super().__init__(pattern=pattern)
