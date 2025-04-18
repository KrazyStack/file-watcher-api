
# file-watcher-api
Monitors SFTP, uploads files to S3, and triggers processing pipeline via SNS/Lambda.

# Installation
```
pip install -r requirements.txt
```

### Running virtualenv
```
pip install virtualenv

virtualenv venv
source venv/bin/activate
which python #to verify
```



# Running an application
## Docker
```
docker-compose up --build

docker-compose down
```
## Starting an application
```
http://localhost:5000/health
```

## Core Functionalities
File | Purpose
- watcher.py |  Flask app entry point: defines routes like /simulate-drop, /health, etc.
- sftp_watcher.py | Logic to monitor SFTP folder (Polls or monitors SFTP folder)
- s3_uploader.py | Upload files to S3 (/raw/)
- sns_notifier.py | Trigger SNS topic to alert admin/client
- logger.py | Structured logging helper


# Setting up in cloud

1. Create IAM User
   - IAM Console
   - User Name: file-watcher-bot
   - Select Programmatic access
   - Attach Policies : 
     - AmazonS3FullAccess (for uploading files)
     - AmazonSNSFullAccess (for publishing to SNS)
   - Save the Access Key ID and Secret Access Key (Or you may need to create explicitly)

2. Create SNS topic (Simple Notification Service)
   - Create Topic
   - Select Type: Standard (Ideal for general even-driven notifications like the file processing events you're triggering. e.g, file received, file processed, etc)
     - High throughput + order is not guaranteed + order of messages isn't critical for us
     - Best for fan-out : multiple subscribers (like email, Lambda, etc) can recevie the messages concurrently
   - Copy the Topic ARN ( eg: arn:aws:sns:)