#!/usr/bin/env python3
import os
import re

errors = []

for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root:
        continue
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                
                # Check for YAML front matter
                if content.startswith('---'):
                    lines = content.split('\n')
                    yaml_started = False
                    yaml_content = []
                    line_num = 0
                    
                    for i, line in enumerate(lines):
                        if line.strip() == '---':
                            if not yaml_started:
                                yaml_started = True
                            else:
                                break
                        elif yaml_started:
                            yaml_content.append((i+1, line))
                            line_num += 1
                    
                    # Check for unquoted colons in values
                    for ln, yl in yaml_content:
                        if ':' in yl:
                            # Skip keys (they have leading spaces or are at start)
                            stripped = yl.lstrip()
                            if stripped.startswith('#'):
                                continue
                            # If there's a colon not in quotes, it's a potential issue
                            if re.match(r'^\s*[^#\s]+:[^>\[\]{}"|\s]', yl):
                                errors.append(f'{path}:{ln} - "{yl.strip()}"')
            except Exception as e:
                errors.append(f'{path}: {e}')

if errors:
    print(f'Found {len(errors)} potential YAML issues:')
    for e in errors[:20]:
        print(e)
    if len(errors) > 20:
        print(f'... and {len(errors)-20} more')
else:
    print('No obvious YAML issues found in front matter')
