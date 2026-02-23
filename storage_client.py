import os
import boto3
from botocore.exceptions import NoCredentialsError
import shutil
import uuid
import logging

logger = logging.getLogger("StorageClient")

class StorageClient:
    def __init__(self):
        self.bucket_name = os.getenv("AWS_BUCKET_NAME", "syndicate-ai-media")
        
        # Initialize only if keys exist
        if os.getenv("AWS_ACCESS_KEY_ID"):
            self.s3 = boto3.client('s3')
            self.use_s3 = True
            logger.info("StorageClient: AWS S3 Backend Activated")
        else:
            self.use_s3 = False
            self.local_dir = "syndicate-ai/uploads"
            os.makedirs(self.local_dir, exist_ok=True)
            logger.info("StorageClient: Falling back to Local Storage (No AWS Keys found)")

    async def upload_file(self, file_obj, filename: str) -> str:
        """
        Uploads a file to S3 if configured, otherwise falls back to local storage.
        Returns the public URL or relative path.
        """
        # Generate a unique filename to prevent collisions in S3
        ext = filename.split('.')[-1] if '.' in filename else ''
        unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"

        if self.use_s3:
            try:
                # Read into memory or pass file object directly
                # In FastAPI, file_obj is a SpooledTemporaryFile
                self.s3.upload_fileobj(
                    file_obj, 
                    self.bucket_name, 
                    unique_filename,
                    ExtraArgs={'ACL': 'public-read'} # Make it public for Web3 streaming
                )
                
                bucket_location = boto3.client('s3').get_bucket_location(Bucket=self.bucket_name)
                region = bucket_location['LocationConstraint'] or 'us-east-1'
                
                url = f"https://{self.bucket_name}.s3.{region}.amazonaws.com/{unique_filename}"
                return url
            except NoCredentialsError:
                logger.error("AWS credentials not available.")
                self.use_s3 = False
            except Exception as e:
                logger.error(f"S3 Upload failed: {e}")
                
        # LOCAL FALLBACK
        file_location = os.path.join(self.local_dir, unique_filename)
        with open(file_location, "wb+") as f:
            shutil.copyfileobj(file_obj, f)
            
        return f"/uploads/{unique_filename}"

storage_client = StorageClient()
