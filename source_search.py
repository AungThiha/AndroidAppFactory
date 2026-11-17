import os
import subprocess
from collections.abc import Iterator
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv

from local_tracing import trace_directory


class SearchResult(TypedDict):
    matches: list[str]
    message: str | None


def search_source(pattern: str) -> SearchResult:
    """Search project text files for single-line literal text.

    If the project is a Git repository, search all text files in that repository,
    excluding untracked files. Skip Git metadata, binary files
    and symbolic links leading outside the search root. Exclude the configured
    local trace directory so generated evidence cannot become source evidence.

    If the project is not a Git repository, search all text files in the configured project folder.

    pattern is the only input: a case-sensitive substring of one source line,
    not a filename, path, glob, or regular expression. No cursor is supported.
    Newlines are not supported; search for a single-line fragment instead.
    This tool cannot open files or read surrounding lines. If matching lines
    identify plausible candidates, report them and any uncertainty requiring
    surrounding context instead of trying to open files through this tool.
    No matches means the text was not found, not that a file does not exist.

    Return at most 20 search-root-relative path:line:code strings in matches.
    Set message when additional matches exist; otherwise it is None.
    Line numbers start at 1.
    For example, pattern "openProduct(" matching line 42 containing
    "  openProduct(id)" in Screen.kt returns
    {"matches": ["Screen.kt:42:openProduct(id)"], "message": None}.
    """
    if "\n" in pattern or "\r" in pattern:
        raise ValueError("Multiline patterns are not supported. Search for a single-line fragment instead.")

    root = Path(os.environ["REPOSITORY_PATH"]).expanduser().resolve()
    max_results = 20
    results = []
    for match in _matching_lines(root, pattern):
        if len(results) >= max_results:
            return {
                "matches": results,
                "message": f"Stopped after {max_results} matches; more matches exist.",
            }
        results.append(match)
    return {"matches": results, "message": None}


def _matching_lines(root: Path, pattern: str) -> Iterator[str]:
    """Yield root-relative matches: '  render()' on line 2 → 'Screen.kt:2:render()'."""
    traces = trace_directory()
    for source_file in _source_files(root):
        resolved = source_file.resolve()
        if not resolved.is_relative_to(root) or resolved.is_relative_to(traces):
            continue
        if not source_file.is_file():
            continue
        try:
            source = source_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "\0" in source:
            continue
        relative_path = source_file.relative_to(root).as_posix()
        for line_number, line in enumerate(source.splitlines(), start=1):
            if pattern in line:
                yield f"{relative_path}:{line_number}:{line.strip()}"


def _source_files(root: Path) -> Iterator[Path]:
    if (root / ".git").exists():
        result = subprocess.run(
            ["git", "ls-files", "--cached", "-z"],
            cwd=root,
            capture_output=True,
            check=True,
        )
        for relative_path in result.stdout.split(b"\0"):
            if relative_path:
                yield root / os.fsdecode(relative_path)
        return

    for directory, directories, filenames in os.walk(root):
        directories[:] = sorted(name for name in directories if name != ".git")
        for filename in sorted(filenames):
            if filename != ".git":
                yield Path(directory) / filename


def main() -> None:
    load_dotenv()
    result = search_source("SearchStockContent(")
    for match in result["matches"]:
        print(match)
    if result["message"] is not None:
        print(result["message"])


if __name__ == "__main__":
    main()
