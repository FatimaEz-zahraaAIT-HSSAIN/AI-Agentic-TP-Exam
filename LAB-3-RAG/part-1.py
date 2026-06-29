from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage

loader = PyPDFLoader("acmecorp-employee-handbook.pdf")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200, 
    add_start_index=True
)
all_splits = text_splitter.split_documents(data)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = InMemoryVectorStore(embeddings)
ids = vector_store.add_documents(documents=all_splits)

def search_handbook(query: str) -> str:
    results = vector_store.similarity_search(query)
    return results[0].page_content

model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

model_with_tools = model.bind_tools([search_handbook])

question = "How many days of vacation does an employee get in their first year?"
messages = [HumanMessage(content=question)]

ai_message = model_with_tools.invoke(messages)
messages.append(ai_message)

if ai_message.tool_calls:
    for tool_call in ai_message.tool_calls:
        if tool_call["name"] == "search_handbook":
            tool_output = search_handbook(tool_call["args"]["query"])
            messages.append(ToolMessage(content=tool_output, tool_call_id=tool_call["id"]))
    
    final_response = model_with_tools.invoke(messages)
    print(final_response.content)
else:
    print(ai_message.content)