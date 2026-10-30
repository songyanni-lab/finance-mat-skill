"""Offline smoke checks for portable exports; no model or network required."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'export_skill.py'
SOURCE = ROOT / 'skills' / 'build-finance-mats'

def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)

def main():
    with tempfile.TemporaryDirectory(prefix='finance-mat-export-') as temp:
        base = Path(temp)
        standard = base / 'standard'
        buddy = base / 'workbuddy'
        assert run('--target', 'standard', '--output', standard).returncode == 0
        original = (SOURCE / 'SKILL.md').read_text(encoding='utf-8')
        assert (standard / 'build-finance-mats' / 'SKILL.md').read_text(encoding='utf-8') == original
        author = 'Example "Publisher"\nTeam'
        assert run('--target', 'workbuddy', '--author', author, '--output', buddy).returncode == 0
        exported = (buddy / 'build-finance-mats' / 'SKILL.md').read_text(encoding='utf-8')
        head, body = exported.split('---', 2)[1:]
        assert body == original.split('---', 2)[2]
        assert 'author: ' + json.dumps(author, ensure_ascii=False) in head
        for key in ['name', 'description', 'display_name', 'display_name_en', 'description_zh', 'description_en', 'version', 'author']:
            assert key + ':' in head
        for file in (SOURCE / 'references').glob('*.md'):
            assert (buddy / 'build-finance-mats' / 'references' / file.name).read_bytes() == file.read_bytes()
        assert run('--target', 'standard', '--output', standard).returncode != 0
        assert run('--target', 'workbuddy', '--output', base / 'no-author').returncode != 0
        assert run('--target', 'standard', '--output', SOURCE / 'nested-test').returncode != 0
    print('PASS: exports preserve content, escape metadata, reject overwrite/missing author/nested output')

if __name__ == '__main__':
    main()
