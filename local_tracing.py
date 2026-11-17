"""Write workflow spans locally as JSON Lines, without a LangSmith client.

Each span has a start and end record linked by its id and parent_run_id. Flush
every record so an interrupted process leaves the evidence captured so far.
"""

import json
import os
from pathlib import Path
from threading import Lock
from typing import TextIO

from langchain_core.tracers.base import BaseTracer
from langchain_core.tracers.schemas import Run


def trace_directory() -> Path:
    return Path(
        os.environ.get("TRACE_DIRECTORY", Path(__file__).resolve().parent / "traces")
    ).expanduser().resolve()


class LocalTracer(BaseTracer):
    raise_error = True
    run_inline = True

    def __init__(self, output: TextIO):
        super().__init__()
        self._output = output
        self._lock = Lock()

    def _on_run_create(self, run: Run) -> None:
        self._write_run("start", run)

    def _on_run_update(self, run: Run) -> None:
        self._write_run("end", run)

    def _persist_run(self, run: Run) -> None:
        # The hooks write every span immediately, including unfinished traces.
        pass

    def _write_run(self, event: str, run: Run) -> None:
        """Write one span event; inputs={"pattern": "Nav"} stays a JSON object.

        UUIDs become strings and timestamps use ISO 8601 in UTC, for example
        2026-11-17 10:00:00+00:00 becomes "2026-11-17T10:00:00Z".
        """
        with self._lock:
            record = run.model_dump(
                mode="json",
                include={
                    "id",
                    "parent_run_id",
                    "name",
                    "run_type",
                    "start_time",
                    "end_time",
                    "inputs",
                    "outputs",
                    "error",
                    "extra",
                    "events",
                },
            )
            line = json.dumps({"event": event, **record}, ensure_ascii=False)
            self._output.write(line + "\n")
            self._output.flush()
