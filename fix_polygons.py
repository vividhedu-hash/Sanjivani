import re

with open('generate_report.py', 'r', encoding='utf-8') as f:
    content = f.read()

orig_count = content.count('c.polygon(')

# Replace c.polygon([...], fill=X, stroke=Y) -> _poly(c, [...], fill=X, stroke=Y)
# Multi-line safe pattern
pattern = r'c\.polygon\((\[(?:[^\[\]]*|\[.*?\])*\]),\s*(fill=\d+),\s*(stroke=\d+)\)'
replacement = r'_poly(c, \1, \2, \3)'
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

result_count = new_content.count('c.polygon(')
poly_count = new_content.count('_poly(c,')
print(f'Original polygon calls: {orig_count}')
print(f'Remaining c.polygon calls: {result_count}')
print(f'_poly calls added: {poly_count}')

with open('generate_report.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Done')
