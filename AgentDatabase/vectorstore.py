from langchain_community.document_loaders import JSONLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["source"] = " "
    metadata["id"] = str(record.get("id", ""))
    metadata["name"] = str(record.get("name", ""))
    metadata["categories"] = str(record.get("categories", []))
    metadata["specialization"] = str(record.get("specialization", ""))
    metadata["initial_bid_range"] = str(record.get("initial_bid_range", []))
    metadata["reduction_strategy"] = str(record.get("reduction_strategy", ""))
    metadata["min_bid"] = str(record.get("min_bid", ""))
    
    # Remove any None values
    metadata = {k: v for k, v in metadata.items() if v is not None}
    
    return metadata

loader = JSONLoader(
    file_path='AgentDatabase/AgentDatabase.json',
    jq_schema='.[]',
    content_key='specialization',
    metadata_func=metadata_func
)

agents = loader.load()

# Checking format
print(agents[1])

embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Save to disk
vectorstore = Chroma.from_documents(agents, embedding_function, persist_directory="./AgentDatabase/chroma_db")

print("Done")