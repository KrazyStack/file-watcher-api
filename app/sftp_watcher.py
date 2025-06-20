import paramiko
import time
import os
from dotenv import load_dotenv
from s3_uploader import upload_file_to_s3
from sns_notifier import notify_admin
from datetime import datetime


# Load environment variables
load_dotenv()


# SFTP server details
SFTP_HOST = os.getenv("SFTP_HOST", "localhost")
SFTP_PORT = int(os.getenv("SFTP_PORT", 22))
SFTP_USERNAME = os.getenv("SFTP_USERNAME", "your_username")
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD", "your_password")
SFTP_DIR = os.getenv("SFTP_DIR", "/upload")

# Local folder path to simulate SFTP drop folder
LOCAL_SFTP_FOLDER = os.getenv("LOCAL_SFTP_FOLDER", "/tmp/sftp_files/")

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_RAW_PREFIX = os.getenv("S3_RAW_PREFIX", "raw/")

print('---------STARTING SFTP WATCHER----------')

'''
Simulating the SFTP Folder from Local Folder

Local Folder: We're now using LOCAL_SFTP_FOLDER as the local folder path that simulates an SFTP drop location.
Polling: The script checks the folder every minute for new files.
File Processing: When a new file is found, it uploads it to S3 and triggers an SNS notification.
File Handling: After processing, you could move the file to a processed folder inside sftp_drop_folder to track which files have already been handled.
'''
def watch_local_folder():
    """Monitors the local 'SFTP' folder for new files."""
    
    while True:
        # Get list of files in the monitored directory
        files = os.listdir(LOCAL_SFTP_FOLDER)
        for file in files:
            print("------------------")
            file_path = os.path.join(LOCAL_SFTP_FOLDER, file)

            # Skip directories or hidden files
            if os.path.isdir(file_path) or file.startswith('.'):
                continue

            print(f"New file found: {file}")
            print(f"Current Time : {datetime.now()}")

            # Upload to S3 and notify
            upload_result = upload_file_to_s3(file_path, S3_BUCKET_NAME, f"{S3_RAW_PREFIX}{file}")
            if upload_result["success"]:
                # Notify via SNS once file is uploaded to S3
                result = notify_admin(file)
                print("SNS Notification Result: " , result)
                
                # Optionally, move file to a "processed" folder after handling
                os.rename(file_path, os.path.join(LOCAL_SFTP_FOLDER, "processed", file))
                print("moved to processed folder in local")
            print("------------------")
            
            
        time.sleep(5)  # Check every seconds


def connect_to_sftp():
    """Establish an SFTP connection."""
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp

def watch_sftp_folder():
    """Monitors the SFTP server for new files."""
    try:
        sftp = connect_to_sftp()
        print(f"Connected to SFTP server: {SFTP_HOST}")

        while True:
            # Get list of files in the monitored directory
            files = sftp.listdir(SFTP_REMOTE_PATH)
            for file in files:
                file_path = f"{SFTP_REMOTE_PATH}/{file}"

                # Check if file exists and is not already processed
                if not file.startswith('.'):  # Ignore hidden files
                    print(f"New file found: {file}")
                    upload_result = upload_file_to_s3(file_path, "your-s3-bucket-name", f"raw/{file}")
                    if upload_result["success"]:
                        # Notify via SNS once file is uploaded to S3
                        notify_admin(file)
            time.sleep(60)  # Check every minute

    except Exception as e:
        print(f"Error in SFTP monitoring: {e}")
    finally:
        sftp.close()

if __name__ == "__main__":
    # watch_sftp_folder()
    watch_local_folder()
