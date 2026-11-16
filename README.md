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

## Run

Set the repository path once per terminal session:

```sh
export REPOSITORY_PATH="/path/to/android-repository"
```

Run the solution designer and enter your task at the prompt:

```sh
python3 solution_designer.py
```
