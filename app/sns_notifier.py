import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

load_dotenv()

SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")
print(f"SNS_TOPIC_ARN: {os.getenv('SNS_TOPIC_ARN')}")


def notify_admin(filename):
    """
    Publishes a notification to SNS when a new file is received.
    Args:
        filename (str): Name of the file to include in the notification
    Returns:
        dict: Result of the publish attempt
    """
    print(f"SNS_TOPIC_ARN: {os.getenv('SNS_TOPIC_ARN')}")
    
    sns = boto3.client("sns")
    subject = f"New File Received: {filename}"
    message = f"A new file named '{filename}' has been uploaded and is ready for processing."

    try:
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
        return {
            "success": True,
            "message_id": response.get("MessageId"),
            "info": f"Notification sent for {filename}"
        }
    except (BotoCoreError, ClientError) as e:
        return {
            "success": False,
            "error": str(e)
        }
