from flask import Flask, jsonify, request
import paramiko
import boto3
from s3_uploader import upload_file_to_s3
from sns_notifier import notify_admin
import os


app = Flask(__name__)
print('---------STARTING----------')


@app.route('/start-watching', methods=['GET'])
def start_watching():
    # Placeholder for SFTP watcher logic
    return jsonify({"message": "Watching SFTP..."})

@app.route('/health', methods=["GET"])
def health_check():
    return jsonify({"status" : "ok", "service": "file-watcher-api"}), 200

@app.route("/simulate-drop", methods=["POST"])
def simulate_drop():
    filename = request.json.get("filename")
    filepath = f"/tmp/{filename}"  # This would be SFTP path in real logic
    bucket = "your-s3-bucket-name"
    key = f"raw/{filename}"

    # Upload to S3
    upload_result = upload_file_to_s3(filepath, bucket, key)

    # Notify SNS
    notify_admin(filename)

    return jsonify({
        "upload_result": upload_result,
        "message": f"{filename} uploaded and notification sent."
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
