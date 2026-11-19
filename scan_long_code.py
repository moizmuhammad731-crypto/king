lines = open("Pink_Wheels_CEP_Report.md", encoding="utf-8").read().split("\n")
inside = False
block_start = 0
count = 0
for i, l in enumerate(lines):
    if l.startswith("```"):
        inside = not inside
        if inside:
            block_start = i + 1
        continue
    if inside and len(l) > 96:
        count += 1
        print(f"{i+1:5d} (block@{block_start}) len={len(l)}: {l[:110]}")
print("long lines:", count)
