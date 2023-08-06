"""Output a card list to different formats."""
from enum import Enum

from pydantic import BaseModel

from .cards import CardList


class Output(Enum):
    """Types of available output."""

    list = 1


class Formatter(BaseModel):
    """Format a card list for a given type of output."""

    output: Output

    def format_cards(self, cards: CardList) -> str:
        """Format ``cards`` using this formatter output type."""
        # TODO: match on self.output to return different outputs.
        return self._format_list(cards)

    @staticmethod
    def _format_list(cards: CardList) -> str:
        return "\n".join([f"{card.occurrences} {card.name}" for card in cards.entries])
