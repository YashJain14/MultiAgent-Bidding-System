from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import json
from BiddingSystem.bidding_system import Agent, run_bidding_simulation

def create_agents_from_docs(docs):
    agents = []
    for doc in docs:
        metadata = doc.metadata
        agent = Agent(
            id=metadata['id'],
            name=metadata['name'],
            initial_bid_range=json.loads(metadata['initial_bid_range'].replace("'", '"')),
            reduction_strategy=metadata['reduction_strategy'],
            min_bid=int(metadata['min_bid']),
            specializations=json.loads(metadata['categories'].replace("'", '"'))
        )
        agents.append(agent)
    return agents