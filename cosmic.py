from datetime import datetime, timezone
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, MessagesState, StateGraph

# Tool definition
def get_current_time() -> dict:
    """Return the current UTC time in ISO-8601 format."""
    now = datetime.now(timezone.utc).replace(microsecond=0)
    iso = now.isoformat().replace('+00:00', 'Z')
    return {"utc": iso}

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# Build the stateless graph
workflow = StateGraph(state_schema=MessagesState)

# Model-calling node with tool integration
def call_model(state: MessagesState):
    last = state["messages"][-1]
    if isinstance(last, HumanMessage) and any(
        phrase in last.content.lower()
        for phrase in ["what time is it", "time is it", "current time", "time now"]
    ):
        time_dict = get_current_time()
        return {"messages": [SystemMessage(f"The current UTC time is {time_dict['utc']}")]}   
    # Otherwise, let the LLM answer
    response = llm.invoke(state["messages"])
    return {"messages": response}

# Graph building
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

app = workflow.compile()

# Main loop
if __name__ == "__main__":
    print("LangGraph Time Bot. Type your message and press Enter. Press Ctrl+C to exit.")
    while True:
        try:
            user_input = input("You: ")
            state = {"messages": [HumanMessage(user_input)]}
            output = app.invoke(state, config={"configurable": {"thread_id": "console-session"}})
            reply = output["messages"][-1]
            print(f"Bot: {reply.content}")           
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break