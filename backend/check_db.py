from langchain_community.vectorstores import Chroma
from get_embeddings import get_embedding_function
from dotenv import load_dotenv
import boto3

import os

CHROMA_PATH = "chroma"
DATA_PATH = "data"

# Load environment variables
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def check_chroma_db():
    chroma_path = "chroma"
    if not os.path.exists(chroma_path):
        return {"error": "Chroma DB directory does not exist."}

    db = Chroma(persist_directory=chroma_path, embedding_function=None)
    existing_items = db.get(include=[])
    existing_ids = existing_items.get("ids", [])
    documents = existing_items.get("documents", [])
    
    if not existing_ids:
        return {"message": "Chroma DB is empty."}
    
    return (len(existing_ids), documents)

def fetch_chunks(num_chunks):
    # Load the database
    db = Chroma(persist_directory="chroma",embedding_function=get_embedding_function())

    # fetch all documents
    all_docs = db.get(include=["documents"])
    all_chunks = all_docs['documents']

    # Print the first num_chunks chunks
    for i in range(min(num_chunks, len(all_chunks))):
        print(f"Chunk {i+1}:")
        print(all_chunks[i])
        print("-" * 50)

def clear_chroma_db():
    # Load the existing database
    db = Chroma(persist_directory="chroma", embedding_function=get_embedding_function())

    # Fetch all document IDs
    existing_items = db.get(include=[])
    existing_ids = existing_items.get("ids", [])

    # Delete all documents
    if existing_ids:
        db.delete(ids=existing_ids)
        print(f"Cleared {len(existing_ids)} documents from Chroma DB.")
    else:
        print("Chroma DB is already empty.")

def clear_s3_bucket():
    response = s3_client.list_objects_v2(Bucket=AWS_S3_BUCKET_NAME)
    for obj in response.get('Contents', []):
        key = obj['Key']
        s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=key)
        print(f"Deleted {key} from S3 bucket")

if __name__ == "__main__":
    result = check_chroma_db()
    try:
        num_chunks = result[0]
        docs = result[1]
        print(f"num chunks: {num_chunks}, docs: {docs}")
        if num_chunks > 0:
            fetch_chunks(1)
        # print("--ATTEMPTING TO CLEAR THE DATABASE--")
        # clear_chroma_db()
    except:
        print("Database is already empty.")


