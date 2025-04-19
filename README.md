
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
- sftp_watcher.py | Logic to monitor SFTP folder (Polls or monitors SFTP folder),  When a new file is detected, it triggers the process of uploading the file to S3,
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

3. Creating a S3 bucket
```
aws s3 mb s3://<bucket-name> --region us-east-1
```

4. Adding an Email Subscription to your SNS Topic
```
1. Go to Amazon SNS in the AWS Console.
2. Click on Topics → select your topic.
3. Go to the "Subscriptions" tab.
4. Click "Create subscription".
5. Set Protocol: Email
6. Set Endpoint: <Enter your email address>
7. Click "Create Subscription"
8. Check your email inbox and confirm the subscription via the link
```
Alternative - throubh AWS CLI
```
aws sns subscribe \
  --topic-arn arn:aws:sns:your-region:your-account-id:your-topic-name \
  --protocol email \
  --notification-endpoint you@example.com
```

# Resources
## S3 - Personal Note
- S3 Note:
  - https://www.notion.so/S3-Simple-Storage-Service-93051e2403024831a5d488bb46e99cad


# Flow:
1. SFTP Watcher watches for files in SFTP folder
2. Uploads to S3 `/raw` folder, if file found + moves to `/processed` folder in local
3. Sends SNS a message
4. SNS has subscription like email protocol which triggers email after uploaded in S3
5. Trigger AWS Lambda after S3 upload. 
   1. To start the process of moving the file, registering metadata, and possibly triggering the next stage in the workflow (eg: file processing)
   2. Why Lambda - because it allows us to execute small, stateless tasks in the cloud without managing infrastructure
   