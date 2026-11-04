#!/usr/bin/env python3
"""
check_suite.py - the Week 07 checker. DO NOT EDIT: the grader runs its own copy over your files.

    python tests/check_suite.py          # from inside week-07/
    python tests/check_suite.py --json   # machine-readable, for the grading pipeline

What it checks (33 checks):

    A1-A5    your project in app/: exported, canBook extracted into a booking module, the page
             uses it, the export is clean, Vitest is installed
    S1-S10   your FINAL suite (booking.test.* beside the module): the real function imported,
             nothing mocked or skipped, T01-T14 + AC5 + X1 + X2 with the plan's inputs and exact
             expected decisions, fixed time, and the first suite kept in suites/first/
    R1-R3    the runs you pasted into lab-report.md: first run, final run, Vitest version
    M1-M4    the three deliberate defects (mutants) and their runs
    U1-U3    the manual UI checks and their screenshots
    L1-L8    lab-report.md has its sections filled in

It never runs your tests and never executes your code. It reads files. The terminal output you
paste is YOUR evidence: R2 checks that it is consistent with the suite you committed, and the
grader may run your suite again. A clean run is the floor, not the grade.

Verdicts:
    PASS   the check found what it was looking for
    FAIL   the content is there but wrong, or not enough of it
    ERROR  it could not check: a file, a folder or a section is missing

Exit codes: 0 = no FAIL and no ERROR - 1 = at least one FAIL or ERROR - 3 = wrong directory.
Standard library only.
"""

import argparse
import hashlib
import json
import os
import re
import struct
import sys

APP = "app"
FIRST = os.path.join("suites", "first")
EVIDENCE = "evidence"
REPORT = "lab-report.md"

MAX_EXPORT_MB = 5
MIN_IMAGE_BYTES = 3000
MIN_TESTS = 17
WORDS_MIN, WORDS_MAX = 120, 180
EXTRACT_MIN = 40

CODE_EXT = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".mts", ".cts", ".vue", ".svelte", ".html")
IGNORED_DIRS = (".git", ".bolt", ".vscode", ".idea", "__pycache__", "node_modules", "dist", "coverage")
MODULE_NAMES = tuple("booking" + e for e in (".ts", ".js", ".tsx", ".jsx", ".mts", ".mjs"))

# The plan: README section 6 and the deck's Task #02. Default fixture: now 540, not blocked,
# bookings [{start: 600, end: 660}]. (id, numbers that must appear in the test, expected, extra)
PLAN = [
    ("T01", (660, 720), True, None),
    ("T02", (540, 570), False, None),
    ("T03", (720,), False, None),
    ("T04", (750, 720), False, None),
    ("T05", (1380, 1441), False, None),
    ("T06", (720, 840), True, None),
    ("T07", (720, 841), False, None),
    ("T08", (570, 600), True, None),
    ("T09", (630, 690), False, None),
    ("T10", (570, 690), False, None),
    ("T11", (615, 645), False, None),
    ("T12", (600, 660), False, None),
    ("T13", (660, 720), False, "blocked"),
    ("T14", (630, 690), True, "empty"),
]
MUTANTS = [("M1", "duration >= 120 rejected"), ("M2", "touching endpoints as overlap"),
           ("M3", "no blocked-room rejection")]
UI = ["U1", "U2", "U3", "U4", "U5"]

# Fixed sentences of the deck's two prompts (slides 16 and 21). Compared after normalising
# whitespace, quotes and dashes, so line wrapping in your paste does not matter.
GENERATION_PROMPT = ("Generate tests for the existing booking function using Vitest.",
                     "Import the real function used by the page.",
                     "Assert exact decisions and unchanged booking data.",
                     "We will run the tests ourselves.")
IMPROVEMENT_PROMPT = ("Identify incorrect expectations, weak assertions, duplicated cases, and missing boundaries.",
                      "Improve the tests without changing correct expectations to match buggy behavior.",
                      "Separate test repairs from implementation fixes.")

TITLES = {
    "A1": "project exported to app/",
    "A2": "booking module exports canBook",
    "A3": "the page imports and calls canBook",
    "A4": "exports are clean: no node_modules, no .env, under %d MB" % MAX_EXPORT_MB,
    "A5": "Vitest is in package.json",
    "S1": "final suite beside the module imports vitest and the real canBook",
    "S2": "nothing mocked, skipped, focused or table-driven",
    "S3": "%d tests or more in the final suite" % MIN_TESTS,
    "S4": "T01-T14 each named in a test",
    "S5": "T01-T14 assert the exact expected decision",
    "S6": "T01-T14 use the plan's inputs",
    "S7": "AC5: bookings compared before and after an Available call",
    "S8": "your own cases X1 and X2 named in tests",
    "S9": "fixed time: no Date or Math.random in the suite",
    "S10": "first suite kept in suites/first/, final differs from it",
    "R1": "report 6.1: the first run, pasted",
    "R2": "report 6.3: the final run, all passing, same suite",
    "R3": "Vitest version recorded",
    "M1": "M1 (>= 120) tried and explained",
    "M2": "M2 (touching as overlap) tried and explained",
    "M3": "M3 (no blocked rejection) tried and explained",
    "M4": "report 7: the three mutant runs, pasted",
    "U1": "five UI screenshots: evidence/ui-1 ... ui-5",
    "U2": "ui-4 taken at phone width (portrait)",
    "U3": "report 8: five UI checks observed and judged",
    "L1": "report 1: project, assistant, model, where, command",
    "L2": "report 2: the function before, and the extraction in %d+ words" % EXTRACT_MIN,
    "L3": "report 3: a reason for every case, X1 and X2 complete",
    "L4": "report 4: generation prompt as sent, and the answer",
    "L5": "report 5: two review decisions or more",
    "L6": "report 6: failures diagnosed, improvement prompt as sent",
    "L7": "report 9.2: first and improved suites compared",
    "L8": "report 10: conclusion of %d-%d words" % (WORDS_MIN, WORDS_MAX),
}
ORDER = list(TITLES)


# --------------------------------------------------------------------------- small helpers


class Results:
    def __init__(self):
        self.rows = []

    def add(self, cid, verdict, message):
        self.rows.append({"id": cid, "title": TITLES[cid], "verdict": verdict, "message": message})

    def counts(self):
        return {v: sum(1 for r in self.rows if r["verdict"] == v) for v in ("PASS", "FAIL", "ERROR")}


def read(path):
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except (OSError, TypeError):
        return None


def rel(path):
    return path.replace(os.sep, "/") if path else path


def walk_files(root):
    for here, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS)
        for name in sorted(files):
            yield os.path.join(here, name)


def project_root(folder):
    """The project: the folder itself, or the one sub-folder a downloaded zip unpacks into."""
    if not os.path.isdir(folder):
        return None
    candidates = [folder] + sorted(os.path.join(folder, d) for d in os.listdir(folder)
                                   if os.path.isdir(os.path.join(folder, d)) and d not in IGNORED_DIRS)
    for c in candidates:
        if os.path.isfile(os.path.join(c, "package.json")) or os.path.isfile(os.path.join(c, "index.html")):
            return c
    return None


def is_test_file(path):
    return bool(re.search(r"\.(test|spec)\.[cm]?[jt]sx?$", os.path.basename(path)))


def norm(text):
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"[‐-―]", "-", text)
    return re.sub(r"\s+", " ", text).strip()


def strip_js_comments(src):
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    return re.sub(r"(?m)(^|[^:'\"`\\])//.*$", r"\1", src)


def image_info(path):
    """(width, height) for a real PNG or JPEG, else None."""
    try:
        data = open(path, "rb").read()
    except OSError:
        return None
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) > 24:
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            length = struct.unpack(">H", data[i + 2:i + 4])[0]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return (w, h)
            i += 2 + length
    return None


def find_image(stem):
    if not os.path.isdir(EVIDENCE):
        return None
    for name in sorted(os.listdir(EVIDENCE)):
        base, ext = os.path.splitext(name)
        if base.lower() == stem.lower() and ext.lower() in (".png", ".jpg", ".jpeg"):
            return os.path.join(EVIDENCE, name)
    return None


def image_problem(path):
    if path is None:
        return "missing"
    if os.path.getsize(path) < MIN_IMAGE_BYTES:
        return "%s is too small to be a screenshot" % rel(path)
    if image_info(path) is None:
        return "%s is not a real PNG or JPEG" % rel(path)
    return None


# --------------------------------------------------------------------------- reading a test file

TEST_CALL = re.compile(r"\b(?:test|it)((?:\.\w+)*)\s*\(\s*(['\"`])((?:\\.|(?!\2).)*?)\2", re.S)


def tests_in(src):
    """[(title, modifiers, block)] - one per test(...) / it(...) call, in order."""
    src = strip_js_comments(src or "")
    found = list(TEST_CALL.finditer(src))
    out = []
    for i, m in enumerate(found):
        end = found[i + 1].start() if i + 1 < len(found) else len(src)
        out.append((m.group(3), m.group(1) or "", src[m.start():end]))
    return out


def booleans_asserted(block):
    """The exact boolean values a test block asserts with toBe/toEqual/toStrictEqual."""
    vals = set()
    for m in re.finditer(r"(\.not)?\.(?:toBe|toEqual|toStrictEqual)\(\s*(true|false)\s*\)", block):
        if not m.group(1):
            vals.add(m.group(2) == "true")
    return vals


def without_assertions(block):
    return re.sub(r"\.(?:not\.)?to\w*\([^()]*\)", " ", block)


def ids_in(title):
    return set(re.findall(r"\b(T0[1-9]|T1[0-4]|X[12]|AC5)\b", title))


def vitest_summaries(text):
    """Every 'Tests  1 failed | 16 passed (17)' line in text, as dicts."""
    out = []
    for line in (text or "").splitlines():
        m = re.match(r"^\s*Tests\s+(.*\(\s*(\d+)\s*\))\s*$", line)
        if not m:
            continue
        body = m.group(1)
        get = lambda word: int((re.search(r"(\d+)\s+%s" % word, body) or [0, 0])[1])
        out.append({"failed": get("failed"), "passed": get("passed"), "skipped": get("skipped"),
                    "todo": get("todo"), "total": int(m.group(2))})
    return out


def vitest_version(text):
    m = re.search(r"\bRUN\s+v(\d+\.\d+\.\d+)", text or "")
    return m.group(1) if m else None


# --------------------------------------------------------------------------- lab-report.md parsing

PLACEHOLDER = re.compile(r"\(paste here\)|\(write here[^)]*\)|^<.*>$|yes / no|"
                         r"accept / revise / reject|Detected / Survived|Pass / Fail / Not testable", re.I)


def sections(text):
    """{'1': body, '6.1': body, ...} - split on the numbered '## N.' and '### N.M' headings."""
    out, current = {}, None
    for line in text.splitlines():
        m = re.match(r"^#{2,3}\s+(\d+(?:\.\d+)?)[.\s]", line)
        if m:
            current = m.group(1)
            out[current] = []
            top = current.split(".")[0]
            if top != current:
                out.setdefault(top, [])
        elif current is not None:
            out[current].append(line)
            top = current.split(".")[0]
            if top != current:
                out[top].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def table_rows(body):
    rows, lines = [], [l.strip() for l in (body or "").splitlines()]
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.match(r"^:?-{2,}:?$", c) for c in cells if c) and any(cells):
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if nxt.startswith("|") and re.match(r"^\|[\s:|-]+\|?$", nxt):
            continue
        rows.append(cells)
    return rows


def useful(cell):
    cell = re.sub(r"<!--.*?-->", "", cell or "").strip()
    return bool(cell) and not PLACEHOLDER.search(cell)


def blocks(body):
    return re.findall(r"```[^\n]*\n(.*?)```", body or "", re.S)


def real_blocks(body, min_lines=2):
    return [b for b in blocks(body)
            if len([l for l in b.splitlines() if l.strip()]) >= min_lines and not PLACEHOLDER.search(b)]


def strip_comments(body):
    return re.sub(r"<!--.*?-->", " ", body or "", flags=re.S)


def word_count(body):
    body = strip_comments(body)
    body = re.sub(r"```.*?```", " ", body, flags=re.S)
    body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith((">", "|", "#")))
    return len(re.findall(r"[^\W_]+(?:['’-][^\W_]+)*", body))


def after_marker(body, marker="Write below this line"):
    return body.split(marker, 1)[1] if marker in (body or "") else (body or "")


def row_by_id(rows, rid):
    for cells in rows:
        if cells and cells[0].strip().upper() == rid.upper():
            return cells
    return None


def cell_word(cell, words):
    cell = re.sub(r"<!--.*?-->", "", cell or "").strip().strip("*").strip().lower()
    for w in words:
        if cell == w.lower():
            return w
    return None


# --------------------------------------------------------------------------- A: the project


def find_module(root):
    hits = [p for p in walk_files(root) if os.path.basename(p) in MODULE_NAMES]
    hits.sort(key=lambda p: (0 if "/src/" in rel(p) + "/" else 1, len(p)))
    return hits[0] if hits else None


def find_suite(module):
    if not module:
        return None
    folder = os.path.dirname(module)
    for name in sorted(os.listdir(folder)):
        if re.match(r"^booking\.(test|spec)\.[cm]?[jt]sx?$", name):
            return os.path.join(folder, name)
    return None


def check_project(res, measured):
    root = project_root(APP)
    measured["app_root"] = rel(root)
    sources = [p for p in walk_files(root) if p.lower().endswith(CODE_EXT)] if root else []

    # A1
    if root and sources:
        res.add("A1", "PASS", "%s: %d source files" % (rel(root), len(sources)))
    else:
        res.add("A1", "ERROR", "no package.json or index.html in app/ - copy your project (source only) "
                               "there" if not root else "app/ has no source files")

    # A2
    module = find_module(root) if root else None
    measured["module"] = rel(module)
    module_src = strip_js_comments(read(module) or "") if module else ""
    exports = bool(re.search(r"\bexport\s+(?:async\s+)?function\s+canBook\b|\bexport\s+(?:const|let)\s+canBook\b"
                             r"|\bexport\s*\{[^}]*\bcanBook\b", module_src))
    if not root:
        res.add("A2", "ERROR", "no project in app/")
    elif not module:
        res.add("A2", "ERROR", "no booking.ts / booking.js in the project - extract the decision into it (Task 1)")
    else:
        res.add("A2", "PASS" if exports else "FAIL",
                "%s exports canBook" % rel(module) if exports
                else "%s does not export canBook - write: export function canBook({ start, end, now, blocked, "
                     "bookings })" % rel(module))

    # A3
    users = []
    if module:
        imp = re.compile(r"import\s*\{[^}]*\bcanBook\b[^}]*\}\s*from\s*['\"][^'\"]*\bbooking(?:\.[cm]?[jt]sx?)?['\"]")
        for p in sources:
            if p == module or is_test_file(p):
                continue
            src = strip_js_comments(read(p) or "")
            if imp.search(src) and re.search(r"\bcanBook\s*\(", src):
                users.append(rel(p))
    measured["page_uses"] = users
    if not module:
        res.add("A3", "ERROR", "no booking module to look for")
    else:
        res.add("A3", "PASS" if users else "FAIL",
                "called from " + ", ".join(users[:3]) if users
                else "no page file imports canBook from the booking module and calls it - the deck: "
                     "\"The page must use it.\"")

    # A4
    problems = []
    for folder in (APP, "suites"):
        if not os.path.isdir(folder):
            continue
        size = 0
        for here, dirs, names in os.walk(folder):
            if "node_modules" in dirs:
                problems.append("%s contains node_modules/ - delete it, it is not your work" % rel(here))
                dirs.remove("node_modules")
            for n in names:
                if n == ".env" or n.startswith(".env."):
                    problems.append("%s/%s must not be committed" % (rel(here), n))
                try:
                    size += os.path.getsize(os.path.join(here, n))
                except OSError:
                    pass
        if size > MAX_EXPORT_MB * 1024 * 1024:
            problems.append("%s/ is %.1f MB - commit source files only" % (folder, size / 1048576.0))
    if not root:
        res.add("A4", "ERROR", "nothing to check until app/ holds the project")
    else:
        res.add("A4", "FAIL" if problems else "PASS", "; ".join(problems) if problems else "clean")

    # A5
    pkg = read(os.path.join(root, "package.json")) if root else None
    if pkg is None:
        res.add("A5", "ERROR", "no app/package.json")
    else:
        try:
            data = json.loads(pkg)
            deps = dict(data.get("devDependencies") or {}, **(data.get("dependencies") or {}))
            ok = "vitest" in deps
            measured["vitest_declared"] = deps.get("vitest")
            res.add("A5", "PASS" if ok else "FAIL",
                    "vitest %s" % deps["vitest"] if ok else "vitest is not in package.json - install it: npm install -D vitest")
        except ValueError:
            res.add("A5", "FAIL", "app/package.json is not valid JSON")
    return root, module, sources


# --------------------------------------------------------------------------- S: the suites


def check_suite(res, measured, root, module, sources):
    suite = find_suite(module)
    measured["suite"] = rel(suite)
    src = read(suite) if suite else None
    tests = tests_in(src) if src else []
    titles = [t for t, _, _ in tests]
    measured["tests_final"] = len(tests)
    measured["test_titles"] = titles

    # all tests in the project, for comparing with the pasted run (R2)
    total = 0
    for p in (sources or []):
        if is_test_file(p):
            total += len(tests_in(read(p) or ""))
    measured["tests_in_project"] = total

    def need_suite(cid):
        if suite is None:
            res.add(cid, "ERROR", "no booking.test.ts / booking.test.js beside %s" % (rel(module) or "the booking module"))
            return False
        return True

    # S1
    if need_suite("S1"):
        clean = strip_js_comments(src)
        probs = []
        if not re.search(r"from\s*['\"]vitest['\"]", clean):
            probs.append("import { test, expect } from 'vitest'")
        if not re.search(r"import\s*\{[^}]*\bcanBook\b[^}]*\}\s*from\s*['\"]\./booking(?:\.[cm]?[jt]sx?)?['\"]", clean):
            probs.append("import { canBook } from './booking' - the real module, not a copy")
        res.add("S1", "FAIL" if probs else "PASS",
                "the suite needs: " + "; ".join(probs) if probs else "%s imports vitest and ./booking" % rel(suite))

    # S2
    if need_suite("S2"):
        clean = strip_js_comments(src)
        bad = []
        if re.search(r"\b(?:vi|jest)\.(?:mock|doMock|spyOn|fn)\s*\(", clean):
            bad.append("a mock or spy (vi.mock / vi.fn / vi.spyOn) - the deck: never mock the booking function")
        mods = sorted(set(m for _, m, _ in tests if m))
        for m in mods:
            if re.search(r"\.(skip|only|todo|fails|skipIf|runIf)\b", m):
                bad.append("test%s" % m)
            if ".each" in m:
                bad.append("test%s - write one test per case so every ID has its own name" % m)
        if re.search(r"\b(?:test|it|describe)\.each\b", clean) and not any(".each" in b for b in bad):
            bad.append("test.each / it.each - write one test per case so every ID has its own name")
        if re.search(r"\b(?:describe|suite)\.(?:skip|only|todo)\b|\bx(?:it|test|describe)\s*\(", clean):
            bad.append("a skipped or focused describe block")
        res.add("S2", "FAIL" if bad else "PASS", "; ".join(bad) if bad else "real function, every test runs")

    # S3
    if need_suite("S3"):
        res.add("S3", "PASS" if len(tests) >= MIN_TESTS else "FAIL",
                "%d tests" % len(tests) + ("" if len(tests) >= MIN_TESTS else
                                           " - T01-T14, the AC5 test and your two cases make %d" % MIN_TESTS))

    # S4-S6
    by_id = {}
    for title, _, block in tests:
        for i in ids_in(title):
            by_id.setdefault(i, []).append(block)
    missing = [pid for pid, _, _, _ in PLAN if pid not in by_id]
    if need_suite("S4"):
        res.add("S4", "FAIL" if missing else "PASS",
                "no test named " + ", ".join(missing) + " - put the ID in the test title, e.g. 'T05 AC1: ...'"
                if missing else "T01-T14 present")
    wrong, weak, inputs = [], [], []
    for pid, numbers, expected, extra in PLAN:
        if pid not in by_id:
            continue
        block = " ".join(by_id[pid])
        vals = booleans_asserted(block)
        if not vals:
            weak.append(pid)
        elif vals != {expected}:
            wrong.append("%s asserts %s" % (pid, "/".join(sorted(str(v).lower() for v in vals))))
        bare = without_assertions(block)
        ok = all(re.search(r"(?<![\w.])%d(?![\w.])" % n, bare) for n in numbers)
        if extra == "blocked":
            ok = ok and bool(re.search(r"\bblocked\s*[:=]\s*true\b|,\s*true\s*[,)]", bare))
        if extra == "empty":
            ok = ok and bool(re.search(r"\[\s*\]", bare))
        if not ok:
            inputs.append(pid)
    if need_suite("S5"):
        if missing and len(missing) == len(PLAN):
            res.add("S5", "ERROR", "no T test to read")
        else:
            probs = []
            if wrong:
                probs.append("wrong expected decision: " + ", ".join(wrong) + " - the plan's Expected comes from the ACs")
            if weak:
                probs.append("no exact .toBe(true) / .toBe(false) in " + ", ".join(weak)
                             + " (toBeTruthy, toBeDefined or 'no exception' let wrong answers pass)")
            res.add("S5", "FAIL" if probs else "PASS", "; ".join(probs) if probs else "exact decisions, as planned")
    measured["wrong_expectations"] = [w.split()[0] for w in wrong]
    if need_suite("S6"):
        if missing and len(missing) == len(PLAN):
            res.add("S6", "ERROR", "no T test to read")
        else:
            res.add("S6", "FAIL" if inputs else "PASS",
                    "the input is not the plan's in " + ", ".join(inputs) + " (start-end from section 3; T13 blocked, T14 no bookings)"
                    if inputs else "inputs as planned")

    # S7
    if need_suite("S7"):
        ac5 = [b for t, _, b in tests if "AC5" in ids_in(t)]
        good = [b for b in ac5 if True in booleans_asserted(b)
                and re.search(r"bookings", b)
                and re.search(r"JSON\.stringify|\.to(?:Strict)?Equal\(|structuredClone|\.toBe\(\s*before", b)]
        if not ac5:
            res.add("S7", "FAIL", "no test named AC5 - the deck: add an AC5 data-preservation test")
        else:
            res.add("S7", "PASS" if good else "FAIL",
                    "AC5 test compares the bookings after an Available call" if good
                    else "the AC5 test must call canBook on an AVAILABLE request (.toBe(true)) and then compare the "
                         "bookings with a copy taken before (JSON.stringify or toEqual) - a rejected request may "
                         "never reach the code that changes them")

    # S8
    if need_suite("S8"):
        own = [x for x in ("X1", "X2") if x not in by_id]
        res.add("S8", "FAIL" if own else "PASS",
                "no test named " + ", ".join(own) + " - your own cases from section 3" if own else "X1 and X2 present")

    # S9
    if need_suite("S9"):
        clean = strip_js_comments(src)
        hits = sorted(set(re.findall(r"\bDate\.now\s*\(|\bnew\s+Date\s*\(|\bMath\.random\s*\(", clean)))
        res.add("S9", "FAIL" if hits else "PASS",
                "the suite reads the clock or random numbers: " + ", ".join(h.strip() for h in hits)
                + " - pass now as a number (540)" if hits else "fixed time")

    # S10
    first = [p for p in walk_files(FIRST) if is_test_file(p)] if os.path.isdir(FIRST) else []
    measured["first_suite"] = rel(first[0]) if first else None
    measured["tests_first"] = len(tests_in(read(first[0]) or "")) if first else None
    if not first:
        res.add("S10", "ERROR", "no *.test.* file in suites/first/ - save the assistant's first test file there, unedited")
    elif suite is None:
        res.add("S10", "ERROR", "no final suite to compare with")
    else:
        same = norm(read(first[0]) or "") == norm(src or "")
        res.add("S10", "FAIL" if same else "PASS",
                "suites/first/ is identical to the final suite - the review must change something "
                "(at least X1 and X2)" if same else "%s kept; final differs" % rel(first[0]))
    return tests


# --------------------------------------------------------------------------- R, M, U, L: the report


def check_runs(res, measured, sec):
    s61 = " ".join(blocks(sec.get("6.1", "")))
    first = vitest_summaries(s61)
    measured["first_run"] = first[0] if first else None
    res.add("R1", "PASS" if first else "FAIL",
            "first run: %(failed)d failed, %(passed)d passed (%(total)d)" % first[0] if first
            else "section 6.1 has no Vitest output - paste the terminal from the RUN line to the 'Tests' line")

    s63 = " ".join(blocks(sec.get("6.3", "")))
    final = vitest_summaries(s63)
    measured["final_run"] = final[-1] if final else None
    if not final:
        res.add("R2", "FAIL", "section 6.3 has no Vitest output of the final suite")
    else:
        f = final[-1]
        probs = []
        if f["failed"]:
            probs.append("%d failed - fix the defect or explain it in 9.1" % f["failed"])
        if f["skipped"] or f["todo"]:
            probs.append("skipped or todo tests in the run")
        have = measured.get("tests_in_project")
        if have and f["total"] != have:
            probs.append("the output reports %d tests, the test files in app/ hold %d - paste the run of the "
                         "suite you committed" % (f["total"], have))
        res.add("R2", "FAIL" if probs else "PASS",
                "; ".join(probs) if probs else "%(passed)d passed (%(total)d)" % f)

    setup = {r[0].lower(): r[1] for r in table_rows(sec.get("1", "")) if len(r) > 1}
    declared = next((v for k, v in setup.items() if "vitest version" in k and useful(v)), "")
    m = re.search(r"(\d+\.\d+(?:\.\d+)?)", declared)
    seen = vitest_version(s63) or vitest_version(s61)
    measured["vitest_version"] = m.group(1) if m else seen
    if not m:
        res.add("R3", "FAIL", "section 1: write the Vitest version from the 'RUN  v...' line, e.g. 3.2.4")
    elif seen and not seen.startswith(m.group(1)):
        res.add("R3", "FAIL", "section 1 says %s, your pasted run says v%s" % (m.group(1), seen))
    else:
        res.add("R3", "PASS", "Vitest %s" % m.group(1))


def check_mutants(res, measured, sec, titles):
    s7 = sec.get("7", "")
    rows = table_rows(s7)
    names = set()
    for t in titles:
        names |= ids_in(t)
    detected = 0
    for mid, what in MUTANTS:
        cells = row_by_id(rows, mid)
        if cells is None or len(cells) < 5:
            res.add(mid, "ERROR", "no row %s in the section 7 table" % mid)
            continue
        verdict = cell_word(cells[2], ("Detected", "Survived"))
        if verdict is None:
            res.add(mid, "FAIL", "write Detected or Survived for %s (%s)" % (mid, what))
        elif verdict == "Detected":
            ids = set(re.findall(r"\b(T0[1-9]|T1[0-4]|X[12]|AC5)\b", cells[3]))
            unknown = sorted(i for i in ids if i not in names)
            if not ids:
                res.add(mid, "FAIL", "%s detected - name the failing test ID(s)" % mid)
            elif unknown and names:
                res.add(mid, "FAIL", "%s: %s is not a test in your final suite" % (mid, ", ".join(unknown)))
            else:
                detected += 1
                res.add(mid, "PASS", "detected by " + ", ".join(sorted(ids)))
        else:
            words = word_count(cells[4])
            res.add(mid, "PASS" if words >= 8 else "FAIL",
                    "survived, explained" if words >= 8
                    else "%s survived - say why (8 words or more) and what you added to catch it" % mid)
    measured["mutants_detected"] = detected
    runs = vitest_summaries(" ".join(blocks(s7)))
    res.add("M4", "PASS" if len(runs) >= 3 else "FAIL",
            "%d mutant runs pasted" % len(runs) if len(runs) >= 3
            else "section 7: paste one Vitest run per mutant, with its 'Tests' line (found %d)" % len(runs))


def check_ui(res, measured, sec):
    found, missing, hashes = {}, [], {}
    for n in range(1, 6):
        p = find_image("ui-%d" % n)
        why = image_problem(p)
        if why:
            missing.append("ui-%d" % n if why == "missing" else why)
        else:
            found[n] = p
            hashes.setdefault(hashlib.sha1(open(p, "rb").read()).hexdigest(), []).append("ui-%d" % n)
    dupes = [ids for ids in hashes.values() if len(ids) > 1]
    if missing:
        res.add("U1", "ERROR" if not found else "FAIL", "missing or unreadable: " + ", ".join(missing))
    elif dupes:
        res.add("U1", "FAIL", "identical files: " + "; ".join(" = ".join(i) for i in dupes))
    else:
        res.add("U1", "PASS", "ui-1 ... ui-5")
    if 4 not in found:
        res.add("U2", "ERROR", "evidence/ui-4.png not found")
    else:
        w, h = image_info(found[4])
        res.add("U2", "PASS" if h > w else "FAIL",
                "%dx%d" % (w, h) + ("" if h > w else " - not portrait; use the browser's device toolbar at about 375 px"))

    rows = table_rows(sec.get("8", ""))
    bad, passed = [], 0
    for uid in UI:
        cells = row_by_id(rows, uid)
        if cells is None or len(cells) < 6 or not useful(cells[4]):
            bad.append(uid)
            continue
        v = cell_word(cells[5], ("Pass", "Fail", "Not testable"))
        if v is None:
            bad.append(uid)
        elif v == "Pass":
            passed += 1
    measured["ui_pass"] = passed
    res.add("U3", "FAIL" if bad else "PASS",
            "section 8: write what you observed and Pass / Fail / Not testable for " + ", ".join(bad)
            if bad else "%d of 5 passed" % passed)


def check_report(res, measured, sec):
    def add(cid, ok, good, bad):
        res.add(cid, "PASS" if ok else "FAIL", good if ok else bad)

    # L1
    setup = {r[0].lower(): r[1] for r in table_rows(sec.get("1", "")) if len(r) > 1}
    need = {"project i continue": "the project you continue (week-06 or starter)",
            "assistant": "the assistant", "exact model": "the exact model",
            "where i ran": "where you ran the tests", "test command": "the test command"}
    lacking = [say for key, say in need.items()
               if not any(key in label and useful(value) for label, value in setup.items())]
    add("L1", not lacking, "setup recorded", "section 1 has no value for: " + ", ".join(lacking))

    # L2
    s2 = sec.get("2", "")
    filled = [r for r in table_rows(s2) if len(r) > 1 and useful(r[1])]
    words = word_count(after_marker(s2))
    probs = []
    if len(filled) < 4:
        probs.append("all four rows of the 'before' table (found %d)" % len(filled))
    if words < EXTRACT_MIN:
        probs.append("%d+ words on the extraction (found %d)" % (EXTRACT_MIN, words))
    add("L2", not probs, "before-table complete; extraction in %d words" % words, "section 2 needs " + "; ".join(probs))

    # L3
    rows = table_rows(sec.get("3", ""))
    no_reason = []
    for rid in [p[0] for p in PLAN] + ["AC5"]:
        cells = row_by_id(rows, rid)
        if cells is None or len(cells) < 5 or len(re.findall(r"\w+", cells[4])) < 3:
            no_reason.append(rid)
    own = [x for x in ("X1", "X2")
           if not (row_by_id(rows, x) and len(row_by_id(rows, x)) >= 5
                   and all(useful(c) for c in row_by_id(rows, x)[1:5]))]
    probs = []
    if no_reason:
        probs.append("a reason (3+ words) for " + ", ".join(no_reason[:6]) + ("..." if len(no_reason) > 6 else ""))
    if own:
        probs.append("all five columns of " + " and ".join(own))
    add("L3", not probs, "every case has a reason; X1 and X2 complete", "section 3 needs " + "; ".join(probs))

    # L4
    s4 = sec.get("4", "")
    allb = blocks(s4)
    prompt = norm(allb[0]) if allb else ""
    probs = []
    lost = [p for p in GENERATION_PROMPT if norm(p) not in prompt]
    if lost:
        probs.append("the deck's prompt as sent (missing: \"%s\")" % lost[0])
    if "[our test framework]" in prompt.lower():
        probs.append("[our test framework] replaced by Vitest")
    if len(real_blocks(s4)) < 2:
        probs.append("the assistant's answer pasted in the second block")
    add("L4", not probs, "prompt as sent; answer pasted", "section 4 needs " + "; ".join(probs))

    # L5
    decisions = [r for r in table_rows(sec.get("5", ""))
                 if len(r) >= 5 and useful(r[1]) and useful(r[2])
                 and re.match(r"^\W*(accept|revise|reject)(ed)?\b", re.sub(r"<!--.*?-->", "", r[3]).strip(), re.I)
                 and not PLACEHOLDER.search(r[3])
                 and useful(r[4])]
    measured["review_decisions"] = len(decisions)
    add("L5", len(decisions) >= 2, "%d review decisions" % len(decisions),
        "section 5 needs at least 2 rows: the test, what is weak, accept/revise/reject, the AC or reason "
        "(found %d)" % len(decisions))

    # L6
    s61 = sec.get("6.1", "")
    diag = [r for r in table_rows(s61) if r and any(useful(c) for c in r)]
    first = measured.get("first_run") or {}
    probs = []
    if first.get("failed"):
        if len([r for r in diag if sum(1 for c in r if useful(c)) >= 4]) < 1:
            probs.append("a diagnosis row for each failure of the first run (6.1)")
    elif not diag:
        probs.append("the diagnosis table in 6.1 - write none if nothing failed")
    imp = norm(" ".join(blocks(sec.get("6.2", ""))))
    lost = [p for p in IMPROVEMENT_PROMPT if norm(p) not in imp]
    if lost:
        probs.append("the improvement prompt as sent in 6.2 (missing: \"%s\")" % lost[0])
    add("L6", not probs, "failures diagnosed; improvement prompt as sent", "section 6 needs " + "; ".join(probs))

    # L7
    comp = [r for r in table_rows(sec.get("9.2", "")) if len(r) >= 3 and useful(r[1]) and useful(r[2])]
    add("L7", len(comp) >= 5, "comparison complete",
        "section 9.2: fill both columns of all five rows (found %d)" % len(comp))

    # L8
    words = word_count(sec.get("10", ""))
    measured["conclusion_words"] = words
    add("L8", WORDS_MIN <= words <= WORDS_MAX, "%d words" % words,
        "section 10 has %d words, the task asks for %d-%d" % (words, WORDS_MIN, WORDS_MAX))


# --------------------------------------------------------------------------- main


def run():
    res, measured = Results(), {}
    root, module, sources = check_project(res, measured)
    tests = check_suite(res, measured, root, module, sources)
    text = read(REPORT)
    if text is None:
        for cid in ORDER:
            if cid[0] in "RMUL":
                res.add(cid, "ERROR", "lab-report.md not found")
    else:
        sec = sections(text)
        check_runs(res, measured, sec)
        check_mutants(res, measured, sec, [t for t, _, _ in tests])
        check_ui(res, measured, sec)
        check_report(res, measured, sec)
    seen = set()
    rows = []
    for r in res.rows:
        if r["id"] not in seen:
            seen.add(r["id"])
            rows.append(r)
    res.rows = sorted(rows, key=lambda r: ORDER.index(r["id"]))
    return res, measured


def print_human(res, measured):
    counts = res.counts()
    print("Week 07 - testing AI-generated code: the project, the suite, the runs, the report\n")
    width = max(len(r["title"]) for r in res.rows)
    for r in res.rows:
        print(("%-6s %-4s %-*s  %s" % (r["verdict"], r["id"], width, r["title"], r["message"])).rstrip())
    print("-" * 78)
    if measured.get("tests_final") is not None and measured.get("suite"):
        print("Final suite: %s, %d tests. First suite: %s tests." % (
            measured["suite"], measured["tests_final"],
            measured["tests_first"] if measured.get("tests_first") is not None else "-"))
    print("SUMMARY pass=%d fail=%d error=%d   (%d checks)"
          % (counts["PASS"], counts["FAIL"], counts["ERROR"], len(res.rows)))
    if counts["FAIL"] or counts["ERROR"]:
        print("Every FAIL or ERROR you keep goes in lab-report.md section 9.1 and in submission.yml known_fails.")
        print("One you report and explain costs you nothing. One you hide costs the whole criterion.")
    else:
        print("Files and shape are clean. This says nothing about whether your tests are good - "
              "the mutants and the review do.")


def main():
    parser = argparse.ArgumentParser(description="Week 07 checker - run from inside week-07/")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    if not os.path.isdir("tests") and not os.path.exists(REPORT) and not os.path.isdir(APP):
        message = "run this from inside your week-07/ folder:  cd week-07 && python tests/check_suite.py"
        print(json.dumps({"ok": False, "error": message}) if args.json else "ERROR: " + message)
        return 3

    res, measured = run()
    counts = res.counts()
    ok = counts["FAIL"] == 0 and counts["ERROR"] == 0
    if args.json:
        print(json.dumps({"ok": ok, "counts": counts, "total": len(res.rows),
                          "rows": res.rows, "measured": measured}, ensure_ascii=False, indent=2))
    else:
        print_human(res, measured)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())