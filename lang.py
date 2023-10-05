from dotenv import load_dotenv
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
import re

load_dotenv()

dburi = 'sqlite:///C:/Users/aksha/Desktop/Test db/Healthcare.db'
db = SQLDatabase.from_uri(dburi)

llm = OpenAI(temperature=0)

# Instantiate the chain with verbose turned off
db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True)

# Ask the user for a question
question = input("Please enter your query: ")

output = db_chain.run(question)

print(output)
