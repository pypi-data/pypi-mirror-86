"""Filter bond lands."""
from ..text import CardTextFilter


class BondLandFilter(CardTextFilter):
    """Filters bond lands."""

    def __init__(self):
        pattern = (
            r"^%(name)s enters the battlefield tapped unless you have "
            r"two or more opponents\.\n"
            r"%(tap)s: Add %(symbols)s or %(symbols)s\.$"
        )
        super().__init__(pattern=pattern)
