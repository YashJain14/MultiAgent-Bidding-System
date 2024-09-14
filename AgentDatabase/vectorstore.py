from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from typing import List
from agents.agent import Agent

class VectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings()
        self.agent_db = None
        self.agents = {}

    def add_agents(self, agents: List[Agent]):
        documents = []
        for agent in agents:
            self.agents[agent.id] = agent
            documents.append(Document(page_content=agent.specialization, metadata={"name": agent.name, "id": agent.id}))
        
        self.agent_db = FAISS.from_documents(documents, self.embeddings)

    def search(self, query: str, top_k: int = 3) -> List[Document]:
        if not self.agent_db:
            raise ValueError("Agent database not initialized. Call add_agents() first.")
        
        return self.agent_db.similarity_search(query, k=top_k)