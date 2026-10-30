#!/usr/bin/env python3
"""Export an intact skill directory. No network, no upload, no overwrite."""
import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills' / 'build-finance-mats'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=['standard', 'workbuddy'], required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--author', help='WorkBuddy publishing identity supplied by the developer')
    args = parser.parse_args()
    if args.target == 'workbuddy' and not (args.author and args.author.strip()):
        parser.error('--author is required for WorkBuddy export')
    destination = args.output.resolve() / 'build-finance-mats'
    if destination.exists():
        parser.error(f'destination already exists: {destination}')
    if SOURCE.resolve() == destination or SOURCE.resolve() in destination.parents:
        parser.error('output cannot be inside the source skill')
    source_text = (SOURCE / 'SKILL.md').read_text(encoding='utf-8')
    match = re.fullmatch(r'---\n(.*?)\n---\n(.*)', source_text, re.S)
    if not match:
        parser.error('source frontmatter is invalid')
    text = source_text
    if args.target == 'workbuddy':
        version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
        extra = {
            'display_name': '金融垫板制作与优化',
            'display_name_en': 'Financial Client Communication Slides',
            'description_zh': '按四类规范新建或优化金融垫板，强调清晰结论、证据和有效图示。',
            'description_en': 'Create or improve financial client slides with evidence-backed conclusions and purposeful visuals.',
            'version': version,
            'author': args.author.strip(),
        }
        # JSON strings are valid YAML quoted scalars; safely preserve user text.
        fields = '\n'.join(f'{key}: {json.dumps(value, ensure_ascii=False)}' for key, value in extra.items())
        text = '---\n' + match.group(1) + '\n' + fields + '\n---\n' + match.group(2)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, destination, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
    (destination / 'SKILL.md').write_text(text, encoding='utf-8')
    print(destination)

if __name__ == '__main__':
    main()
