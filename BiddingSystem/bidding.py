from typing import List
import random
from agents.agent import Agent, Bid

def conduct_bidding(agents: List[Agent], max_rounds: int = 5) -> Bid:
    print("\nStarting bidding process...")
    
    # Initial bids
    bids = [Bid(agent.id, random.uniform(*agent.initial_bid_range)) for agent in agents]
    
    for round in range(max_rounds):
        print(f"\nRound {round + 1}:")
        bids.sort(key=lambda x: x.amount)
        for bid in bids:
            print(f"Agent {bid.agent_id} bids ${bid.amount:.2f}")
        
        if round == max_rounds - 1:
            break
        
        # New round of bidding
        new_bids = []
        for agent in agents:
            new_bid = agent.place_bid(bids[0].amount)
            new_bids.append(new_bid)
        
        bids = new_bids

    winning_bid = min(bids, key=lambda x: x.amount)
    return winning_bid