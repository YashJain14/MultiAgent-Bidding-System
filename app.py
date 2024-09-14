# app.py
from flask import Flask, render_template, request, jsonify
from BiddingSystem.query import create_agents_from_docs, run_bidding_simulation
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import json

app = Flask(__name__)

# Set up vector store and retriever
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./AgentDatabase/chroma_db", embedding_function=embedding_function)
retriever = vectorstore.as_retriever(search_kwargs={"k": 8})  # Retrieve 4 agents

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    data = request.json
    query = data['query']
    project_complexity = 1.0  # Default value
    required_specializations = []  # Empty list, as we're not using this in the chatbot interface

    # Query for relevant agents
    docs = retriever.get_relevant_documents(query)

    # Create Agent objects from the retrieved documents
    agents = create_agents_from_docs(docs)

    # Run the bidding simulation
    winner, winning_bid, vechain_log, vechain_hash = run_bidding_simulation(agents, project_complexity, required_specializations)

    # Get top 3 bidders
    sorted_bids = sorted(json.loads(vechain_log)['bidding_logs'][-1]['bids'].items(), key=lambda x: float(x[1]))
    top_3_bidders = sorted_bids[:3]

    # Prepare response
    response = []
    for bidder_id, bid in top_3_bidders:
        bidder = next((agent for agent in agents if agent.id == bidder_id), None)
        if bidder:
            bid_unit = getattr(bidder, 'bid_unit', 'per unit')
            response.append({
                'name': bidder.name,
                'bid': f"${float(bid):.2f} {bid_unit}",
                'offering': bidder.specialization
            })

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)




    

