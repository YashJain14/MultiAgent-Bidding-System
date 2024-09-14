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
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})  # Retrieve 4 agents

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    data = request.json
    query = data['query']
    project_complexity = float(data['projectComplexity'])
    required_specializations = data['requiredSpecializations'].split(',')

    # Query for relevant agents
    docs = retriever.get_relevant_documents(query)

    # Create Agent objects from the retrieved documents
    agents = create_agents_from_docs(docs)

    # Run the bidding simulation
    winner, winning_bid, vechain_log, vechain_hash = run_bidding_simulation(agents, project_complexity, required_specializations)

    return jsonify({
        'winner': winner,
        'winningBid': winning_bid,
        'vechainLog': json.loads(vechain_log),
        'vechainHash': vechain_hash
    })

if __name__ == '__main__':
    app.run(debug=True)