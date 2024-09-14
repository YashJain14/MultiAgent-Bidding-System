# query_system.py

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import json
from bidding_system import Agent, run_bidding_simulation

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

# Set up vector store and retriever
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./AgentDatabase/chroma_db", embedding_function=embedding_function)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})  # Retrieve 4 agents

# Query for relevant agents
query = "industrial processes inspired by natural biological systems"
docs = retriever.get_relevant_documents(query)

# Create Agent objects from the retrieved documents
agents = create_agents_from_docs(docs)

# Set up bidding parameters
project_complexity = 1.2
required_specializations = ["Green Chemistry", "Smart Manufacturing", "Robotics and Automation", "AI and Machine Learning"]

# Run the bidding simulation
winner, winning_bid, vechain_log, vechain_hash = run_bidding_simulation(agents, project_complexity, required_specializations)

# Print results
print(f"\nSimulation complete. Winner: {winner} with bid: ${winning_bid}")
print(f"VeChain Log Hash: {vechain_hash}")
print("\nVeChain Log:")
print(json.dumps(json.loads(vechain_log), indent=2))