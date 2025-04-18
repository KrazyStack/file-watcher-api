import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError

import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError

def upload_file_to_s3(filepath, bucket_name, key):
    """
    Uploads a local file to S3 at the specified key.
    Args:
        filepath (str): Local file path
        bucket_name (str): S3 bucket name
        key (str): S3 object key (e.g., raw/filename.csv)
    Returns:
        dict: Result info or error
    """
    s3 = boto3.client("s3")

    if not os.path.exists(filepath):
        return {"success": False, "error": f"File not found: {filepath}"}

    try:
        s3.upload_file(filepath, bucket_name, key)
        return {
            "success": True,
            "bucket": bucket_name,
            "key": key,
            "message": "File uploaded successfully"
        }
    except (BotoCoreError, ClientError) as e:
        return {
            "success": False,
            "error": str(e)
        }
