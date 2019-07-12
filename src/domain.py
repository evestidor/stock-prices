from datetime import date

from dataclasses import dataclass, field


@dataclass
class Price:
    symbol: str
    amount: float
    created: date = field(default_factory=date.today)
