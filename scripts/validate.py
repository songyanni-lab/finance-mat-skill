#!/usr/bin/env python3
"""Offline structural checks. Does not assess financial accuracy or slide quality."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'build-finance-mats'

def main():
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    m = re.fullmatch(r'---\n(.*?)\n---\n(.*)', text, re.S)
    check(m is not None, 'Missing or invalid frontmatter')
    if m:
        fields = dict(re.findall(r'^([a-z-]+): (.+)$', m.group(1), re.M))
        check(set(fields) == {'name', 'description'}, 'Core must contain only name and description')
        name = fields.get('name', '')
        check(name == SKILL.name and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) is not None and len(name) <= 64, 'Invalid skill name')
        check(0 < len(fields.get('description', '')) <= 1024, 'Invalid description length')
    check(len(text.splitlines()) < 500, 'SKILL.md must stay under 500 lines')
    for file in SKILL.rglob('*.md'):
        content = file.read_text(encoding='utf-8')
        check('[TODO' not in content, f'Unfinished template: {file.name}')
        for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', content):
            if '://' in link or link.startswith('#'):
                continue
            path = (file.parent / link.split('#')[0]).resolve()
            check(path.is_relative_to(SKILL.resolve()) and path.exists(), f'Broken or escaping link: {file.name}: {link}')
    for name in ['standard.md', 'execution.md', 'examples.md', 'house-style.md', 'maintenance.md']:
        check((SKILL / 'references' / name).is_file(), f'Missing reference: {name}')
    standard = (SKILL / 'references' / 'standard.md').read_text(encoding='utf-8')
    for kind in ['市场趋势与指标解读', '基础知识及产品机制', '工具比较与选择', '政策规则解读']:
        check(kind in standard, f'Missing content type: {kind}')
    version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    check(re.fullmatch(r'\d+\.\d+\.\d+', version) is not None, 'Invalid VERSION')
    check(f'## {version} ' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8'), 'VERSION missing from CHANGELOG')
    cases = json.loads((ROOT / 'tests' / 'cases.json').read_text(encoding='utf-8'))
    ids = [case['id'] for case in cases]
    check(len(ids) == len(set(ids)), 'Duplicate test ID')
    check({'new', 'optimize'} <= {case['mode'] for case in cases}, 'Both workflows require cases')
    for case in cases:
        check(bool(case.get('prompt')) and bool(case.get('acceptance')), f'Incomplete case: {case["id"]}')
    if errors:
        print('\n'.join('FAIL: ' + error for error in errors))
        return 1
    print(f'PASS: structure, references, version and {len(cases)} regression case definitions. Content/visual review still required.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
