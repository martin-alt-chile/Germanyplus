from pathlib import Path
import py_compile


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    files = [ROOT / "streamlit_app.py", *sorted((ROOT / "germany_plus").glob("*.py"))]
    for file in files:
        py_compile.compile(str(file), doraise=True)
    print(f"OK: {len(files)} archivos Python compilan correctamente")


if __name__ == "__main__":
    main()
