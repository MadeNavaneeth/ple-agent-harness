"""PLE harness extension: deliverable detection, validation, gating, discipline.

Imported by serve.py. Stdlib-only (it runs in the harness container, not the task
container); the actual file inspection runs INSIDE the task container through a
generated python3 heredoc, so it uses the task's own installed libraries.

The DISCIPLINE block encodes what the dev-set graders actually penalise, found by
running the graders offline against our own submissions:
  * register precision below the floor voids EVERY family (wind-diaphragm-shear:
    precision 0.55 < 0.60 -> mean_p 0.0 even though parse_ok was true)
  * one non-numeric cell makes installed_cost infinite, so the objective term can
    never pay
  * a deflection of 146,038 in and a failed footprint family both trace back to
    the model never pinning down the as-built geometry
"""

from __future__ import annotations

import json
import posixpath
import re
from typing import Any

# ---------------------------------------------------------------- detection

_EXT_KIND = {
    ".zip": "zip",
    ".xlsx": "xlsx",
    ".xlsm": "xlsx",
    ".xls": "xlsx",
    ".docx": "docx",
    ".doc": "docx",
    ".pptx": "pptx",
    ".pdf": "pdf",
    ".ifc": "ifc",
    ".dxf": "dxf",
    ".json": "json",
    ".csv": "text",
    ".md": "text",
    ".txt": "text",
    ".py": "text",
}

# A deliverable mentioned only in passing is not a deliverable.
_MAX_DELIVERABLES = 8


def kind_of(path: str) -> str:
    """Maps a file path to a validator kind."""
    lower = path.lower()
    for ext, kind in _EXT_KIND.items():
        if lower.endswith(ext):
            return kind
    return "text"


def _normalise(path: str, workdir: str) -> str:
    path = path.strip().strip("`'\"")
    if path.startswith("/"):
        return path
    return posixpath.join(workdir.rstrip("/"), path)


def detect(instruction: str, workdir: str) -> list[dict[str, Any]]:
    """Finds the graded deliverables named in the task instruction."""
    candidates: list[str] = []
    for pattern in (
        r"write your deliverable to\s+`([^`]+)`",
        r"deliverables?:?\s+`([^`]+)`",
    ):
        for m in re.finditer(pattern, instruction, re.I):
            candidates.append(m.group(1))
    for m in re.finditer(r"`([^`]*output/[^`]+)`", instruction):
        candidates.append(m.group(1))
    for m in re.finditer(
        r"`([\w./-]+\.(?:zip|xlsx|xlsm|docx|pptx|pdf|ifc|dxf|md))`", instruction
    ):
        candidates.append(m.group(1))

    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in candidates:
        if not raw or " " in raw:
            continue
        path = _normalise(raw, workdir)
        if path in seen:
            continue
        seen.add(path)
        out.append({"path": path, "kind": kind_of(path)})
        if len(out) >= _MAX_DELIVERABLES:
            break

    # The graded artifact is usually a zip holding all the others: if a zip is
    # present it is the primary deliverable and the other named files are its
    # members, so they must NOT be validated as separate top-level paths.
    zips = [d for d in out if d["kind"] == "zip"]
    if zips:
        primary = zips[0]
        members = [posixpath.basename(d["path"]) for d in out if d is not primary]
        if members:
            primary["members"] = members
        rest = [d for d in out if d is not primary and d["kind"] == "zip"]
        return [primary] + rest[:1]
    return out


DISCIPLINE = """Engineering discipline that decides the score on this benchmark.
1. GEOMETRY FIRST. Extract the as-built geometry with code (DXF via ezdxf, IFC via
   ifcopenshell, point clouds with numpy, schedules with openpyxl) and write it to
   a geometry JSON that every later calculation reads. Cross-check each governing
   dimension against at least two independent sources (drawing dimension text,
   federated model, survey, scan). When they disagree, state which document
   governs and why. Do not size anything from a number you have not extracted.
2. COMPUTE, NEVER RECALL. Every number in a deliverable must come from a script
   you ran here. Never do arithmetic in prose. Print intermediates and sanity-check
   magnitudes: a deflection of 146,000 in, a reaction of 1e6 lb, or an area of
   1e-3 sf means a unit or parsing error, so stop and fix it before continuing.
3. UNITS. Keep one unit system, put the unit in every column header and table
   caption, and convert explicitly rather than silently.
4. NUMERIC CELLS MUST BE NUMBERS. In any workbook a cost/quantity cell that is
   empty, text, "N/A" or "TBD" makes the totals unreadable and the whole cost
   objective scores zero. Sum the total from the line items and print it.
5. CONSTRAINT REGISTER (when the task asks for one). Cite only a document and
   clause you have actually opened and quote the clause wording as you read it.
   One document per row, at most three clauses and at most eight numbers per row.
   Never cite a superseded revision (paths containing SUPERSEDED, Rev0/Rev1, or a
   study for a different building). Wrong rows are penalised and if precision
   drops below the required floor EVERY entry is voided: a short, fully correct
   register beats a long, partly wrong one. Aim for 15-40 rows you are sure of.
6. SELF-CHECK BEFORE FINISHING. Re-open every deliverable, confirm it parses,
   confirm each required sheet/column/section exists and is non-empty, then fix
   what is wrong.
7. DO NOT GUESS LIBRARY APIS. Before calling a library function you are not
   certain of, inspect it: `python3 -c "import openpyxl; print([n for n in dir(openpyxl) if 'load' in n])"`,
   `help(ezdxf.new)`, or `inspect.signature(...)`. Put anything longer than three
   lines in a `.py` file and run it, so a syntax error can be fixed with one edit
   instead of a full rewrite."""


def recovery_hint(exit_code: Any, output: str) -> str:
    """Returns a short, error-class-specific hint to append to a failed command.

    Grounded in the trajectory failure taxonomy: 31.6% of commands failed, and
    ~half of those were the model writing code against APIs it half-remembers.
    """
    if exit_code in (0, None):
        return ""
    text = output or ""

    def has(*needles: str) -> bool:
        return any(n in text for n in needles)

    if has("AttributeError"):
        return (
            "\n[harness] AttributeError: that API does not exist under that name. "
            "Do not retry a guess - inspect it first, e.g. "
            '`python3 -c "import LIB; print([n for n in dir(LIB) if \'NAME\' in n])"` '
            "or `python3 -c \"import inspect, LIB; print(inspect.signature(LIB.FN))\"`, "
            "then call the real name/signature."
        )
    if has("unexpected keyword argument"):
        return (
            "\n[harness] Wrong keyword argument: print the real signature before "
            'retrying: `python3 -c "import inspect, LIB; '
            'print(inspect.signature(LIB.FN))"`.'
        )
    if has("SyntaxError", "IndentationError"):
        return (
            "\n[harness] Syntax error in the heredoc/one-liner. Write the code to a "
            "file with write_file, run it with `python3 file.py`, and fix it with "
            "edit_file instead of rewriting the whole block."
        )
    if has("ModuleNotFoundError"):
        return (
            "\n[harness] That package is not installed and there is no network. Use "
            "`python3 -c \"import sys; print(sys.version)\"` and check what exists with "
            "`python3 -c \"import pkgutil; print(sorted(m.name for m in pkgutil.iter_modules()))\"`, "
            "or use the standard library."
        )
    if has("TypeError"):
        return (
            "\n[harness] TypeError: check argument order/types - print the values you "
            "pass with `print(type(x), repr(x))` before the failing call."
        )
    if has("IndexError", "KeyError"):
        return (
            "\n[harness] Index/Key error: print the container's shape or keys before "
            "indexing (`print(len(x))`, `print(list(d)[:20])`)."
        )
    if has("json.decoder.JSONDecodeError"):
        return (
            "\n[harness] Invalid JSON: print the first 300 characters of the payload "
            "and check it is complete before parsing."
        )
    if has("MemoryError", "Killed"):
        return (
            "\n[harness] Out of memory: process the file in chunks or lower precision."
        )
    return ""


def contract_message(deliverables: list[dict[str, Any]]) -> str:
    """System addendum: the enforced deliverable contract plus discipline rules."""
    if not deliverables:
        return ""
    lines = [
        "GRADED DELIVERABLE CONTRACT (enforced by the harness).",
        "The run is graded only on these paths; a missing or unparseable file "
        "scores zero however good the analysis is:",
    ]
    for d in deliverables:
        extra = ""
        if d.get("members"):
            extra = " and it must contain: " + ", ".join(d["members"])
        lines.append(f"- {d['path']} [{d['kind']}]{extra}")
    lines += [
        "Rules:",
        "1. Create a COMPLETE, parseable version of every deliverable early "
        "(use templates/ when the task provides them), then improve it in "
        "place. Never leave the deliverable missing while you keep analysing.",
        "2. Produce binary formats (xlsx/docx/pdf/ifc/dxf) by running code, "
        "not by writing prose into a file with the wrong extension.",
        "3. Call check_deliverable before you finish; it opens the file with "
        "the real libraries and reports what is wrong.",
        "",
        DISCIPLINE,
    ]
    return "\n".join(lines)


# --------------------------------------------------------------- validation

_VALIDATOR = r'''
import json, os, sys, zipfile

spec = json.loads(sys.argv[1])
path, kind, members = spec["path"], spec["kind"], spec.get("members") or []
res = {"path": path, "kind": kind, "ok": False}
try:
    if not os.path.exists(path):
        res["error"] = "file does not exist"
    else:
        size = os.path.getsize(path)
        res["size"] = size
        if size == 0:
            res["error"] = "file is empty"
        elif kind == "zip":
            with zipfile.ZipFile(path) as z:
                names = z.namelist()
                res["count"] = len(names)
                res["members"] = names[:60]
                bad = z.testzip()
                missing = [m for m in members if not any(m == n or n.endswith("/" + m) for n in names)]
                if bad:
                    res["error"] = f"corrupt member: {bad}"
                elif not names:
                    res["error"] = "zip has no members"
                elif missing:
                    res["error"] = "missing required members: " + ", ".join(missing)
                else:
                    res["ok"] = True
        elif kind == "xlsx":
            import openpyxl
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
            res["sheets"] = wb.sheetnames
            empty = [s for s in wb.sheetnames if wb[s].max_row <= 1]
            res["empty_sheets"] = empty
            res["ok"] = bool(wb.sheetnames)
            if not res["ok"]:
                res["error"] = "workbook has no sheets"
            wb.close()
        elif kind == "docx":
            import docx
            d = docx.Document(path)
            paras = [p.text for p in d.paragraphs if p.text.strip()]
            res["paragraphs"] = len(paras)
            res["tables"] = len(d.tables)
            res["ok"] = bool(paras or d.tables)
            if not res["ok"]:
                res["error"] = "document has no text or tables"
        elif kind == "pptx":
            import pptx
            pr = pptx.Presentation(path)
            res["slides"] = len(pr.slides)
            res["ok"] = res["slides"] > 0
            if not res["ok"]:
                res["error"] = "presentation has no slides"
        elif kind == "pdf":
            try:
                import fitz
                doc = fitz.open(path)
                res["pages"] = doc.page_count
                text = "".join(p.get_text() for p in doc[:3])
                doc.close()
            except ImportError:
                import pypdf
                r = pypdf.PdfReader(path)
                res["pages"] = len(r.pages)
                text = "\n".join((p.extract_text() or "") for p in r.pages[:3])
            res["text_chars_first_pages"] = len(text.strip())
            res["ok"] = res.get("pages", 0) > 0 and res["text_chars_first_pages"] > 0
            if not res["ok"]:
                res["error"] = "pdf has no pages or no extractable text"
        elif kind == "ifc":
            import ifcopenshell
            f = ifcopenshell.open(path)
            res["entities"] = len(f.wrapped_data.entity_names()) if hasattr(f.wrapped_data, "entity_names") else None
            res["schema"] = f.schema
            res["ok"] = True
        elif kind == "dxf":
            import ezdxf
            doc = ezdxf.readfile(path)
            res["layers"] = [l.dxf.name for l in doc.layers][:40]
            res["entities"] = len(doc.modelspace())
            res["ok"] = res["entities"] > 0
            if not res["ok"]:
                res["error"] = "dxf modelspace is empty"
        elif kind == "json":
            with open(path, encoding="utf-8", errors="replace") as fh:
                json.load(fh)
            res["ok"] = True
        else:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            res["chars"] = len(text)
            res["ok"] = len(text.strip()) > 0
            if not res["ok"]:
                res["error"] = "text file is empty"
except Exception as exc:  # noqa: BLE001 - report, never crash the harness
    res["error"] = f"{type(exc).__name__}: {exc}"
print("PLE_VALIDATION " + json.dumps(res))
'''


def validator_command(kind: str, path: str, members: list[str] | None = None) -> str:
    """Builds the bash command that validates one deliverable in the container."""
    spec = json.dumps({"path": path, "kind": kind, "members": members or []})
    return f"python3 - {shell_quote(spec)} <<'PLE_VALIDATOR'\n{_VALIDATOR}\nPLE_VALIDATOR"


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def parse_validation(output: str) -> dict[str, Any]:
    """Extracts the JSON line a validator command printed."""
    for line in reversed((output or "").splitlines()):
        if line.startswith("PLE_VALIDATION "):
            try:
                return json.loads(line[len("PLE_VALIDATION ") :])
            except json.JSONDecodeError:
                break
    return {"ok": False, "error": "validator produced no result: " + (output or "")[:300]}


def describe(result: dict[str, Any]) -> str:
    """Human/model readable one-line verdict."""
    path = result.get("path", "?")
    if result.get("ok"):
        bits = [f"OK {path}", f"{result.get('size', 0)} bytes"]
        for key in ("count", "sheets", "pages", "entities", "slides", "paragraphs", "chars"):
            if key in result:
                bits.append(f"{key}={result[key]}")
        if result.get("empty_sheets"):
            bits.append("EMPTY SHEETS=" + ",".join(result["empty_sheets"]))
        return ", ".join(bits)
    return f"FAIL {path}: {result.get('error', 'unknown error')}"
