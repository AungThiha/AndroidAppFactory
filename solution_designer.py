from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from source_read import read_sources
from source_search import search_source


class AgentState(MessagesState):
    pass


class SolutionDesigner:
    def __init__(self, model: ChatOpenAI):
        # Binding describes the tool to the model; it does not execute requests.
        tools = [search_source, read_sources]
        self._model = model.bind_tools(tools)
        self._system_message = SystemMessage(
            "You are an Android solution designer. Help the user understand "
            "existing code, compare design options and trade-offs, and refine "
            "implementation plans through discussion. Keep answers concise. "
            "Support repository-specific claims with file and line evidence "
            "when available, and say when you need source access to verify them."
        )

        workflow = StateGraph(AgentState)
        workflow.add_node("respond", self._respond)
        # Execute requested tools and append their results as ToolMessages.
        # Return input errors to the model so it can correct tool requests.
        workflow.add_node("tools", ToolNode(tools, handle_tool_errors=(ValueError,)))
        workflow.add_edge(START, "respond")
        # Execute tools only when the model requests them; otherwise finish.
        workflow.add_conditional_edges(
            "respond", tools_condition, {"tools": "tools", END: END}
        )
        workflow.add_edge("tools", "respond")
        self._graph = workflow.compile()

    def run(self, task: str) -> str:
        state = self._graph.invoke({"messages": [HumanMessage(task)]})
        response = state["messages"][-1]
        return response.text

    def _respond(self, state: AgentState) -> AgentState:
        response = self._model.invoke([self._system_message, *state["messages"]])
        return {"messages": [response]}


def main() -> None:
    load_dotenv()
    designer = SolutionDesigner(ChatOpenAI(model="gpt-5-mini"))
    print(designer.run(input("Task: ")))


if __name__ == "__main__":
    main()
