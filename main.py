# from tkinter import END
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph
from node import run_agent_reasoning, tool_node

load_dotenv()

AGENT_REASON = "agent_reason"
ACT = "act"
END_NODE = "end_node"
LAST = -1


def should_continue(state: MessagesState) -> str:
    """Decide whether to continue or end the flow."""
    if not state.messages[LAST].tool_calls:
        return END_NODE
    return ACT


flow = StateGraph(MessagesState)
flow.add_node(AGENT_REASON, run_agent_reasoning)
flow.set_entry_point(AGENT_REASON)
flow.add_node(ACT, tool_node)
flow.add_node(END_NODE, lambda state: state)

flow.add_conditional_edges(
    AGENT_REASON, should_continue, {"end_node": END_NODE, "act": ACT}
)

flow.add_edge(ACT, AGENT_REASON)

app = flow.compile()
app.get_graph().draw_mermaid_png(output_file_path="flow.png")


if __name__ == "__main__":
    print("Hello ReACT Langgraph with Function Calling")
