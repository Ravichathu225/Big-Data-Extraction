from dotenv import load_dotenv
import os
from agency_swarm import Agency
from get_data_bot.readbigdata_bot import readbigdata
# from insert_data_bot.insert_data_bot import insertBot
# from update_bot.update_bot import updatebot
import openai
from flask import Flask, request, jsonify

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

financeBot_manager = readbigdata()
# insertBot_manager = insertBot()
# update_manager = updatebot()

agency = Agency(
    [financeBot_manager],
    shared_instructions='./agency_manifesto.md',
    temperature=0.5,
    max_prompt_tokens=25000
)

app = Flask(__name__)

@app.route("/api/boq_query", methods=["POST"])
def finance_query():
    # Extract the user query from the request body
    data = request.get_json()
    user_input = data.get("input_data")
    
    # Check if the query is provided
    if not user_input:
        return jsonify({"error": "Query not provided"}), 400
    
    # Get the response from the Agency instance
    response = agency.get_completion(user_input)  # {{ edit_1 }} - Replace 'run' with the correct method name
    
    # Return the response as JSON
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
