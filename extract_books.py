# -*- coding: utf-8 -*-
"""Extract articles (مواد) from the penal-code book files into CSVs.

Columns: book, door, section, subject_number, subject_name, description
- Repealed (ملغاة) articles are skipped.
- An article runs from its (مادة) header to the next مادة/باب/فصل header,
  so mid-article blank lines do not truncate the description.
- Title vs body split is deterministic via an explicit multi-line-title set
  per book (the only titles that wrap to a 2nd line), since body text starts
  with too many different words to detect by keyword.
"""
import re
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(HERE, "source")
CSV_DIR = os.path.join(HERE, "csv")
TATWEEL = "ـ"

def norm(s):
    return s.replace(TATWEEL, "").replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")

ORD = {
    "الاول": 1, "الثاني": 2, "الثالث": 3, "الرابع": 4,
    "الخامس": 5, "السادس": 6, "السابع": 7, "الثامن": 8,
}

ARTICLE_RE = re.compile(r"^\(?\s*(?:مادة|ماده|أداة|اداة)?\s*\(?\s*(\d{3})\s*\)")
BAB_RE = re.compile(r"^الباب\s+(\S+)\s*$")
FASL_RE = re.compile(r"^الفصل\s+(\S+)\s*$")
MUKARRAR_RE = re.compile(r"^(مكرر(?:ة)?)\s*(\(\s*([ء-ي])?\s*\))?")
DASH = "–—-"

def collapse(s):
    return re.sub(r"\s+", " ", s).strip()

def is_malgha(rest):
    return "ملغا" in rest.replace(" ", "")

def parse_mukarrar(rest):
    m = MUKARRAR_RE.match(rest)
    if not m:
        return "", rest
    base = m.group(1)
    letter = m.group(3)
    label = base + (" (" + letter + ")" if letter else "")
    return label, rest[m.end():].strip()

# Articles whose title wraps onto a 2nd line (keyed by full subject_number string).
MULTILINE = {
    "2": {"171","172","173","178","180","185","197","198","199","208","211",
          "234","238","240","241","242","245","248","279","280","283","289",
          "299","303","310","315","325","329","331","332","334","335","336",
          "337","339","342","343","353","357"},
    "3": {"404","405","413","442","448","448 مكرر"},
    "4": {"485","489"},
}

BOOKS = [
    {"file": "الكتاب الثاني.txt",  "num": "2", "out": "book2_subjects.csv"},
    {"file": "الكتاب الثالث.txt",  "num": "3", "out": "book3_subjects.csv"},
    {"file": "الكتاب الرابع.txt",  "num": "4", "out": "book4_subjects.csv"},
]

def parse(path, book_num):
    with open(path, encoding="utf-8-sig") as f:
        lines = [ln.rstrip("\r\n") for ln in f]
    n = len(lines)
    ml = MULTILINE.get(book_num, set())
    door = None
    section = None
    rows = []
    i = 0
    while i < n:
        s = lines[i].strip()
        if s == "":
            i += 1
            continue
        key = norm(s)
        mb = BAB_RE.match(key)
        if mb and mb.group(1) in ORD:
            door = ORD[mb.group(1)]
            section = None
            i += 1
            continue
        mf = FASL_RE.match(key)
        if mf and mf.group(1) in ORD:
            section = ORD[mf.group(1)]
            i += 1
            continue
        ma = ARTICLE_RE.match(s)
        if ma:
            num = ma.group(1)
            rest = s[ma.end():].strip().lstrip(DASH + " ").strip()
            if is_malgha(rest):
                i += 1
                continue
            mk, title_part = parse_mukarrar(rest)
            title_part = title_part.lstrip(DASH + ": ").strip()
            subject_number = num + (" " + mk if mk else "")
            K = 2 if subject_number in ml else 1
            # gather all non-blank lines until the next مادة/باب/فصل header
            j = i + 1
            rest_lines = []
            while j < n:
                t = lines[j].strip()
                if t != "":
                    tk = norm(t)
                    if (BAB_RE.match(tk) and BAB_RE.match(tk).group(1) in ORD) or \
                       (FASL_RE.match(tk) and FASL_RE.match(tk).group(1) in ORD) or \
                       ARTICLE_RE.match(t):
                        break
                    rest_lines.append(t)
                j += 1
            cont = rest_lines[:K - 1]
            body = rest_lines[K - 1:]
            title = collapse(title_part + " " + " ".join(cont))
            rows.append({
                "book": book_num,
                "door": str(door) if door else "null",
                "section": str(section) if section else "null",
                "subject_number": subject_number,
                "subject_name": title,
                "description": collapse(" ".join(body)),
            })
            i = j
            continue
        i += 1
    return rows

def write_csv(rows, out_path):
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "book", "door", "section", "subject_number", "subject_name", "description"])
        w.writeheader()
        w.writerows(rows)

def main():
    os.makedirs(CSV_DIR, exist_ok=True)
    combined = []
    for b in BOOKS:
        rows = parse(os.path.join(SRC_DIR, b["file"]), b["num"])
        write_csv(rows, os.path.join(CSV_DIR,b["out"]))
        combined.extend(rows)
        base = [r["subject_number"] for r in rows if "مكرر" not in r["subject_number"]]
        mk = [r["subject_number"] for r in rows if "مكرر" in r["subject_number"]]
        nums = sorted(int(x) for x in base)
        gaps = [x for x in range(nums[0], nums[-1] + 1) if x not in set(nums)]
        print("book", b["num"], "->", b["out"], "| rows:", len(rows),
              "| base:", len(base), "| mukarrar:", len(mk),
              "| range:", nums[0], "-", nums[-1], "| repealed gaps:", gaps)
    write_csv(combined, os.path.join(CSV_DIR,"all_books_subjects.csv"))
    print("combined -> all_books_subjects.csv | rows:", len(combined))

    # New CSVs with مكرر rows removed (base-numbered articles only)
    def no_mk(rows):
        return [r for r in rows if "مكرر" not in r["subject_number"]]
    for b in BOOKS:
        rows = no_mk(parse(os.path.join(SRC_DIR, b["file"]), b["num"]))
        out = b["out"].replace(".csv", "_no_mukarrar.csv")
        write_csv(rows, os.path.join(CSV_DIR,out))
        print(out, "| rows:", len(rows))
    write_csv(no_mk(combined), os.path.join(CSV_DIR,"all_books_subjects_no_mukarrar.csv"))
    print("all_books_subjects_no_mukarrar.csv | rows:", len(no_mk(combined)))

if __name__ == "__main__":
    main()
