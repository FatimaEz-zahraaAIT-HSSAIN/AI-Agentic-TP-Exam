from langchain_community.utilities import SQLDatabase
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama

db = SQLDatabase.from_uri("sqlite:///Chinook.db")

@tool
def sql_query(query: str) -> str:
    """Obtain information from the database using SQL queries"""
    try:
        print(f"Executing SQL query: {query}")
        return db.run(query)
    except Exception as e:
        return f"Error: {e}"

model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

system_prompt = """You are a SQL expert.
Rules: 
- Only use sql_query tool
- The sql_query tool takes a SQL query as input and returns the result of the query.
- Only use available columns
- If information does not exist, say so
- Do not guess
- you have to return the results in a human readable format, do not return raw SQL results or a sql query.
Database schema: 
Table Artist: 
- ArtistId 
- Name"""

agent = create_agent(
    model=model,
    tools=[sql_query],
    system_prompt=system_prompt
)

question = HumanMessage(content="Give me the first 5 artists in the database")
response = agent.invoke(
    {"messages": [question]}
)

print(response['messages'][-1].content)