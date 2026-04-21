#!/usr/bin/env python3
"""Portfolio Manager — Noémie Ducly"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import shutil
import subprocess
import re
import unicodedata
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image as PilImage
    PILLOW_OK = True
except ImportError:
    PILLOW_OK = False

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp"}

# ── Config ─────────────────────────────────────────────────────────────────────
SITE_DIR   = Path(__file__).parent
ASSETS_DIR = SITE_DIR / "assets" / "projects"
DATA_FILE  = SITE_DIR / "data.js"
TAGS_FILE  = SITE_DIR / "tags.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Design tokens (Apple macOS dark mode) ─────────────────────────────────────
BG      = "#1c1c1e"
SIDEBAR = "#141416"
CARD    = "#2c2c2e"
INPUT   = "#3a3a3c"
SEP     = "#38383a"
T1      = "#f2f2f7"
T2      = "#8e8e93"
T3      = "#48484a"
ACCENT  = "#0a84ff"
SUCCESS = "#30d158"
DANGER  = "#ff453a"

TAGS_DEFAULT = [
    "Creative Direction", "CGI", "VFX",
    "Photography", "Graphic Design", "Motion Design", "Film",
]


# ── Tags persistence ──────────────────────────────────────────────────────────

def load_tags() -> list:
    if TAGS_FILE.exists():
        try:
            import json
            data = json.loads(TAGS_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list) and data:
                return data
        except Exception:
            pass
    return list(TAGS_DEFAULT)


def save_tags(tags: list):
    import json
    TAGS_FILE.write_text(
        json.dumps(tags, ensure_ascii=False, indent=2), encoding="utf-8")


# ── Backend helpers ────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def url_encode(path: str) -> str:
    return path.replace(" ", "%20")


def convert_to_webp(src: Path, dest_dir: Path, quality: int = 85) -> Path:
    out = dest_dir / (src.stem + ".webp")
    with PilImage.open(src) as img:
        img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB").save(
            out, "WEBP", quality=quality, method=6)
    return out


def copy_files(files: list, dest: Path,
               to_webp: bool = False, quality: int = 85) -> list:
    dest.mkdir(parents=True, exist_ok=True)
    result = []
    for f in files:
        src = Path(f)
        is_image = src.suffix.lower() in IMAGE_EXTS
        if to_webp and is_image and src.suffix.lower() != ".webp":
            if not PILLOW_OK:
                raise RuntimeError(
                    "Pillow n'est pas installé.\nLance : pip install Pillow")
            out = convert_to_webp(src, dest, quality=quality)
        else:
            out = dest / src.name
            shutil.copy2(src, out)
        rel = out.relative_to(SITE_DIR)
        result.append(url_encode(str(rel).replace("\\", "/")))
    return result


def js_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def build_js_entry(p: dict) -> str:
    parts = []
    parts.append(f'client: "{js_escape(p["client"])}"')
    parts.append(f'title: "{js_escape(p["title"])}"')
    parts.append(f'slug: "{js_escape(p["slug"])}"')
    parts.append(f'tags: [' + ", ".join(f'"{t}"' for t in p["tags"]) + "]")
    parts.append(f'role: "{js_escape(p["role"])}"')
    parts.append(f'image: "{p["image"]}"')
    parts.append(f'video: "{p["video"]}"' if p.get("video") else "video: null")
    if p.get("videos") and len(p["videos"]) > 1:
        parts.append("videos: [" + ", ".join(f'"{v}"' for v in p["videos"]) + "]")
    if p.get("vimeo_url"):
        parts.append(f'vimeoUrl: "{js_escape(p["vimeo_url"])}"')
    parts.append(f'year: "{js_escape(p["year"])}"')
    desc = (p.get("description", "")
            .replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n"))
    parts.append(f'description: "{desc}"')
    if p.get("wips"):
        parts.append("wips: [" + ", ".join(f'"{w}"' for w in p["wips"]) + "]")
    return "{ " + ", ".join(parts) + " }"


def inject_project(project: dict):
    text = DATA_FILE.read_text(encoding="utf-8")
    marker = "const FEATURED_PROJECTS = ["
    idx = text.find(marker)
    if idx == -1:
        raise ValueError("Impossible de trouver FEATURED_PROJECTS dans data.js")
    pos = idx + len(marker)
    DATA_FILE.write_text(
        text[:pos] + "\n  " + build_js_entry(project) + "," + text[pos:],
        encoding="utf-8")


def run_git(*args) -> tuple:
    r = subprocess.run(
        ["git", *args], cwd=str(SITE_DIR),
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout, r.stderr


# ── data.js parser ────────────────────────────────────────────────────────────

def _extract_project_texts(text: str) -> list[str]:
    m = re.search(r'const FEATURED_PROJECTS\s*=\s*\[', text)
    if not m:
        return []
    i, depth, start, objects = m.end(), 0, None, []
    while i < len(text):
        ch = text[i]
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start is not None:
                objects.append(text[start:i + 1])
                start = None
        elif ch == ']' and depth == 0:
            break
        i += 1
    return objects


def _js_str(obj: str, key: str) -> str:
    m = re.search(rf'\b{key}\s*:\s*"((?:[^"\\]|\\.)*)"', obj)
    if not m:
        return ""
    return (m.group(1).replace('\\n', '\n')
                      .replace('\\"', '"')
                      .replace('\\\\', '\\'))


def _js_nullable(obj: str, key: str):
    m = re.search(rf'\b{key}\s*:\s*(?:"((?:[^"\\]|\\.)*)"|null)', obj)
    if not m:
        return None
    return (m.group(1).replace('\\n', '\n')
                      .replace('\\"', '"')
                      .replace('\\\\', '\\')) if m.group(1) is not None else None


def _js_arr(obj: str, key: str) -> list:
    m = re.search(rf'\b{key}\s*:\s*\[(.*?)\]', obj, re.DOTALL)
    return re.findall(r'"([^"]*)"', m.group(1)) if m else []


def parse_project(obj_text: str) -> dict:
    return {
        'client':      _js_str(obj_text, 'client'),
        'title':       _js_str(obj_text, 'title'),
        'slug':        _js_str(obj_text, 'slug'),
        'role':        _js_str(obj_text, 'role'),
        'image':       _js_str(obj_text, 'image'),
        'video':       _js_nullable(obj_text, 'video'),
        'vimeo_url':   _js_nullable(obj_text, 'vimeoUrl'),
        'year':        _js_str(obj_text, 'year'),
        'description': _js_str(obj_text, 'description'),
        'tags':        _js_arr(obj_text, 'tags'),
        'videos':      _js_arr(obj_text, 'videos'),
        'wips':        _js_arr(obj_text, 'wips'),
    }


def load_all_projects() -> list[dict]:
    text = DATA_FILE.read_text(encoding="utf-8")
    return [parse_project(o) for o in _extract_project_texts(text)]


def update_project_in_data_js(original_slug: str, updated: dict):
    text = DATA_FILE.read_text(encoding="utf-8")
    m = re.search(rf'\bslug\s*:\s*"{re.escape(original_slug)}"', text)
    if not m:
        raise ValueError(f'Projet avec slug "{original_slug}" introuvable.')
    brace = text.rfind('{', 0, m.start())
    if brace == -1:
        raise ValueError("Structure inattendue dans data.js.")
    depth, i, end = 0, brace, None
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                end = i
                break
        i += 1
    if end is None:
        raise ValueError("Impossible de délimiter l'objet projet.")
    DATA_FILE.write_text(
        text[:brace] + build_js_entry(updated) + text[end + 1:],
        encoding="utf-8")


def delete_project_from_data_js(slug: str):
    text = DATA_FILE.read_text(encoding="utf-8")
    m = re.search(rf'\bslug\s*:\s*"{re.escape(slug)}"', text)
    if not m:
        raise ValueError(f'Projet avec slug "{slug}" introuvable.')
    brace = text.rfind('{', 0, m.start())
    depth, i, end = 0, brace, None
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                end = i
                break
        i += 1
    if end is None:
        raise ValueError("Impossible de trouver la fin de l'objet projet.")
    before = text[:brace]
    after  = text[end + 1:]
    # Supprime la virgule associée (après ou avant)
    import re as _re
    after_stripped = after.lstrip()
    if after_stripped.startswith(','):
        after = after_stripped[1:]
    else:
        before = _re.sub(r',\s*$', '', before)
    DATA_FILE.write_text(before.rstrip() + "\n" + after.lstrip(),
                         encoding="utf-8")


