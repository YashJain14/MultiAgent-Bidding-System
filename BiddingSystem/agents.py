from dataclasses import dataclass
import random
from typing import Tuple

@dataclass
class Bid:
    agent_id: str
    amount: float

@dataclass
class Agent:
    id: str
    name: str
    specialization: str
    initial_bid_range: Tuple[float, float]
    reduction_strategy: str
    min_bid: float

    def place_bid(self, current_lowest_bid: float) -> Bid:
        if self.reduction_strategy == "percentage":
            bid_amount = max(current_lowest_bid * 0.95, self.min_bid)
        elif self.reduction_strategy == "fixed":
            bid_amount = max(current_lowest_bid - 100, self.min_bid)
        else:  # random
            bid_amount = max(random.uniform(self.min_bid, current_lowest_bid), self.min_bid)
        
        return Bid(self.id, round(bid_amount, 2))