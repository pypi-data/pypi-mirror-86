"""Scryfall queries."""
from enum import Enum
from typing import List

from pydantic import BaseModel


class QueryType(Enum):
    """Type of queries available."""

    land = "land"
    artifact = "artifact"


class QueryBuilder(BaseModel):
    """Builds a scryfall query string."""

    type: QueryType

    def build(self) -> str:
        """Build the query string."""
        return f"t:{self.type.value}"


class SetQueryBuilder(QueryBuilder):
    """A set dependant query builder."""

    sets: List[str]

    def build(self) -> str:
        """Build the query string."""
        query = super().build()

        if not self.sets:
            return query

        output = []
        for set_ in self.sets:
            output.append(f"set:{set_}")

        sets = SetQueryBuilder._or(output)

        return f"{query} {sets}"

    @staticmethod
    def _or(queries: List[str]) -> str:
        """Return an OR grouped list of queries."""
        return f"({' or '.join(queries)})"
