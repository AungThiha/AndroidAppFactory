import subprocess
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph


class AgentState(MessagesState):
    pass


class ResearchWorkflow:
    def __init__(self, model: ChatOpenAI):
        self._model = model
        self._system_message = SystemMessage(
            "You are an Android engineering researcher. Answer engineering "
            "questions concisely and say when you need repository evidence."
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
    workflow = ResearchWorkflow(ChatOpenAI(model="gpt-5-mini"))
    print(workflow.run(input("Task: ")))


if __name__ == "__main__":
    main()
