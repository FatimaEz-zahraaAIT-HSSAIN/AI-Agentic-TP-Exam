from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq


from tools.hr_tools import get_leave_balance, get_employee_details

class WorkEaseState(TypedDict):
    messages: Annotated[list, add_messages]

def create_workease_graph(vector_retriever):

    from langchain_core.tools import tool
    @tool
    def search_company_policies(query: str) -> str:
        """Searches corporate policy documents for rules and guidelines."""
        results = vector_retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in results])

    tools = [get_leave_balance, get_employee_details, search_company_policies]
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    llm_with_tools = llm.bind_tools(tools)

    def agent_node(state: WorkEaseState):
        system_prompt = SystemMessage(content=(
            "You are an intelligent HR assistant for WorkEase. "
            "You have access to tools to look up employee information and company policies. "
            "When calling a tool, you must pass valid arguments strictly matching the tool's expected JSON schema. "
            "Do not truncate arguments or emit custom punctuation around tool requests.\n\n"
            "CRITICAL: Always use tools silently. Never expose the backend tool names, raw JSON strings, "
            "or structural function parameters to the user. Read the tool's JSON output behind the scenes "
            "and craft a friendly, natural sentence answer for the employee."
        ))
        return {"messages": [llm_with_tools.invoke([system_prompt] + state["messages"])]}

    def should_continue(state: WorkEaseState) -> Literal["tools", "__end__"]:
        last_message = state["messages"][-1]
        return "tools" if hasattr(last_message, 'tool_calls') and last_message.tool_calls else "__end__"

    builder = StateGraph(WorkEaseState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(tools))
    
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", should_continue)
    builder.add_edge("tools", "agent")
    
    return builder.compile(checkpointer=MemorySaver())