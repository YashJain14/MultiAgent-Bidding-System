from typing import List
from database.vector_store import VectorStore
from agents.agent import Agent

def match_query_to_agents(vector_store: VectorStore, query: str, top_k: int = 3) -> List[Agent]:
    matched_docs = vector_store.search(query, top_k)
    matched_agents = [vector_store.agents[doc.metadata['id']] for doc in matched_docs]
    return matched_agents