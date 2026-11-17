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
- The README for each selected case in
  `evals/{selected_agent_folder}/{case}/README.md`

Each case folder contains:

- `README.md`: run instructions and grading criteria.
- `prompt.txt`: the prompt sent to the agent being evaluated.
- `fixture/`: the source files copied into the run workspace.

## Assign workers

The supervisor assigns one test case per worker, with at most three workers active
across the entire request. Give the worker the paths to the agent's README and
selected case README. The worker reads these instructions to learn how to run and
grade the eval, then runs the agent with the case's `prompt.txt`. The prompts are
inputs to the agent being evaluated.

After a worker reports its verdict and supporting evidence, terminate it. Never
reuse it for another case. Start a fresh worker for the next selected case as a
slot becomes available. The three-worker limit applies across all selected agents.

## Run each case

From the project root, invoke the shared runner with the agent and case folder
names. For example:

```sh
.venv/bin/python evals/runner.py solution_designer stops_after_sufficient_evidence
```

## Grade the local trace

Grade each case against its rubric using only the workflow-produced `.jsonl`
trace in the run workspace's `traces/` folder. Do not fetch remote traces or
create separate trace files or saved run snapshots.

## Report results

Collect each worker's results and retain its workspace for review, including after
a failure or timeout. Summarize each selected case and its evidence in chat,
distinguishing behavioral failures from execution errors. Include the local trace
path and cite span IDs for the evidence supporting each verdict.

## Clean up manually

Do not clean up workspaces automatically. Keep run files and any workflow-produced
traces after the evaluator reports its result so humans can inspect unexpected
behavior. When review is complete, manually delete individual run directories or
the entire `eval-runs/` folder.
