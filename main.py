from agents.agent import Agent
from agents.bidding import conduct_bidding
from database.vector_store import VectorStore
from matching.query_matcher import match_query_to_agents
from blockchain.vechain_integration import reward_winner
from config import DUMMY_AGENTS

def main():
    # Initialize vector store and add dummy agents
    vector_store = VectorStore()
    agents = [Agent(**agent_data) for agent_data in DUMMY_AGENTS]
    vector_store.add_agents(agents)

    while True:
        query = input("\nEnter your sustainability query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break

        # Match query to agents
        matched_agents = match_query_to_agents(vector_store, query)
        print("Matched Agents:")
        for agent in matched_agents:
            print(f"- {agent.name} (ID: {agent.id})")
            print(f"  Specialization: {agent.specialization}")

        # Conduct bidding
        if matched_agents:
            winning_bid = conduct_bidding(matched_agents)
            print(f"\nWinning bid: Agent {winning_bid.agent_id} with ${winning_bid.amount:.2f}")

            # Reward winner with VeChain tokens
            reward_winner(winning_bid.agent_id, winning_bid.amount)
        else:
            print("No matching agents found.")

if __name__ == "__main__":
    main()