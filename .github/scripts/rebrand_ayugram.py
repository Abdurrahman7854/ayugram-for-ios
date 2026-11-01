#!/usr/bin/env python3
"""Replace visible Swiftgram product names in the AyuGram iOS build source."""

from pathlib import Path
import sys


def replace_text(path: Path, old: str, new: str) -> int:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count:
        path.write_text(text.replace(old, new), encoding="utf-8")
    return count


def main() -> None:
    source = Path(sys.argv[1]).resolve()
    localization_roots = [
        source / "Telegram/Telegram-iOS",
        source / "Swiftgram/SGStrings/Strings",
    ]
    changed_files = 0
    changed_names = 0
    for root in localization_roots:
        if not root.is_dir():
            raise SystemExit(f"Missing localization directory: {root}")
        for path in root.rglob("*"):
            if path.suffix not in {".strings", ".stringsdict"}:
                continue
            file_changes = replace_text(path, "Swiftgram", "AyuGram")
            file_changes += replace_text(path, "SWIFTGRAM", "AYUGRAM")
            changed_names += file_changes
            if file_changes:
                changed_files += 1

    for path in (source / "Telegram/Telegram-iOS").rglob("AppIntentVocabulary.plist"):
        file_changes = replace_text(path, "Swiftgram", "AyuGram")
        changed_names += file_changes
        if file_changes:
            changed_files += 1

    source_replacements = {
        "Swiftgram/SGSettingsUI/Sources/SGSettingsController.swift": (
            ('title: .text("Swiftgram")', 'title: .text("AyuGram")'),
        ),
        "Swiftgram/SGDebugUI/Sources/SGDebugUI.swift": (
            ('title: .text("Swiftgram Debug")', 'title: .text("AyuGram Debug")'),
        ),
        "Swiftgram/SGProUI/Sources/SGProUI.swift": (
            ('title: .text("Swiftgram Pro")', 'title: .text("AyuGram Pro")'),
        ),
        "Swiftgram/SGPayWall/Sources/SGPayWall.swift": (
            ('Text("Swiftgram Pro")', 'Text("AyuGram Pro")'),
        ),
    }
    for relative, replacements in source_replacements.items():
        path = source / relative
        if not path.is_file():
            raise SystemExit(f"Missing expected AyuGram UI source: {relative}")
        for old, new in replacements:
            count = replace_text(path, old, new)
            if count != 1:
                raise SystemExit(f"Expected one {old!r} in {relative}, found {count}")
            changed_names += count
        changed_files += 1

    if changed_names == 0:
        raise SystemExit("No Swiftgram branding was found to replace")
    print(f"Rebranded {changed_names} visible names across {changed_files} localization and UI files.")


if __name__ == "__main__":
    main()
