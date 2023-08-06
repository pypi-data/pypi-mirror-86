"""Filter check lands."""
from ..text import CardTextFilter


class CheckLandFilter(CardTextFilter):
    """Filters check lands."""

    def __init__(self):
        pattern = (
            r"^%(name)s enters the battlefield tapped unless you control "
            r"(a|an) %(basics)s or (a|an) %(basics)s\.\n"
            r"%(tap)s: Add %(symbols)s or %(symbols)s\.$"
        )
        super().__init__(pattern=pattern)
