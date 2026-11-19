# Run and grade an eval case

Read the assigned case README for its rubric and any case-specific instructions.

## Run the case

From the project root, run the shared runner with the agent and case folder
names from `evals/<agent>/<case>/README.md`. For example:

```sh
.venv/bin/python evals/runner.py solution_designer stops_after_sufficient_evidence
```

The runner copies `fixture/` into the workspace and passes `prompt.txt` to the
agent. It prints the workspace path and any trace paths. It suppresses the
agent's stdout so you see the answer once, in the trace. The agent's stderr
stays visible for errors that may not appear in the trace. The runner exits
with the agent's exit code.

## Grade the local trace

Apply the case rubric using only the original `.jsonl` trace in the run
workspace's `traces/` folder.

After the runner exits, run a command to get only `outputs.messages` from the
record where `event` is `"end"` and `parent_run_id` is `null`. Read the question,
tool requests and results, and final answer in that order. Look up span IDs for
citations without printing full records.

If the conversation is missing or incomplete, inspect only the trace records
needed to apply the rubric or explain why the verdict is inconclusive.

Do not fetch remote traces or save separate trace files or run snapshots.

## Report the verdict

Return a short report with your verdict, local trace path, and
supporting evidence with relevant span IDs. Leave the workspace available for
review, including after a failure or timeout.
