from flask import Flask, request, jsonify
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
import os
import json
import requests

# Load environment variables
load_dotenv()

# Set up Flask app
app = Flask(__name__)

api_key = os.getenv("BUBBLE_API_KEY")
workflow_url = os.getenv("WORKFLOW_URL")

# Set up parser
parser = LlamaParse(
    result_type="text"  # Options: "markdown" or "text"
)

# Endpoint to upload files and process them
@app.route('/upload', methods=['POST'])
def upload_files():
    # Check if files are included in the request
    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400
    
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No selected files"}), 400

    # Save files temporarily to process
    file_paths = []
    for file in files:
        filename = file.filename
        filepath = os.path.join("uploads", filename)
        file.save(filepath)
        file_paths.append(filepath)

    # Use SimpleDirectoryReader to parse the uploaded files
    file_extractor = {".xlsx": parser}
    documents = SimpleDirectoryReader(input_files=file_paths, file_extractor=file_extractor).load_data()

    print(documents)

    # Convert the documents into JSON
    response_json = json.dumps([doc.to_dict() for doc in documents], indent=2)

    payload = json.dumps({
        "data":response_json
    })
    headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
    }

        # Assuming the endpoint for inserting data is a POST request to a specific Bubble.io API endpoint
    response = requests.post(
        f"{workflow_url}",  # Replace 'your_data_type' with the actual type
        headers=headers,
        data=payload
    )

    if response.status_code == 200:
        # Process and return data if the request is successful
        data = response.json()
        return f"Data saved successfully: {data}"
    else:
        # Return an error message if the request fails
        return f"Error {response.status_code}: {response.text}"

        # return jsonify({"message": "Files uploaded and processed successfully", "data": response})


# Run the Flask app
if __name__ == '__main__':
    # Create the uploads folder if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)




# index = VectorStoreIndex.from_documents(documents)

# # create a query engine for the index
# query_engine = index.as_query_engine()

# # query the engine
# query = "To automate calculations for BOQ items (Concrete, Reinforcement, and Formwork)"
# response = query_engine.query(query)
# print(response)