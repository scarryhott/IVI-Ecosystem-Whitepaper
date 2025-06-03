from __future__ import annotations

"""Simple token ledger for the IVI ecosystem."""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class TokenLedger:
    """Track balances of intangible reputation tokens."""

    balances: Dict[str, float] = field(default_factory=dict)

    def mint(self, user: str, amount: float) -> None:
        if amount <= 0:
            return
        self.balances[user] = self.balances.get(user, 0.0) + amount

    def transfer(self, from_user: str, to_user: str, amount: float) -> bool:
        if amount <= 0 or self.balances.get(from_user, 0.0) < amount:
            return False
        self.balances[from_user] -= amount
        self.balances[to_user] = self.balances.get(to_user, 0.0) + amount
        return True

    def balance_of(self, user: str) -> float:
        return self.balances.get(user, 0.0)