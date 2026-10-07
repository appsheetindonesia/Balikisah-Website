#!/usr/bin/env python
"""9-check verification: the nine requirement documents + the built site chrome."""
import os
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPECTED = [
    "Market Requirements Document (MRD).md",
    "Customer Requirements Document (CRD).md",
    "Business Requirements Document (BRD).md",
    "Product Requirements Document (PRD) 18 Section.md",
    "User Interface Requirements Document (UIRD).md",
    "Functional Requirements Document (FRD).md",
    "Technical Requirements Document (TRD).md",
    "Quality Requirements Document (QRD).md",
    "Software Requirements Specification (SRS).md",
]

fail = []


def bad(msg):
    fail.append(msg)
    print("  FAIL " + msg)


def slug(text):
    t = text.strip().lower()
    t = re.sub(r"[`*_]", "", t)
    t = re.sub(r"[^a-z0-9\s-]", "", t)
    return re.sub(r"[\s-]+", "-", t).strip("-")


print("1) nama file")
present = sorted(f for f in os.listdir(ROOT) if f.endswith(".md"))
for name in EXPECTED:
    if not os.path.isfile(os.path.join(ROOT, name)):
        bad("missing " + name)
print("   %d/%d ditemukan" % (len(EXPECTED) - len([f for f in fail if f.startswith('missing')]),
                              len(EXPECTED)))

print("2) UTF-8 valid + isi terbaca")
docs = {}
for name in EXPECTED:
    path = os.path.join(ROOT, name)
    if not os.path.isfile(path):
        continue
    try:
        docs[name] = open(path, encoding="utf-8").read()
    except UnicodeDecodeError as exc:
        bad("%s tidak valid UTF-8: %s" % (name, exc))
print("   %d dokumen terbaca" % len(docs))

print("3) tidak ada karakter CJK / Cyrillic / Hiragana nyasar")
suspicious = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af\u0400-\u04ff]")
for name, text in docs.items():
    hits = suspicious.findall(text)
    if hits:
        bad("%s memuat %d karakter asing: %s" % (name, len(hits), "".join(sorted(set(hits)))[:20]))
print("   bersih")

print("4) tautan silang antar dokumen")
# Nama file memuat tanda kurung, jadi kurung dalam path harus ikut tertangkap.
MD_LINK = re.compile(r"\]\(((?:[^()\s]|\([^()]*\))*?\.md)(#[^()\s]*)?\)")
links = broken = 0
for name, text in docs.items():
    for target, _frag in MD_LINK.findall(text):
        links += 1
        t = unquote(target.strip())
        if not os.path.isfile(os.path.join(ROOT, t)):
            broken += 1
            bad("%s -> tautan rusak: %s" % (name, t))
print("   %d tautan diperiksa, %d rusak" % (links, broken))

print("5) anchor internal valid")
anchors = {}
for name, text in docs.items():
    set_ = set()
    for line in text.splitlines():
        m = re.match(r"^#{1,6}\s+(.*)$", line)
        if m:
            set_.add(slug(m.group(1)))
    anchors[name] = set_
internal = bad_anchor = 0
for name, text in docs.items():
    for target, frag in MD_LINK.findall(text):
        internal += 1
        owner = unquote(target.strip()) or name
        if frag.strip() and unquote(frag.strip().lstrip("#").lower()) not in anchors.get(owner, set()):
            bad_anchor += 1
            bad("%s -> anchor hilang di %s: #%s" % (name, owner or name, frag))
    # anchor ke dokumen sendiri: [](#slug)
    for frag in re.findall(r"\]\(#([^)]+)\)", text):
        internal += 1
        if unquote(frag.strip().lstrip("#").lower()) not in anchors[name]:
            bad_anchor += 1
            bad("%s -> anchor sendiri hilang: #%s" % (name, frag))
print("   %d anchor internal, %d hilang" % (internal, bad_anchor))

print("6) PRD punya tepat bagian 1..18")
prd = docs.get("Product Requirements Document (PRD) 18 Section.md", "")
nums = [int(m.group(1)) for m in re.finditer(r"^##\s+(\d+)\.", prd, re.M)]
if nums != list(range(1, 19)):
    bad("PRD urutan bagian = %s" % nums)
print("   bagian: %s" % nums)

print("7) baris tabel markdown tidak rusak")
broken_rows = 0
for name, text in docs.items():
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        if not line.strip().startswith("|"):
            continue
        if not line.strip().endswith("|"):
            broken_rows += 1
            bad("%s:%d baris tabel tidak diakhiri '|'" % (name, i))
        # jumlah sel harus sama dengan baris separator di atas
        if i > 1 and lines[i - 2].strip().startswith("|"):
            def cells(row):
                return len([c for c in re.split(r"(?<!\\)\|", row.strip().strip("|"))])
            if cells(lines[i - 2]) != cells(line):
                broken_rows += 1
                bad("%s:%d jumlah sel tidak cocok (%d vs %d)"
                    % (name, i, cells(lines[i - 2]), cells(line)))
print("   %d baris tabel rusak" % broken_rows)

print("8) pagar kode seimbang + token UIRD terukur ada")
for name, text in docs.items():
    if text.count("```") % 2:
        bad("%s: pagar kode tidak seimbang" % name)
uird = docs.get("User Interface Requirements Document (UIRD).md", "")
TOKENS = ["#F7F0DD", "#180E00", "#73706A", "#6F5138", "#94542E", "#8F5432",
          "#E7D6BC", "#54432C", "#E5DCC6", "#EDE7DA", "1120", "78px", "**38**",
          "11px", "28px", "14px", "259", "345", "3/2", "999",
          "sepia(.45)", "--card-pad", "--card-gap-title", "--card-gap-excerpt"]
missing = [t for t in TOKENS if t not in uird]
if missing:
    bad("token UIRD hilang: %s" % missing)
print("   %d/%d token terukur ada" % (len(TOKENS) - len(missing), len(TOKENS)))

print("9) chrome situs bebas label lama (Contact us / Bali Kisah / Kenajaan)")
chrome_script = os.path.join(ROOT, ".freebuff", "verify_chrome.py")
if not os.path.isfile(chrome_script):
    bad("skrip .freebuff/verify_chrome.py tidak ditemukan")
else:
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run([sys.executable, chrome_script], capture_output=True,
                          text=True, encoding="utf-8", errors="replace", env=env)
    output = ((proc.stdout or "") + (proc.stderr or "")).strip()
    for out_line in output.splitlines():
        print("   " + out_line.encode("ascii", "replace").decode("ascii"))
    if proc.returncode != 0:
        bad("chrome situs memuat label lama atau tidak terbaca (lihat baris GAGAL di atas)")

total_lines = sum(t.count("\n") + 1 for t in docs.values())
print()
print("total baris dokumen: %d" % total_lines)
print("HASIL: %s (%d masalah)" % ("LULUS" if not fail else "GAGAL", len(fail)))
sys.exit(1 if fail else 0)
