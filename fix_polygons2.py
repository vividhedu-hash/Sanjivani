"""Direct polygon replacement script"""

with open('generate_report.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Manual replacements by line number (1-indexed -> 0-indexed)
replacements = {
    338: "        _poly(c, [w-10, h*0.15, w-16, h*0.18, w-16, h*0.12], fill=1, stroke=0)\n",
    407: "        _poly(c, [w*0.22, h*0.42, w*0.19, h*0.44, w*0.19, h*0.40], fill=1, stroke=0)\n",
    # line 418-419 (multiline): replace next 2 lines
    417: "        _poly(c, [w/2, h*0.95, w/2-3*mm, h*0.90, w/2+3*mm, h*0.90], fill=1, stroke=0)\n",
    418: "",  # delete the continuation line
    423: "        _poly(c, [w/2, h*0.30, w/2-3*mm, h*0.25, w/2+3*mm, h*0.25], fill=1, stroke=0)\n",
    609: "        _poly(c, pts, fill=1, stroke=0)\n",
    612: "        _poly(c, pts, fill=0, stroke=1)\n",
    771: "            _poly(c, [ax+3*mm, ay, ax, ay+2*mm, ax, ay-2*mm], fill=1, stroke=0)\n",
    782: "        _poly(c, [pelt_x, ny+bh, pelt_x-2*mm, ny+bh+5*mm, pelt_x+2*mm, ny+bh+5*mm], fill=1, stroke=0)\n",
}

for idx, new_line in replacements.items():
    if idx < len(lines):
        print(f"Line {idx+1}: {repr(lines[idx][:60])} -> {repr(new_line[:60])}")
        lines[idx] = new_line

# Handle the multi-line polygon calls at lines 466-469 and 628-631
# Check what's there
print("Line 466:", repr(lines[465][:80]))
print("Line 467:", repr(lines[466][:80]))
print("Line 628:", repr(lines[627][:80]))
print("Line 629:", repr(lines[628][:80]))

with open('generate_report.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Done basic replacements")
