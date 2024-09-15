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
        self.b3tr_tokens = 0
        self.round_tokens = 0  # Tokens earned in the current round

    def place_initial_bid(self, project_complexity: float) -> float:
        base_bid = random.uniform(self.initial_bid_range[0], self.initial_bid_range[1])
        self.current_bid = base_bid * project_complexity * self.reputation
        return self.current_bid

    def place_bid(self, current_lowest_bid: float, round: int) -> Tuple[float, float, float]:
        old_bid = self.current_bid
        if self.reduction_strategy == "percentage":
            new_bid = max(self.current_bid * (0.98 - (round * 0.01)), self.min_bid)
        elif self.reduction_strategy == "fixed":
            new_bid = max(self.current_bid - (self.current_bid * 0.05), self.min_bid)
        else:  # random
            new_bid = max(random.uniform(self.min_bid, self.current_bid), self.min_bid)

        if new_bid < current_lowest_bid:
            self.current_bid = new_bid
            bid_time = time.time()
            reduction = old_bid - new_bid
            return new_bid, bid_time, reduction
        return None, None, 0

    def award_b3tr_tokens(self, amount: float):
        self.b3tr_tokens += amount
        self.round_tokens = amount

    def reset_round_tokens(self):
        self.round_tokens = 0

class Coalition:
    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.specializations = list(set([spec for agent in agents for spec in agent.specializations]))
        self.reputation = sum([agent.reputation for agent in agents]) / len(agents)
        self.b3tr_tokens = 0
        self.round_tokens = 0  # Tokens earned in the current round

    def place_bid(self, current_lowest_bid: float, round: int) -> Tuple[float, float, float]:
        individual_bids = [agent.place_bid(current_lowest_bid, round) for agent in self.agents]
        valid_bids = [bid for bid, _, _ in individual_bids if bid is not None]
        if valid_bids:
            coalition_bid = sum(valid_bids) * 0.9  # 10% discount for coalition
            if coalition_bid < current_lowest_bid:
                bid_time = time.time()
                reduction = sum([agent.current_bid for agent in self.agents]) - coalition_bid
                return coalition_bid, bid_time, reduction
        return None, None, 0

    def award_b3tr_tokens(self, amount: float):
        self.b3tr_tokens += amount
        self.round_tokens = amount
        per_agent_amount = amount / len(self.agents)
        for agent in self.agents:
            agent.award_b3tr_tokens(per_agent_amount)

    def reset_round_tokens(self):
        self.round_tokens = 0
        for agent in self.agents:
            agent.reset_round_tokens()

class BiddingSystem:
    def __init__(self, agents: List[Agent], project_complexity: float, required_specializations: List[str]):
        self.agents = agents
        self.project_complexity = project_complexity
        self.required_specializations = required_specializations
        self.rounds = 5
        self.bids = {}
        self.bid_logs = []
        self.coalitions = self.form_coalitions()
        self.b3tr_pool = 1000
        self.reduction_reward_pool = 500  # Tokens for rewarding price reductions

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
            total_reduction = 0

            for agent in self.agents + self.coalitions:
                new_bid, bid_time, reduction = agent.place_bid(current_lowest_bid, round)
                total_reduction += reduction
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
            self.distribute_reduction_rewards(total_reduction)
            self.print_round_tokens()
            self.log_round(round)

        winner = min(self.bids, key=self.bids.get)
        winning_bid = self.bids[winner]
        self.distribute_b3tr_tokens(winner)
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

    def distribute_reduction_rewards(self, total_reduction):
        if total_reduction == 0:
            return

        for agent in self.agents + self.coalitions:
            if isinstance(agent, Agent):
                agent_id = agent.id
                old_bid = self.bids[agent_id]
                new_bid, _, reduction = agent.place_bid(old_bid, 0)  # Just to get the reduction
            else:  # Coalition
                agent_id = f"Coalition_{'-'.join([a.id for a in agent.agents])}"
                old_bid = self.bids[agent_id]
                new_bid, _, reduction = agent.place_bid(old_bid, 0)  # Just to get the reduction

            if reduction > 0:
                reward = (reduction / total_reduction) * self.reduction_reward_pool
                agent.award_b3tr_tokens(reward)

    def print_round_tokens(self):
        print("\nB3TR tokens awarded for price reductions in this round:")
        for agent in self.agents + self.coalitions:
            if isinstance(agent, Agent):
                print(f"{agent.name} (ID: {agent.id}): {agent.round_tokens:.2f} B3TR tokens")
            else:  # Coalition
                coalition_id = f"Coalition_{'-'.join([a.id for a in agent.agents])}"
                print(f"{coalition_id}: {agent.round_tokens:.2f} B3TR tokens")
            agent.reset_round_tokens()

    def distribute_b3tr_tokens(self, winner):
        winner_tokens = self.b3tr_pool * 0.5
        remaining_tokens = self.b3tr_pool * 0.5

        if winner.startswith("Coalition"):
            winner_coalition = next(c for c in self.coalitions if f"Coalition_{'-'.join([a.id for a in c.agents])}" == winner)
            winner_coalition.award_b3tr_tokens(winner_tokens)
        else:
            winner_agent = next(a for a in self.agents if a.id == winner)
            winner_agent.award_b3tr_tokens(winner_tokens)

        non_winners = [agent for agent in self.agents + self.coalitions if (isinstance(agent, Agent) and agent.id != winner) or (isinstance(agent, Coalition) and f"Coalition_{'-'.join([a.id for a in agent.agents])}" != winner)]
        tokens_per_participant = remaining_tokens / len(non_winners)
        
        for participant in non_winners:
            participant.award_b3tr_tokens(tokens_per_participant)

        print("\nFinal B3TR token distribution:")
        for agent in self.agents + self.coalitions:
            if isinstance(agent, Agent):
                print(f"{agent.name} (ID: {agent.id}): {agent.b3tr_tokens:.2f} B3TR tokens")
            else:  # Coalition
                coalition_id = f"Coalition_{'-'.join([a.id for a in agent.agents])}"
                print(f"{coalition_id}: {agent.b3tr_tokens:.2f} B3TR tokens")

    def generate_vechain_log(self):
        vechain_log = {
            "project_complexity": self.project_complexity,
            "required_specializations": self.required_specializations,
            "bidding_logs": self.bid_logs,
            "final_result": {
                "winner": min(self.bids, key=self.bids.get),
                "winning_bid": min(self.bids.values())
            },
            "b3tr_distribution": {
                "total_pool": self.b3tr_pool,
                "reduction_reward_pool": self.reduction_reward_pool,
                "agent_tokens": {agent.id: agent.b3tr_tokens for agent in self.agents},
                "coalition_tokens": {f"Coalition_{'-'.join([a.id for a in coalition.agents])}": coalition.b3tr_tokens for coalition in self.coalitions}
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