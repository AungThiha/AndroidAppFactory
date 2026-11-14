import os
from pathlib import Path
from typing import TypedDict


class ReadResult(TypedDict):
    path: str
    content: str


def read_sources(paths: list[str]) -> list[ReadResult]:
    """Read 1 to 20 text files in the configured repository.

    paths must be repository-relative, as returned by search. Return one object
    per path, in input order, containing only path and complete UTF-8 content.
    For example, paths=["Screen.kt"] for a file containing "render()\n" returns
    [{"path": "Screen.kt", "content": "render()\n"}]. Invalid paths raise errors.
    """
    if not 1 <= len(paths) <= 20:
        raise ValueError("Provide 1 to 20 repository-relative file paths.")

    repository = Path(os.environ["REPOSITORY_PATH"]).expanduser().resolve()
    results: list[ReadResult] = []
    for path in paths:
        if Path(path).is_absolute():
            raise ValueError("paths must be relative to the configured repository.")
        source_file = (repository / path).resolve()
        relative_path = source_file.relative_to(repository).as_posix()
        results.append({
            "path": relative_path,
            "content": source_file.read_text(encoding="utf-8"),
        })
    return results
