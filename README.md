# Android Development Workflow

Multi-agent Android development workflow using Python and LangGraph.

## Requirements

Python 3.11 or newer (`python3`).

## Setup

Run these commands from the project directory.

### 1. Install and activate dependencies

```sh
source ./setup.sh
```

This creates a local `.venv`, installs the exact dependency versions listed in
`requirements.txt`, and activates it.

### 2. Configure the API key

If you do not have a `.env` file, create it:

```sh
cp .env.example .env
```

Set `OPENAI_API_KEY` in `.env` to your API key.

### 3. Configure LangSmith tracing

In [LangSmith Cloud](https://smith.langchain.com), create a workspace-scoped
service key and connect an existing agent with ID `solutiondesigner`.

Copy the `LANGSMITH_*` settings from `.env.example` into your `.env`. 

Set `LANGSMITH_API_KEY` to the service key and use the endpoint for your account's
region (the example uses APAC). 

Keep `LANGSMITH_AGENT_ENVIRONMENT=local`.

Tracing starts automatically when you run the agent. 

View runs under **SolutionDesigner → Local → Tracing**.

## Run

Set the repository path once per terminal session:

```sh
export REPOSITORY_PATH="/path/to/android-repository"
```

Run the solution designer and enter your task at the prompt:

```sh
python3 solution_designer.py
```
