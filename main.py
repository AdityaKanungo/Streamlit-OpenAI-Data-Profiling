import openai
import json

# Initialize the OpenAI API (you'll need your API key)
openai.api_key = ''
def format_metadata_for_prompt(metadata):
    tables = list(metadata.keys())
    columns = {table: [col['name'] for col in metadata[table]['columns']] for table in tables}
    return {"tables": tables, "columns": columns}

def generate_sql_query(prompt, formatted_metadata):
    # Set up the conversation with the model
    messages = [
        {"role": "system", "content": f"Given a database with tables {formatted_metadata['tables']} and columns {formatted_metadata['columns']}, you need to generate SQL queries."},
        {"role": "user", "content": prompt}
    ]
    
    # Use OpenAI to generate SQL using the chat endpoint
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    
    # Extract the model's message from the response
    return response.choices[0].message['content'].strip()
    
    return response.choices[0].text.strip()

if __name__ == "__main__":
    # Load the metadata
    with open('db_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    formatted_metadata = format_metadata_for_prompt(metadata)
    prompt = input("Please provide a prompt for SQL generation: ")
    sql_query = generate_sql_query(prompt, formatted_metadata)
    print("Generated SQL Query:", sql_query)
