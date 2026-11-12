from pathlib import Path


def main() -> None:
    """Print matches as repository-relative path:line:code.

    For example, line 42 containing "  openProduct(id)" in Screen.kt
    becomes "Screen.kt:42:openProduct(id)". Line numbers start at 1.
    """
    repository = Path("/Users/aungthiha/AndroidStudioProjects/StockMate")
    source_file = repository / (
        "stock/presentation/src/main/java/"
        "io/github/aungthiha/stock/search/SearchStockScreen.kt"
    )
    source = source_file.read_text(encoding="utf-8")
    pattern = "SearchStockContent("
    relative_path = source_file.relative_to(repository)
    matches = [
        (line_number, line)
        for line_number, line in enumerate(source.splitlines(), start=1)
        if pattern in line
    ]
    for line_number, match in matches:
        print(f"{relative_path}:{line_number}:{match.strip()}")


if __name__ == "__main__":
    main()
