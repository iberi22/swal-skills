#!/usr/bin/env python3
import os
import re

removed_count = 0
error_count = 0

for root, dirs, files in os.walk('.'):
    # Skip certain directories
    dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'skills', 'bench', 'docs', '.git']]
    
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                
                # Check if it has YAML front matter with problematic content
                if content.startswith('---'):
                    # Find the end of YAML front matter
                    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                    if match:
                        yaml_content = match.group(1)
                        # Check for problematic patterns
                        if '\\n' in yaml_content or re.search(r'<example>|</example>', yaml_content, re.IGNORECASE):
                            # Remove the YAML front matter
                            new_content = content[match.end():]
                            # Also remove any remaining yaml at the end (like "color:", "tools:", etc.)
                            new_content = re.sub(r'^(color|tools|type):.*\n', '', new_content, flags=re.MULTILINE)
                            new_content = new_content.lstrip('\n')
                            
                            with open(path, 'w', encoding='utf-8') as fp:
                                fp.write(new_content)
                            
                            removed_count += 1
                            print(f'Fixed: {path}')
            except Exception as e:
                error_count += 1
                print(f'Error: {path}: {e}')

print(f'\nDone: {removed_count} files fixed, {error_count} errors')
