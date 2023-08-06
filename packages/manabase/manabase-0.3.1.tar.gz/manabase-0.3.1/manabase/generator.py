"""Card list generator."""
from typing import Optional

from pydantic import BaseModel

from .cards import CardList
from .client import Client
from .filler.filler import ListFiller
from .filter.manager import FilterManager
from .priorities import PriorityManager
from .query import SetQueryBuilder


class ListGenerator(BaseModel):
    """Generates a list of cards from a query, filters, priorities and filler cards."""

    filters: FilterManager
    priorities: PriorityManager
    query: SetQueryBuilder
    filler: Optional[ListFiller] = None

    def generate(self, client: Client) -> CardList:
        """Generate the list of cards."""
        cards = client.fetch(self.query)

        results = self.filters.filter_cards(cards)

        card_list = self.priorities.build_list(results)

        if card_list.available and self.filler is not None:
            filler_list = self.filler.generate_filler(card_list.available)
            card_list.update(filler_list)

        return card_list
