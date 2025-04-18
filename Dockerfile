FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Ensure the sftp_drop_folder has appropriate permissions
RUN chmod -R 755 /app/sftp_drop_folder

EXPOSE 5000

CMD ["python", "-u", "app/sftp_watcher.py"]
