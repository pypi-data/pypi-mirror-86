"""Filter signet."""
from ..text import CardTextFilter


class SignetFilter(CardTextFilter):
    """Filters signets."""

    def __init__(self):
        pattern = r"^\{1\}, %(tap)s: Add %(symbols)s%(symbols)s\.$"
        super().__init__(pattern=pattern)
