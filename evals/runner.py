"""Run one eval case using its prompt.txt and `fixture/` inputs.

Create a workspace folder at `eval-runs/<agent>/<case>/<uuid>/`.
Copy fixture contents directly into the workspace and print the workspace path.

Set the `REPOSITORY_PATH` environment variable to the workspace.
Set `TRACE_DIRECTORY` to the workspace's `traces/` folder, where the workflow
writes its traces.

The runner launches the agent from the project root with the same Python
executable used to launch the runner.

After the agent exits, the runner prints the path of each `.jsonl` file in the
trace directory and exits with the agent's exit code. The agent's stderr stays
visible in the terminal so errors before tracing starts can still be diagnosed.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from uuid import uuid4


def _read_prompt(path: Path) -> str:
    """Read UTF-8 prompt text, removing trailing newlines."""
    return path.read_text(encoding="utf-8").rstrip("\n")


def _prepare_workspace(project: Path, agent: str, case: str) -> Path:
    """Copy fixture contents into a fresh workspace and return its absolute path.

    For example, evals/solution_designer/example/fixture/Screen.kt is copied to
    eval-runs/solution_designer/example/<uuid>/Screen.kt under project.
    """
    fixture = project / "evals" / agent / case / "fixture"
    runs = project / "eval-runs" / agent / case
    runs.mkdir(parents=True, exist_ok=True)
    while True:
        workspace = runs / str(uuid4())
        try:
            workspace.mkdir()
            break
        except FileExistsError:
            continue
    shutil.copytree(fixture, workspace, dirs_exist_ok=True)
    return workspace.resolve()


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Prepare an eval workspace and run the agent with its case prompt."
    )
    parser.add_argument("agent", help="Agent folder name under evals/")
    parser.add_argument("case", help="Case folder name under the agent folder")
    args = parser.parse_args()

    for name in (args.agent, args.case):
        if Path(name).name != name or name in (".", ".."):
            parser.error("Agent and case must be names, not paths.")

    script = project / f"{args.agent}.py"
    case = project / "evals" / args.agent / args.case
    for path in (script, case / "prompt.txt"):
        if not path.is_file():
            parser.error(f"File not found: {path}")
    if not (case / "fixture").is_dir():
        parser.error(f"Fixture folder not found: {case / 'fixture'}")
    prompt = _read_prompt(case / "prompt.txt")

    workspace = _prepare_workspace(project, args.agent, args.case)
    trace_directory = workspace / "traces"
    print(f"Workspace: {workspace}", flush=True)
    result = subprocess.run(
        [sys.executable, str(script)],
        input=prompt + "\n",
        text=True,
        # The trace already contains the answer the evaluator will grade.
        stdout=subprocess.DEVNULL,
        cwd=project,
        env={
            **os.environ,
            "REPOSITORY_PATH": str(workspace),
            "TRACE_DIRECTORY": str(trace_directory),
        },
    )
    for trace in sorted(trace_directory.glob("*.jsonl")):
        print(f"Trace: {trace}")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
