
import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


from graph.workflow import create_workease_graph

load_dotenv()


loader = TextLoader("./data/leave_policy.txt")
splits = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(loader.load())
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


graph = create_workease_graph(retriever)

if __name__ == "__main__":

    try:
        with open("graph_visualization.png", "wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())
        print("[System: Modular Graph visualization saved]\n")
    except Exception as e:
        print(f"[System Visualizer Error: {e}]\n")

    print("==========================================================")
    print(" Modular WorkEase System Started! Type 'exit' to quit. ")
    print("==========================================================")
    
    chat_config = {"configurable": {"thread_id": "session_main"}}
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ['quit', 'exit']:
            break
        
        start_time = time.time()
        result = graph.invoke({"messages": [("user", user_input)]}, chat_config)
        print(f"Agent: {result['messages'][-1].content}")
        print(f"[Response Time: {round(time.time() - start_time, 2)} seconds]")