import subprocess
from pathlib import Path


def main() -> None:
    """Print matches as repository-relative path:line:code.

    For example, line 42 containing "  openProduct(id)" in Screen.kt
    becomes "Screen.kt:42:openProduct(id)". Line numbers start at 1.
    """
    repository = Path("/Users/aungthiha/AndroidStudioProjects/StockMate")

    # subprocess runs another program; here, Git lists tracked Kotlin files.
    result = subprocess.run(
        ["git", "ls-files", "--", "*.kt"],
        cwd=repository,  # Run inside StockMate (cwd stands for current working directory).
        capture_output=True,  # Save normal/error output in stdout/stderr. stdout and stderr are not files
        text=True,  # Return captured output as strings instead of bytes.
        check=True,  # Raise an exception if Git exits with a nonzero status.
    )
    source_paths = result.stdout.splitlines()
    print(f"Found {len(source_paths)} tracked Kotlin files.")

    pattern = "SearchStockContent("
    for relative_path in source_paths:
        source_file = repository / relative_path
        source = source_file.read_text(encoding="utf-8")
        matches = [
            (line_number, line)
            for line_number, line in enumerate(source.splitlines(), start=1)
            if pattern in line
        ]
        for line_number, match in matches:
            print(f"{relative_path}:{line_number}:{match.strip()}")


if __name__ == "__main__":
    main()
