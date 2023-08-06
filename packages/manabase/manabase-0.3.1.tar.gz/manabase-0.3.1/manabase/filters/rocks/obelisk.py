"""Filter obelisks."""
from ..text import CardTextFilter


class ObeliskFilter(CardTextFilter):
    """Filters obelisks."""

    def __init__(self):
        pattern = r"^%(tap)s: Add %(symbols)s, %(symbols)s, or %(symbols)s\.$"
        super().__init__(pattern=pattern)
