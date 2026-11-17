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

### 3. Configure tracing

Runs save local JSON Lines traces in the project's Gitignored `traces/` folder.
During eval runs, traces are saved under the run workspace, for example `eval-runs/solution_designer/stops_after_sufficient_evidence/<run-id>/traces/`; see the [eval README](evals/README.md) for more information.

If you need another location for regular runs, set `TRACE_DIRECTORY` to the
directory path.

If you want to view runs in [LangSmith](https://smith.langchain.com), copy the
`LANGSMITH_*` settings from `.env.example` into `.env`. Use a workspace-scoped
service key for `LANGSMITH_API_KEY` and your account's regional endpoint for
`LANGSMITH_ENDPOINT` (the example uses APAC). Keep
`LANGSMITH_AGENT_ENVIRONMENT=local`.

## Run

Set the repository path once per terminal session:

```sh
export REPOSITORY_PATH="/path/to/android-repository"
```

Run the solution designer and enter your task at the prompt:

```sh
python3 solution_designer.py
```
