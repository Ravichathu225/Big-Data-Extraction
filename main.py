import os
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import Document
from llama_index.core.settings import Settings
import pandas as pd
import json
import requests

os.environ["OPENAI_API_KEY"] = "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"

# Step 1: Upload and read the Excel file through Bubble.io
bubble_file_url = "https://res.cloudinary.com/dx6ae7luv/raw/upload/v1732098096/ko9bxupbkqo5rblq9q8s.xlsx"
response = requests.get(bubble_file_url)
with open("input_file.xlsx", 'wb') as file:
    file.write(response.content)

input_data = pd.read_excel("input_file.xlsx")

# Print the column names to see what's available
print("Available columns:", input_data.columns.tolist())

# Convert all columns to string and combine them into a single text
documents = []
for _, row in input_data.iterrows():
    # Combine all columns into a single text string
    text = " ".join(str(value) for value in row.values if pd.notna(value))
    documents.append(Document(text=text))

# Step 2: Initialize LlamaIndex with Settings
Settings.llm_cache = None  # Disable caching (optional)
Settings.chunk_size = 1024  # Set chunk size (optional)
index = VectorStoreIndex.from_documents(documents)

# Step 3: Query for structured data
query_engine = index.as_query_engine()
query = "Extract names, dates, and addresses from the content."
response = query_engine.query(query)

# Parse the response into structured data
# For simplicity, assume LlamaIndex returns JSON-like objects
structured_data = [
    {"Name": "John Doe", "Date": "2024-11-01", "Address": "123 Main St"},
    {"Name": "Jane Smith", "Date": "2024-11-15", "Address": "456 Elm St"},
    # Parse actual response here based on your query
]

# Step 4: Export the structured data to a JSON file
output_file = "structured_data.json"
with open(output_file, 'w') as file:
    json.dump(structured_data, file)

print(f"Structured data has been saved to {output_file}")