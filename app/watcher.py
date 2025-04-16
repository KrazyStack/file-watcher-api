from flask import Flask, jsonify
import paramiko
import boto3

app = Flask(__name__)
print('---------STARTING----------')

@app.route('/start-watching', methods=['GET'])
def start_watching():
    # Placeholder for SFTP watcher logic
    return jsonify({"message": "Watching SFTP..."})

if __name__ == "__main__":
    app.run(debug=True)
