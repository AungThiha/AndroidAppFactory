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

#### Local traces

Runs save traces as JSON Lines files:

- **Regular runs:** saved in the project's Gitignored `traces/` folder. Set
  `TRACE_DIRECTORY` to use another directory.
- **Eval runs:** saved in each run workspace's `traces/` folder. See the
  [evaluator instructions](evals/evaluator.md) for details.

#### View runs in LangSmith (optional)

Copy the `LANGSMITH_*` settings from `.env.example` into `.env` to view runs in
[LangSmith](https://smith.langchain.com). Configure these values:

| Setting | Value |
| --- | --- |
| `LANGSMITH_API_KEY` | A workspace-scoped service key |
| `LANGSMITH_ENDPOINT` | Your account's regional endpoint; the example uses APAC |
| `LANGSMITH_AGENT_ENVIRONMENT` | Keep `local` |

## Run

Set the repository path once per terminal session:

```sh
export REPOSITORY_PATH="/path/to/android-repository"
```

Run the solution designer and enter your task at the prompt:

```sh
python3 solution_designer.py
```
