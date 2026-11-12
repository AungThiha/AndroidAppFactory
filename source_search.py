import subprocess
from pathlib import Path
from typing import TypedDict


class SearchResult(TypedDict):
    matches: list[str]
    message: str | None


def search_source(pattern: str) -> SearchResult:
    """Search tracked Kotlin files in StockMate for literal text.

    Return at most 20 repository-relative path:line:code strings in matches.
    Set message when additional matches exist; otherwise it is None.
    Line numbers start at 1.
    For example, pattern "openProduct(" matching line 42 containing
    "  openProduct(id)" in Screen.kt returns
    {"matches": ["Screen.kt:42:openProduct(id)"], "message": None}.
    """
    repository = Path("/Users/aungthiha/AndroidStudioProjects/StockMate").resolve()

    # subprocess runs another program; here, Git lists tracked Kotlin files.
    result = subprocess.run(
        ["git", "ls-files", "--", "*.kt"],
        cwd=repository,  # Run inside StockMate (cwd stands for current working directory).
        capture_output=True,  # Save normal/error output in stdout/stderr. stdout and stderr are not files
        text=True,  # Return captured output as strings instead of bytes.
        check=True,  # Raise an exception if Git exits with a nonzero status.
    )
    source_paths = result.stdout.splitlines()

    max_results = 20
    results = []
    for relative_path in source_paths:
        source_file = (repository / relative_path).resolve()
        source = source_file.read_text(encoding="utf-8")
        matches = [
            (line_number, line)
            for line_number, line in enumerate(source.splitlines(), start=1)
            if pattern in line
        ]
        for line_number, match in matches:
            if len(results) >= max_results:
                return {
                    "matches": results,
                    "message": f"Stopped after {max_results} matches; more matches exist.",
                }
            results.append(f"{relative_path}:{line_number}:{match.strip()}")
    return {"matches": results, "message": None}


def main() -> None:
    result = search_source("SearchStockContent(")
    for match in result["matches"]:
        print(match)
    if result["message"] is not None:
        print(result["message"])


if __name__ == "__main__":
    main()
