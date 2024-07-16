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

"""
Add an error check in case "CLEAR" is clicked, but DB is empty.
Same check for S3 is needed, to avoid any issues.
"""

def clear_chroma_db():
    try:
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
    except Exception as e:
        print(f"Error clearing Chroma DB: {e}")
"""
Code may be outdated, but Java example similarly uses S3 client.
AWS Docs, Java Example: https://docs.aws.amazon.com/AmazonS3/latest/userguide/delete-bucket.html
Can add error-checking code within each function, instead of main.
 - Ask Chat / look into what is best practice.
"""
def clear_s3_bucket():
    try:
        response = s3_client.list_objects_v2(Bucket=AWS_S3_BUCKET_NAME)
        for obj in response.get('Contents', []):
            key = obj['Key']
            s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=key)
            print(f"Deleted {key} from S3 bucket")
    except Exception as e:
        print(f"Error clearing the S3 bucket: {e}")

if __name__ == "__main__":
    try:
        clear_chroma_db()
    except Exception as e:
        print(f"Could not clear Chroma DB: {e}")

    try:
        clear_s3_bucket()
    except Exception as e:
        print(f"Could not clear S3 bucket: {e}")