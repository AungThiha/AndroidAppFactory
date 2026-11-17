from uuid import uuid4

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tracers.langchain import wait_for_all_tracers
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from local_tracing import LocalTracer, trace_directory
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
            """You are an Android solution designer. Help the user understand code,
compare design options and trade-offs, and refine implementation plans.

- Respect the user's investigation boundary. Request only evidence needed to
  answer a specific unresolved part of the question.
- You may try plausible symbols or file paths. Use unsuccessful results to adjust
  your next request; do not repeat a failed request.
- Reuse successful results instead of repeating searches or file reads.
- Once the question is answered, stop. State uncertainty beyond the requested
  scope without investigating it.
- Keep answers concise and cite files and functions. Include line numbers when
  available, without extra tool calls just to obtain them.
"""
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
        directory = trace_directory()
        directory.mkdir(parents=True, exist_ok=True)
        trace_path = directory / f"{uuid4()}.jsonl"
        with trace_path.open("x", encoding="utf-8") as output:
            print(f"Solution Designer trace: {trace_path}", flush=True)
            state = self._graph.invoke(
                {"messages": [HumanMessage(task)]},
                config={"callbacks": [LocalTracer(output)]},
            )
        response = state["messages"][-1]
        return response.text

    def _respond(self, state: AgentState) -> AgentState:
        response = self._model.invoke([self._system_message, *state["messages"]])
        return {"messages": [response]}


def main() -> None:
    load_dotenv()
    try:
        designer = SolutionDesigner(ChatOpenAI(model="gpt-5-mini"))
        print(designer.run(input("Task: ")))
    finally:
        wait_for_all_tracers()


if __name__ == "__main__":
    main()
