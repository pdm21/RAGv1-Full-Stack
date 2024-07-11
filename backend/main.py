import subprocess
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
from pydantic import BaseModel

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
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.get("/getallfiles")
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

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Print file details for debugging
        print(f"File received: filename={file.filename}, content_type={file.content_type}")

        # Check if file.file is not None
        if file.file:
            s3_client.upload_fileobj(file.file, AWS_S3_BUCKET_NAME, file.filename)
            return {"info": f"file '{file.filename}' saved at '{AWS_S3_BUCKET_NAME}'"}
        else:
            return {"error": "File object is None"}
    except NoCredentialsError:
        return {"error": "Credentials not available"}
    except PartialCredentialsError:
        return {"error": "Incomplete credentials provided"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/populate_db/")
async def populate_db(reset: bool = False):
    try:
        command = ["python3", "backend/pop_db.py"]
        if reset:
            command.append("--reset")

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return {"error": result.stderr}

        return {"info": result.stdout}
    except Exception as e:
        return {"error": str(e)}


class QueryRequest(BaseModel):
    query: str

@app.post("/query/")
async def query(request: QueryRequest):
    try:
        command = ["python3", "query.py", request.query]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return {"response": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
