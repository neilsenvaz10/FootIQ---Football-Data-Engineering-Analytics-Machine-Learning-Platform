import os, sys, re, collections
sys.path.insert(0, r"D:\Foot IQ\FootIQ_Dataset_Submission\_build")
import footballtxt as ft
import build_club_matches as b
RAW = r"D:\Foot IQ\FootIQ_Dataset_Submission\_raw_sources"
cnt = collections.Counter(); files = set(); 
for repo in ("austria","belgium","deutschland","england","espana","europe","italy","south-america","world"):
    for dp, dn, fn in os.walk(os.path.join(RAW, repo)):
        dn[:] = [d for d in dn if d != ".git"]
        for n in fn:
            full = os.path.join(dp, n); rel = os.path.relpath(full, RAW).replace("\\", "/")
            if not re.search(r"(2026|2025-26|2026-27)", rel): continue
            info = b.describe(rel)
            if info is None or info["std"][1] != "domestic_league": continue
            text = open(full, "rb").read().decode("utf-8", "replace")
            title, matches, issues = ft.parse_text(text, int(info["season"][:4]))
            for m in matches:
                r = m["res"]; d = str(m.get("date"))
                if d > "2026-09-20" and isinstance(r, dict) and r.get("status") == "scored":
                    cnt[d[:7]] += 1; files.add(rel)
print(cnt, len(files))
m0 = None
print(matches[0] if matches else None)
