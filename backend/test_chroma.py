from langchain_community.vectorstores import Chroma
from get_embeddings import get_embedding_function
from langchain.schema import Document

CHROMA_PATH = "chroma"

def test_chroma_operations():
    # Initialize Chroma DB
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())

    # Clear existing documents
    clear_chroma_db()

    # Add sample documents
    sample_docs = [
        Document(page_content="This is a test document.", metadata={"id": "test-doc-1"}),
        Document(page_content="Another test document.", metadata={"id": "test-doc-2"})
    ]
    db.add_documents(sample_docs, ids=["test-doc-1", "test-doc-2"])

    # Fetch documents
    fetched_docs = db.get(include=["documents"])
    print("Fetched Documents:", fetched_docs)

    # Clear Chroma DB again
    clear_chroma_db()

def clear_chroma_db():
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    existing_items = db.get(include=[])
    existing_ids = existing_items.get("ids", [])

    if existing_ids:
        db.delete(ids=existing_ids)
        print(f"Cleared {len(existing_ids)} documents from Chroma DB.")
    else:
        print("Chroma DB is already empty.")

if __name__ == "__main__":
    test_chroma_operations()
