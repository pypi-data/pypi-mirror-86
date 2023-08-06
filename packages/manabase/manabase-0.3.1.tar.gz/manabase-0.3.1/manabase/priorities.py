"""Manage a list of priorities.

When the targetted number if lands is reached, priorities can be set to
decide whichever land is returned first, and whichever is discarded.
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .cards import CardList, MaximumSizeExceeded
from .defaults import default_lands, default_occurrences
from .filter.data import FilterAlias
from .filters.base import FilterResult


class PriorityManager(BaseModel):
    """Build prioritized lists of cards."""

    maximum: int = default_lands()
    occurrences: int = default_occurrences()
    priorities: List[FilterAlias]

    @classmethod
    def from_string(
        cls,
        priorities: str,
        maximum: int = default_lands(),
        occurrences: int = default_occurrences(),
    ) -> PriorityManager:
        """Build a priority manager from a string of space separated aliases.

        Example::
        ```python
        >>> from manabase.priorities import PriorityManager
        >>> string = "original fetch"
        >>> PriorityManager.from_string(string)
        PriorityManager(maximum=37, occurrences=1, priorities=[<FilterAlias.original: \
'original'>, <FilterAlias.fetch: 'fetch'>])

        ```
        """
        priorities_list = [FilterAlias(alias) for alias in priorities.split()]
        return cls(maximum=maximum, occurrences=occurrences, priorities=priorities_list)

    def build_list(self, results: List[FilterResult]) -> CardList:
        """Build a new list of cards by truncating the specified one."""
        if self.priorities:
            results.sort(key=self._result_key, reverse=True)

        card_list = CardList(self.maximum)

        for result in results:

            try:
                card_list.add_card(result.card, self.occurrences)
            except MaximumSizeExceeded:
                if card_list.available:
                    card_list.add_card(result.card, card_list.available)
                break

        return card_list

    def _result_key(self, result: FilterResult) -> int:
        """Return a priority key for ``result``.

        Raises:
            KeyError: If accepting filter has no alias.
        """
        if not result.accepted_by:
            return -1

        alias = FilterAlias.alias(result.accepted_by)

        try:
            return len(self.priorities) - self.priorities.index(alias)
        except ValueError:
            return -1
