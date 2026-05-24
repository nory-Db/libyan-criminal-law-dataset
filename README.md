# Libyan Criminal Law — Dataset / القانون الجنائي الليبي — مجموعة بيانات

> *(English below — النسخة العربية في الأسفل)*

---

## English

Structured **CSV datasets** extracted from the text of the **Libyan Criminal Law** (the Penal Code — قانون العقوبات), covering Books Two, Three, and Four. Each article (مادة) is turned into a row with its book, door, section, number, title, and full text — ready for search, analysis, or import into a database/spreadsheet.

### Source

Plain‑text files of the code in `source/`:

| File | Book | Subject |
|---|---|---|
| `الكتاب الثاني.txt` | Book 2 | Felonies & misdemeanours against the public interest |
| `الكتاب الثالث.txt` | Book 3 | Crimes against individuals |
| `الكتاب الرابع.txt` | Book 4 | Other misdemeanours & contraventions |

### Repository layout

```
.
├── README.md
├── extract_books.py        # the parser that produces the CSVs
├── source/                 # original plain-text code (Arabic)
└── csv/                    # generated datasets (UTF-8 with BOM)
```

### CSV columns

| Column | Meaning |
|---|---|
| `book` | Book number — `2`, `3`, or `4` |
| `door` | Door (الباب) number within the book |
| `section` | Section (الفصل) number, or `null` when the door has no sections |
| `subject_number` | Article (مادة) number, e.g. `220`; bis articles keep their label, e.g. `227 مكررة`, `448 مكرر` |
| `subject_name` | Article title / heading |
| `description` | Full article text |

### Files in `csv/`

Two variants are provided. **Repealed (ملغاة) articles are excluded from all files.**

| File | Rows | Contents |
|---|---|---|
| `book2_subjects.csv` | 199 | Book 2, incl. مكرر |
| `book3_subjects.csv` | 102 | Book 3, incl. مكرر |
| `book4_subjects.csv` | 38 | Book 4 |
| `all_books_subjects.csv` | 339 | All books combined, incl. مكرر |
| `book2_subjects_no_mukarrar.csv` | 191 | Book 2, base articles only |
| `book3_subjects_no_mukarrar.csv` | 90 | Book 3, base articles only |
| `book4_subjects_no_mukarrar.csv` | 38 | Book 4, base articles only |
| `all_books_subjects_no_mukarrar.csv` | 319 | All books combined, base articles only |

- **`*_no_mukarrar.csv`** drop the *bis* (مكرر / مكررة) articles, keeping only base‑numbered articles.
- Articles covered: **165–507** (Book 2: 165–367, Book 3: 368–466, Book 4: 467–507).

### Regenerate

Requires Python 3 (standard library only):

```bash
python extract_books.py
```

It reads the text files from `source/` and writes every CSV into `csv/`.

### Notes & disclaimer

- The CSVs are produced from plain‑text files that contain occasional OCR‑style artifacts (stray characters, elongation/tatweel). The structure (book/door/section/number/title) is faithful, but **this is an unofficial dataset for reference and research — verify against the official gazette before any legal use.**
- Files are saved as UTF‑8 with BOM so Arabic displays correctly in Excel.

---

## العربية

مجموعات **بيانات CSV منظمة** مستخرجة من نص **القانون الجنائي الليبي (قانون العقوبات)**، وتشمل الكتاب الثاني والثالث والرابع. كل مادة تتحوّل إلى صف يحتوي على الكتاب والباب والفصل ورقم المادة وعنوانها ونصها الكامل — جاهزة للبحث أو التحليل أو الاستيراد إلى قاعدة بيانات أو جدول.

### المصدر

ملفات نصية للقانون في مجلد `source/`:

| الملف | الكتاب | الموضوع |
|---|---|---|
| `الكتاب الثاني.txt` | الكتاب الثاني | الجنايات والجنح ضد المصلحة العامة |
| `الكتاب الثالث.txt` | الكتاب الثالث | الجرائم ضد آحاد الناس |
| `الكتاب الرابع.txt` | الكتاب الرابع | الجنح الأخرى والمخالفات |

### هيكل المستودع

```
.
├── README.md
├── extract_books.py        # السكربت الذي يُنتج ملفات CSV
├── source/                 # النص الأصلي للقانون (بالعربية)
└── csv/                    # البيانات المُولّدة (UTF-8 مع BOM)
```

### أعمدة ملف CSV

| العمود | المعنى |
|---|---|
| `book` | رقم الكتاب — `2` أو `3` أو `4` |
| `door` | رقم الباب داخل الكتاب |
| `section` | رقم الفصل، أو `null` إذا لم يكن للباب فصول |
| `subject_number` | رقم المادة، مثل `220`؛ والمواد المكرّرة تحتفظ بوصفها مثل `227 مكررة` و`448 مكرر` |
| `subject_name` | عنوان المادة |
| `description` | النص الكامل للمادة |

### الملفات في مجلد `csv/`

تتوفّر نسختان. **المواد الملغاة مستبعدة من جميع الملفات.**

| الملف | عدد الصفوف | المحتوى |
|---|---|---|
| `book2_subjects.csv` | 199 | الكتاب الثاني، يشمل المكرّر |
| `book3_subjects.csv` | 102 | الكتاب الثالث، يشمل المكرّر |
| `book4_subjects.csv` | 38 | الكتاب الرابع |
| `all_books_subjects.csv` | 339 | كل الكتب مجمّعة، تشمل المكرّر |
| `book2_subjects_no_mukarrar.csv` | 191 | الكتاب الثاني، المواد الأساسية فقط |
| `book3_subjects_no_mukarrar.csv` | 90 | الكتاب الثالث، المواد الأساسية فقط |
| `book4_subjects_no_mukarrar.csv` | 38 | الكتاب الرابع، المواد الأساسية فقط |
| `all_books_subjects_no_mukarrar.csv` | 319 | كل الكتب مجمّعة، المواد الأساسية فقط |

- ملفات **`*_no_mukarrar.csv`** تحذف المواد المكرّرة وتُبقي فقط المواد ذات الأرقام الأساسية.
- المواد المشمولة: **165–507** (الكتاب الثاني 165–367، الثالث 368–466، الرابع 467–507).

### إعادة التوليد

يتطلّب بايثون 3 (المكتبة القياسية فقط):

```bash
python extract_books.py
```

يقرأ السكربت الملفات النصية من `source/` ويكتب جميع ملفات CSV في `csv/`.

### ملاحظات وإخلاء مسؤولية

- أُنتجت الملفات من نصوص قد تحتوي على أخطاء ناتجة عن المسح الضوئي (أحرف زائدة، تطويل). البنية (الكتاب/الباب/الفصل/الرقم/العنوان)  لكن **هذه بيانات غير رسمية للاطّلاع والبحث — يُرجى التحقق من الجريدة الرسمية قبل أي استخدام قانوني.**
- حُفظت الملفات بترميز UTF-8 مع BOM لتظهر العربية بشكل صحيح في Excel.
