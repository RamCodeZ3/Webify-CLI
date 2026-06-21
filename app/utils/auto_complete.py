from pathlib import Path


def auto_complete_files(incomplete: str):
    partial_path = Path(incomplete) if incomplete else Path(".")

    if partial_path.is_dir():
        base_dir = partial_path
        prefix = ""

    else:
        base_dir = (
            partial_path.parent
            if str(partial_path.parent) != ""
            else Path(".")
        )
        prefix = partial_path.name

    try:
        entries = list(base_dir.iterdir())

    except (FileNotFoundError, NotADirectoryError, PermissionError):
        return []

    matches = []
    for entry in entries:
        if entry.name.startswith(prefix):
            candidate = str(entry) + ("/" if entry.is_dir() else "")
            matches.append(candidate)

    return matches

