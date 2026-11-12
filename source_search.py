from pathlib import Path


def main() -> None:
    repository = Path("/Users/aungthiha/AndroidStudioProjects/StockMate")
    source_file = repository / (
        "stock/presentation/src/main/java/"
        "io/github/aungthiha/stock/search/SearchStockScreen.kt"
    )
    source = source_file.read_text(encoding="utf-8")
    print(source)


if __name__ == "__main__":
    main()
