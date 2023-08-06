"""Filter crystals."""
from ..text import CardTextFilter


class CrystalFilter(CardTextFilter):
    """Filters crystals."""

    def __init__(self):
        pattern = (
            r"^%(tap)s: Add %(symbols)s, %(symbols)s, or %(symbols)s\.\n"
            r"Cycling \{2\} \(\{2\}, Discard this card: Draw a card\.\)$"
        )
        super().__init__(pattern=pattern)
