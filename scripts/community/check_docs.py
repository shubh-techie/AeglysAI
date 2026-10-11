#!/usr/bin/env python3
"""Offline Markdown file/link/fence checks; report filenames only."""
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote


def main():
    paths = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z']).decode().split('\0')
    errors = set()
    for name in paths:
        path = Path(name)
        if path.suffix != '.md' or not path.is_file():
            continue
        text = path.read_text()
        if text.count('```') % 2:
            errors.add(name)
        for target in re.findall(r'\]\(([^)]+)\)', text):
            target = target.split('#')[0].strip('<>')
            if target and ':' not in target and not target.startswith('/'):
                if not (path.parent / unquote(target)).exists():
                    errors.add(name)
    if errors:
        for path in sorted(errors):
            print('FAIL documentation: ' + path)
        return 1
    print('PASS: local Markdown targets and fences; remote URLs/anchors not checked')
    return 0


if __name__ == '__main__':
    sys.exit(main())
