# Android Development Workflow

Requires Python 3 (`python3`). Run these commands from the project directory.

## Setup

### 1. Install and activate dependencies

```sh
source ./setup.sh
```

This creates a local `.venv`, installs `requirements.txt`, and activates it.

### 2. Configure the API key

If you do not have a `.env` file, create it:

```sh
cp .env.example .env
```

Set `OPENAI_API_KEY` in `.env` to your API key.
