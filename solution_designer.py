import subprocess
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph


class AgentState(MessagesState):
    pass


class SolutionDesigner:
    def __init__(self, model: ChatOpenAI):
        self._model = model
        self._system_message = SystemMessage(
            "You are an Android solution designer. Help the user understand "
            "existing code, compare design options and trade-offs, and refine "
            "implementation plans through discussion. Keep answers concise. "
            "Support repository-specific claims with file and line evidence "
            "when available, and say when you need source access to verify them."
        )

        workflow = StateGraph(AgentState)
        workflow.add_node("respond", self._respond)
        workflow.add_edge(START, "respond")
        workflow.add_edge("respond", END)
        self._graph = workflow.compile()

    def run(self, task: str) -> str:
        state = self._graph.invoke({"messages": [HumanMessage(task)]})
        return state["messages"][-1].text

    def _respond(self, state: AgentState) -> AgentState:
        response = self._model.invoke([self._system_message, *state["messages"]])
        return {"messages": [response]}


def main() -> None:
    load_dotenv()
    designer = SolutionDesigner(ChatOpenAI(model="gpt-5-mini"))
    print(designer.run(input("Task: ")))


if __name__ == "__main__":
    main()
