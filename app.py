import os

from flask import Flask, request, send_file
from azure.storage.blob import BlobServiceClient, BlobClient
from io import BytesIO


app = Flask(__name__)

# Configuration
AZURE_CONNECTION_STRING = os.environ.get('AZURE_CONNECTION_STRING')
CONTAINER_NAME = "tllsidecarpoccontainer"

# Initialize the Azure Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)


@app.route("/get-file", methods=["GET"])
def get_file():
    # Get the file path from the query parameter
    file_path = request.args.get("path")

    if not file_path:
        return "File path parameter 'path' is missing.", 400

    try:
        blob_client: BlobClient = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_path)

        blob_data = blob_client.download_blob()
        stream = BytesIO()
        blob_data.readinto(stream)
        stream.seek(0)

        # Inferring the file type could be done here if needed
        return send_file(
            stream,
            as_attachment=True,
            download_name=file_path.split('/')[-1],
            mimetype='application/octet-stream',
        )
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
