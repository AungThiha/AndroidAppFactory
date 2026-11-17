# Run evals

The main Codex chat supervises the requested evals.

Each subfolder represents an agent and matches its Python file in the project
root. For example, `evals/solution_designer/` corresponds to `solution_designer.py`.

## Select test cases

Run only the scope the user requests:

| Request | Selected cases |
| --- | --- |
| One named test case for an agent | Only that case |
| All test cases for one agent | Every case for that agent |
| All test cases for all agents | Every case across all agents |

If the scope is unclear, ask before running. Do not assume all cases are requested.
For each selected agent, read:

- `evals/{selected_agent_folder}/README.md`
- The selected case files in `evals/{selected_agent_folder}/test_cases/*.md`

Each case file describes its prompts and grading criteria; its sibling folder
with the same name contains the fixture.

## Assign workers

The supervisor assigns one test case per worker, with at most three workers active
across the entire request. Give the worker the paths to the agent's README and
selected case file. The worker reads these instructions to learn how to run and
grade the eval, then runs the agent with the case's test prompts. The prompts are
inputs to the agent being evaluated.

After a worker reports its verdict and supporting evidence, terminate it. Never
reuse it for another case. Start a fresh worker for the next selected case as a
slot becomes available. The three-worker limit applies across all selected agents.

## Prepare each fixture

Each worker creates a workspace under the project root:

```text
eval-runs/<agent>/<case>/<run-id>/
```

Use the agent folder name and case file name without `.md` from `evals/`.
Choose a fresh UUID as the run ID for each invocation, including retries. If the
workspace already exists, choose a new run ID instead of reusing it.

Copy only the contents of the case's fixture folder into that workspace. Each
worker uses its own workspace. The project-root `eval-runs/` folder is Gitignored.

Run the agent from the original project root using `.venv/bin/python`.

Set `REPOSITORY_PATH` to the absolute path of the worker's workspace
for that invocation. For example, for Solution Designer:

```sh
REPOSITORY_PATH="/absolute/path/to/project/eval-runs/solution_designer/stops_after_sufficient_evidence/<run-id>" .venv/bin/python solution_designer.py
```

The variable applies only to that agent process and its child processes.

## Report results

Collect each worker's results and retain its workspace for review, including after
a failure or timeout. Summarize each selected case and its evidence in chat,
distinguishing behavioral failures from execution errors. Do not create trace
files or saved run snapshots.
