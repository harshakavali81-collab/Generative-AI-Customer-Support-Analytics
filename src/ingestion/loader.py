"""Ingest local, explicitly trusted Markdown / TXT support policy files."""
from pathlib import Path
import hashlib

MAX_BYTES = 256_000
EXTENSIONS = {".md", ".txt"}

def load_documents(folder: str | Path) -> list[dict]:
    root = Path(folder).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Documentation directory not found: {root}")
    records = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS or path.is_symlink():
            continue
        if not path.resolve().is_relative_to(root):
            continue
        if path.stat().st_size > MAX_BYTES:
            raise ValueError(f"Document too large: {path.name}")
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        relative = path.relative_to(root).as_posix()
        records.append({"source": relative, "text": text,
                        "checksum": hashlib.sha256(text.encode()).hexdigest()})
    if not records:
        raise ValueError("No trusted source documents found")
    return records
