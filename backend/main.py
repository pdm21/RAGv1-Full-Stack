import subprocess
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List


load_dotenv()

app = FastAPI()

# Load environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

# Initialize boto3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# Set up CORS
# Set up CORS
# origins = [
#     "http://localhost:3000",  # Keep this if you are testing locally
#     "http://44.202.55.152",   # Replace with your frontend's IP or domain
#     "https://docu-dive.com/",  # If using a custom domain
# ]
origins = [
    "https://docu-dive.com",  # If using a custom domain
    "http://www.docu-dive.com",
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.get("/api/getallfiles/")
async def get_all_files():
    try:
        res = s3_client.list_objects_v2(Bucket=AWS_S3_BUCKET_NAME)
        return res.get('Contents', [])
    except NoCredentialsError:
        return {"error": "Credentials not available"}
    except PartialCredentialsError:
        return {"error": "Incomplete credentials provided"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/uploadfile/")
async def upload_file(files: List[UploadFile] = File(...)):
    try:
        # Iterate over each file and upload it to S3
        for file in files:
            # Print file details for debugging
            print(f"File received: filename={file.filename}, content_type={file.content_type}")

            # Check if file.file is not None
            if file.file:
                s3_client.upload_fileobj(file.file, AWS_S3_BUCKET_NAME, file.filename)
            else:
                return {"error": f"File object for {file.filename} is None"}

        return {"info": "All files have been uploaded successfully."}
    except NoCredentialsError:
        return {"error": "Credentials not available"}
    except PartialCredentialsError:
        return {"error": "Incomplete credentials provided"}
    except Exception as e:
        return {"error": str(e)}
    

@app.post("/api/populate_db/")
async def populate_db(reset: bool = False):
    try:
        command = ["python3", "pop_db.py"]

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return {"error": result.stderr}

        return {"info": result.stdout}
    except Exception as e:
        return {"error": str(e)}


class QueryRequest(BaseModel):
    query: str

@app.post("/api/query/")
async def query(request: QueryRequest):
    try:
        command = ["python3", "query.py", request.query]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return {"response": result.stdout}
    except Exception as e:
        print(f"Error: {e}")  # Add logging for debugging
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clearfiles/")
async def clearfiles():
    try:
        command = ["python3", "clearfiles.py"]

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return {"error": result.stderr}

        return {"info": result.stdout}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
