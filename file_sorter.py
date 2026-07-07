import os
import shutil
from collections import Counter

from categories import CATEGORY_FOLDERS, OTHERS, SKIP_FILES, get_category


def safe_dest_path(dest_dir: str, filename: str) -> str:
    dest = os.path.join(dest_dir, filename)
    if not os.path.exists(dest):
        return dest
    name, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(dest):
        dest = os.path.join(dest_dir, f"{name}_{counter}{ext}")
        counter += 1
    return dest


class FileSorter:
    def __init__(self, folder: str, action: str = "move"):
        self.folder = folder
        self.action = action

    def _list_files(self) -> list[str]:
        files = []
        for entry in os.listdir(self.folder):
            path = os.path.join(self.folder, entry)
            if not os.path.isfile(path):
                continue
            if entry.lower() in SKIP_FILES or entry.startswith("."):
                continue
            if entry in CATEGORY_FOLDERS or entry == OTHERS:
                continue
            files.append(entry)
        return files

    def preview(self) -> dict[str, int]:
        counts: Counter[str] = Counter()
        for filename in self._list_files():
            counts[get_category(filename)] += 1
        return dict(counts)

    def sort(self) -> dict:
        files = self._list_files()
        summary: Counter[str] = Counter()
        log: list[str] = []
        errors: list[str] = []

        if not files:
            return {"summary": {}, "log": [], "errors": [], "total": 0}

        for filename in files:
            category = get_category(filename)
            dest_dir = os.path.join(self.folder, category)
            os.makedirs(dest_dir, exist_ok=True)

            src = os.path.join(self.folder, filename)
            dest = safe_dest_path(dest_dir, filename)

            try:
                if self.action == "copy":
                    shutil.copy2(src, dest)
                    verb = "Copied"
                else:
                    shutil.move(src, dest)
                    verb = "Moved"
                rel_dest = os.path.relpath(dest, self.folder)
                log.append(f"{verb} {filename} -> {rel_dest}")
                summary[category] += 1
            except OSError as exc:
                errors.append(f"Failed to process {filename}: {exc}")

        return {
            "summary": dict(summary),
            "log": log,
            "errors": errors,
            "total": sum(summary.values()),
        }
