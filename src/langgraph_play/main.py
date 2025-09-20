from typing import TypedDict
from langgraph.graph import StateGraph, END


class State(TypedDict):
    count: int


def inc(state: State):
    return {"count": state["count"] + 1}


builder = StateGraph(State)
builder.add_node("inc", inc)
builder.set_entry_point("inc")
builder.add_edge("inc", END)

graph = builder.compile()

if __name__ == "__main__":
    print(graph.invoke({"count": 0}))
