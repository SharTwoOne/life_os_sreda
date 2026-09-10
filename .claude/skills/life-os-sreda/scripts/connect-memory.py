#!/usr/bin/env python3
"""Подключает <среда>/memory к памяти Claude Code, чтобы MEMORY.md читался в каждой сессии.

    python3 connect-memory.py <путь к среде>

Claude Code держит память проекта в ~/.claude/projects/<путь-через-дефисы>/memory.
Скрипт ставит туда симлинк на папку memory в среде. Источник истины остаётся в среде.
Если там уже лежит чужая память — ничего не трогает и говорит, что сделать руками.
"""
import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    env = Path(sys.argv[1]).expanduser().resolve()
    memory = env / "memory"
    if not memory.is_dir():
        print(f"✗ Нет папки {memory}. Сначала разверни среду.")
        sys.exit(1)

    slug = re.sub(r"[^A-Za-z0-9]", "-", str(env))
    target = Path.home() / ".claude" / "projects" / slug / "memory"

    if target.is_symlink():
        if target.resolve() == memory:
            print(f"✓ Уже подключено: {target} → {memory}")
            return
        print(f"✗ {target} уже ведёт в {target.resolve()}. Проверь руками, какая память правильная.")
        sys.exit(1)

    if target.exists():
        files = [p for p in target.iterdir() if not p.name.startswith(".")]
        if files:
            print(f"✗ В {target} уже лежит память ({len(files)} файлов). Ничего не трогаю.")
            print("  Перенеси нужные заметки в memory/ среды, строки — в memory/MEMORY.md,")
            print(f"  потом убери {target} и запусти скрипт снова.")
            sys.exit(1)
        target.rmdir()

    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(memory, target_is_directory=True)
    print(f"✓ Подключено: {target} → {memory}")
    print("  Проверка: новая сессия Claude Code в папке среды, спроси «что у тебя в памяти».")


if __name__ == "__main__":
    main()
