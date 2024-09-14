# BiddingSystem/bidding_system.py
import random
import json
import time
from typing import List, Tuple
import hashlib

class Agent:
    def __init__(self, id: str, name: str, initial_bid_range: List[float], reduction_strategy: str, min_bid: float, specializations: List[str], bid_unit: str, specialization: str):
        self.id = id
        self.name = name
        self.initial_bid_range = [float(x) for x in initial_bid_range]
        self.reduction_strategy = reduction_strategy
        self.min_bid = float(min_bid)
        self.specializations = specializations
        self.bid_unit = bid_unit
        self.specialization = specialization
        self.current_bid = None
        self.reputation = random.uniform(0.5, 1.0)

    def place_initial_bid(self, project_complexity: float) -> float:
        base_bid = random.uniform(self.initial_bid_range[0], self.initial_bid_range[1])
        self.current_bid = base_bid * project_complexity * self.reputation
        return self.current_bid

    def place_bid(self, current_lowest_bid: float, round: int) -> Tuple[float, float]:
        if self.reduction_strategy == "percentage":
            new_bid = max(self.current_bid * (0.98 - (round * 0.01)), self.min_bid)
        elif self.reduction_strategy == "fixed":
            new_bid = max(self.current_bid - (self.current_bid * 0.05), self.min_bid)
        else:  # random
            new_bid = max(random.uniform(self.min_bid, self.current_bid), self.min_bid)

        if new_bid < current_lowest_bid:
            self.current_bid = new_bid
            bid_time = time.time()
            return new_bid, bid_time
        return None, None
class Coalition:
    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.specializations = list(set([spec for agent in agents for spec in agent.specializations]))
        self.reputation = sum([agent.reputation for agent in agents]) / len(agents)

    def place_bid(self, current_lowest_bid: float, round: int) -> Tuple[float, float]:
        individual_bids = [agent.place_bid(current_lowest_bid, round) for agent in self.agents]
        valid_bids = [bid for bid, _ in individual_bids if bid is not None]
        if valid_bids:
            coalition_bid = sum(valid_bids) * 0.9  # 10% discount for coalition
            if coalition_bid < current_lowest_bid:
                bid_time = time.time()
                return coalition_bid, bid_time
        return None, None

class BiddingSystem:
    def __init__(self, agents: List[Agent], project_complexity: float, required_specializations: List[str]):
        self.agents = agents
        self.project_complexity = project_complexity
        self.required_specializations = required_specializations
        self.rounds = 5
        self.bids = {}
        self.bid_logs = []
        self.coalitions = self.form_coalitions()

    def form_coalitions(self) -> List[Coalition]:
        coalitions = []
        for i in range(len(self.agents)):
            for j in range(i+1, len(self.agents)):
                if set(self.agents[i].specializations + self.agents[j].specializations) == set(self.required_specializations):
                    coalitions.append(Coalition([self.agents[i], self.agents[j]]))
        return coalitions

    def initial_bidding(self):
        for agent in self.agents + self.coalitions:
            if isinstance(agent, Agent):
                self.bids[agent.id] = agent.place_initial_bid(self.project_complexity)
            else:  # Coalition
                self.bids[f"Coalition_{'-'.join([a.id for a in agent.agents])}"] = sum([a.place_initial_bid(self.project_complexity) for a in agent.agents])
        
    def run_bidding(self):
        self.initial_bidding()
        print("Initial bids:")
        self.print_bids()
        self.log_round("initial")

        for round in range(1, self.rounds + 1):
            print(f"\nRound {round}:")
            current_lowest_bid = min(self.bids.values())
            new_bids = {}

            for agent in self.agents + self.coalitions:
                new_bid, bid_time = agent.place_bid(current_lowest_bid, round)
                if new_bid:
                    if isinstance(agent, Agent):
                        new_bids[agent.id] = new_bid
                        self.log_bid(agent.id, new_bid, bid_time, round)
                    else:  # Coalition
                        coalition_id = f"Coalition_{'-'.join([a.id for a in agent.agents])}"
                        new_bids[coalition_id] = new_bid
                        self.log_bid(coalition_id, new_bid, bid_time, round)
                else:
                    if isinstance(agent, Agent):
                        new_bids[agent.id] = self.bids[agent.id]
                    else:  # Coalition
                        new_bids[f"Coalition_{'-'.join([a.id for a in agent.agents])}"] = self.bids[f"Coalition_{'-'.join([a.id for a in agent.agents])}"]

            self.bids = new_bids
            self.print_bids()
            self.log_round(round)

        winner = min(self.bids, key=self.bids.get)
        winning_bid = self.bids[winner]
        return winner, winning_bid

    def print_bids(self):
        for agent_id, bid in self.bids.items():
            if agent_id.startswith("Coalition"):
                print(f"{agent_id}: ${bid:.2f}")
            else:
                agent = next(agent for agent in self.agents if agent.id == agent_id)
                print(f"{agent.name} (ID: {agent_id}): ${bid:.2f} {agent.bid_unit}")

    def log_bid(self, agent_id: str, bid: float, timestamp: float, round: int):
        log_entry = {
            "agent_id": agent_id,
            "bid": bid,
            "timestamp": timestamp,
            "round": round
        }
        self.bid_logs.append(log_entry)

    def log_round(self, round):
        log_entry = {
            "round": round,
            "bids": self.bids.copy()
        }
        self.bid_logs.append(log_entry)

    def generate_vechain_log(self):
        vechain_log = {
            "project_complexity": self.project_complexity,
            "required_specializations": self.required_specializations,
            "bidding_logs": self.bid_logs,
            "final_result": {
                "winner": min(self.bids, key=self.bids.get),
                "winning_bid": min(self.bids.values())
            }
        }
        return json.dumps(vechain_log)

    def get_vechain_hash(self):
        vechain_log = self.generate_vechain_log()
        return hashlib.sha256(vechain_log.encode()).hexdigest()

def run_bidding_simulation(agents: List[Agent], project_complexity: float, required_specializations: List[str]):
    bidding_system = BiddingSystem(agents, project_complexity, required_specializations)
    winner, winning_bid = bidding_system.run_bidding()
    vechain_log = bidding_system.generate_vechain_log()
    vechain_hash = bidding_system.get_vechain_hash()
    return winner, winning_bid, vechain_log, vechain_hash