# Run evals

The main Codex chat supervises the requested evals. The supervisor can use its
chat history, previous runs, and prompt-tuning discussions to coordinate the work.
The workers assigned to run and grade cases are called evaluators.

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
Find the README for each selected case at `evals/<agent>/<case>/README.md`.

## Assign workers

Start a fresh evaluator for each case run with `fork_turns: "none"` and assign
it the case README. Keep at most three evaluators active across the request.
Keep your chat history, previous runs, and prompt-tuning discussions out of the
assignment.

## Report results

Collect a short report from each evaluator with its verdict, local trace path,
and supporting span IDs. Terminate the evaluator after it reports. Summarize
the results in chat and distinguish behavioral failures from execution errors.

## Clean up manually

Do not clean up workspaces automatically. Keep run files and any workflow-produced
traces after the evaluator reports its result so humans can inspect unexpected
behavior. When review is complete, manually delete individual run directories or
the entire `eval-runs/` folder.
