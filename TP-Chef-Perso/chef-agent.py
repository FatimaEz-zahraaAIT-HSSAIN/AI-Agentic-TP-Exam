from langchain.agents import create_agent 
from langchain.messages import HumanMessage 
from langchain_ollama import ChatOllama 
from langchain.tools import tool 
from typing import Dict, Any 
from tavily import TavilyClient 
from dotenv import load_dotenv 
from langgraph.checkpoint.memory import InMemorySaver 

load_dotenv() 

model = ChatOllama( 
    model="llama3.2:3b",
    temperature=0 
)

tavily_client = TavilyClient() 

@tool 
def web_search(query: str) -> Dict[str, Any]: 
    """Outil pour rechercher sur internet des recettes, techniques de cuisine ou associations d'ingrédients."""
    return tavily_client.search(query) 

system_prompt = """Vous êtes un chef cuisinier personnel intelligent.
Votre mission est de :
1. Recevoir la liste des ingrédients disponibles dans le réfrigérateur de l'utilisateur.
2. Mémoriser les préférences (ex: végétarien, allergies) de l'utilisateur au fil de la discussion.
3. Utiliser l'outil 'web_search' pour compléter vos connaissances culinaires si nécessaire (recettes, techniques, etc.).
4. Proposer un ou plusieurs plats savoureux adaptés aux ingrédients disponibles et aux préférences mémorisées."""

checkpointer = InMemorySaver() 
config = {"configurable": {"thread_id": "1"}} 

chef_agent = create_agent(
    model=model, 
    tools=[web_search], 
    system_prompt=system_prompt, 
    checkpointer=checkpointer 
)

print("\n" + "="*50)
print("| Bienvenue ! Votre Chef Personnel est prêt.     |")
print("| (Tapez 'quitter', 'exit' ou 'quit' pour        | \n"
"| arrêter la discussion)                         |")
print("="*50 + "\n")

while True:
    user_text = input("Vous : ")
    
    if user_text.lower() in ['quitter', 'exit', 'quit']:
        print("\nChef : Au revoir et bon appétit ! 🍽️")
        break
        
    if not user_text.strip():
        continue

    question = HumanMessage(content=user_text)

    try:
        response = chef_agent.invoke(
            {"messages": [question]}, 
            config 
        )
        print("\nChef :", response['messages'][-1].content, "\n")
        
    except Exception as e:
        print(f"\n[Erreur] Une erreur s'est produite : {e}\n")