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


# ── Application ───────────────────────────────────────────────────────────────

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Portfolio Manager — Noémie Ducly")
        self.geometry("800x880")
        self.minsize(700, 600)

        self._image_file  = None
        self._video_files: list = []
        self.wip_files:    list = []
        self.tag_vars: dict[str, ctk.BooleanVar] = {}

        self.e_image_file    = None
        self.e_video_files:  list = []
        self.e_wip_files:    list = []
        self.e_current_slug  = None
        self.e_tag_vars: dict[str, ctk.BooleanVar] = {}
        self._proj_btns: dict[str, ctk.CTkButton] = {}

        tabs = ctk.CTkTabview(self, anchor="nw")
        tabs.pack(fill="both", expand=True, padx=16, pady=16)
        tabs.add("Nouveau projet")
        tabs.add("Modifier un projet")
        tabs.add("Publier sur GitHub")

        self._build_new_tab(tabs.tab("Nouveau projet"))
        self._build_edit_tab(tabs.tab("Modifier un projet"))
        self._build_publish_tab(tabs.tab("Publier sur GitHub"))

    # ── helpers communs ───────────────────────────────────────────────────────

    def _lbl(self, parent, text):
        ctk.CTkLabel(parent, text=text, anchor="w",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(
            fill="x", padx=12, pady=(14, 2))

    def _ent(self, parent, var, placeholder=""):
        e = ctk.CTkEntry(parent, textvariable=var,
                         placeholder_text=placeholder, height=34)
        e.pack(fill="x", padx=12, pady=(0, 4))
        return e

    def _file_row(self, parent, var, cmd, btn_text):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=12, pady=4)
        ctk.CTkLabel(f, textvariable=var, anchor="w", wraplength=520).pack(
            side="left", fill="x", expand=True)
        ctk.CTkButton(f, text=btn_text, width=170, command=cmd).pack(side="right")

    def _tag_grid(self, parent, tag_vars: dict, tags_list: list,
                  toggle_fn=None):
        """Draw checkboxes for all tags. toggle_fn unused, kept for compat."""
        for w in parent.winfo_children():
            w.destroy()
        prev = {t for t, v in tag_vars.items() if v.get()}
        tag_vars.clear()
        for i, t in enumerate(tags_list):
            v = ctk.BooleanVar(value=(t in prev))
            tag_vars[t] = v
            ctk.CTkCheckBox(parent, text=t, variable=v).grid(
                row=i // 3, column=i % 3, sticky="w", padx=8, pady=4)

    def _webp_section(self, parent, var_webp, var_quality, lbl_quality_ref):
        webp_row = ctk.CTkFrame(parent, fg_color="transparent")
        webp_row.pack(fill="x", padx=12, pady=(14, 4))
        ctk.CTkCheckBox(webp_row, text="Convertir les images en WebP",
                        variable=var_webp,
                        font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        hint = "(recommandé)" if PILLOW_OK else "  ⚠ pip install Pillow requis"
        ctk.CTkLabel(webp_row, text=hint, text_color="gray",
                     font=ctk.CTkFont(size=11)).pack(side="left", padx=(8, 0))

        q_row = ctk.CTkFrame(parent, fg_color="transparent")
        q_row.pack(fill="x", padx=12, pady=(0, 4))
        ctk.CTkLabel(q_row, text="Qualité WebP :",
                     font=ctk.CTkFont(size=11)).pack(side="left")
        ctk.CTkSlider(q_row, from_=50, to=100, number_of_steps=50,
                      variable=var_quality, width=180).pack(
            side="left", padx=(8, 8))
        lbl = ctk.CTkLabel(q_row, text="85", font=ctk.CTkFont(size=11), width=30)
        lbl.pack(side="left")
        lbl_quality_ref.append(lbl)
        var_quality.trace_add(
            "write", lambda *_, lq=lbl, vq=var_quality: lq.configure(
                text=str(vq.get())))

    # ── Tab : Nouveau projet ──────────────────────────────────────────────────

    def _build_new_tab(self, parent):
        scroll = ctk.CTkScrollableFrame(parent)
        scroll.pack(fill="both", expand=True)

        self._lbl(scroll, "Client")
        self.var_client = ctk.StringVar()
        self.var_client.trace_add("write", self._auto_folder)
        self._ent(scroll, self.var_client)

        self._lbl(scroll, "Titre du projet")
        self.var_title = ctk.StringVar()
        self.var_title.trace_add("write", self._auto_slug_and_folder)
        self._ent(scroll, self.var_title)

        self._lbl(scroll, "Slug (URL)")
        self.var_slug = ctk.StringVar()
        self._ent(scroll, self.var_slug)

        self._lbl(scroll, "Nom du dossier assets  (ex: MUGLER - LES EXCEPTIONS)")
        self.var_folder = ctk.StringVar()
        self._ent(scroll, self.var_folder)

        row2 = ctk.CTkFrame(scroll, fg_color="transparent")
        row2.pack(fill="x", padx=12, pady=(14, 4))
        ctk.CTkLabel(row2, text="Année",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     width=80).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(row2, text="Rôle",
                     font=ctk.CTkFont(size=12, weight="bold")).grid(
            row=0, column=1, sticky="w", padx=(20, 0))
        self.var_year = ctk.StringVar(value=str(datetime.now().year))
        ctk.CTkEntry(row2, textvariable=self.var_year,
                     width=90, height=34).grid(row=1, column=0, sticky="w")
        self.var_role = ctk.StringVar()
        ctk.CTkEntry(row2, textvariable=self.var_role, height=34).grid(
            row=1, column=1, sticky="ew", padx=(20, 0))
        row2.columnconfigure(1, weight=1)

        self._lbl(scroll, "Tags")
        self.tag_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        self.tag_frame.pack(fill="x", padx=12, pady=4)
        self.tags_list = load_tags()
        self._tag_grid(self.tag_frame, self.tag_vars, self.tags_list)

        new_tag_row = ctk.CTkFrame(scroll, fg_color="transparent")
        new_tag_row.pack(fill="x", padx=12, pady=(4, 0))
        self.var_new_tag = ctk.StringVar()
        ctk.CTkEntry(new_tag_row, textvariable=self.var_new_tag,
                     placeholder_text="Nouveau tag...", height=32).pack(
            side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkButton(new_tag_row, text="+ Ajouter", width=110, height=32,
                      command=self._add_tag).pack(side="left")

        self._lbl(scroll, "Description")
        self.txt_desc = ctk.CTkTextbox(scroll, height=100)
        self.txt_desc.pack(fill="x", padx=12, pady=(0, 4))

        self._lbl(scroll, "Image de preview  (PREVIEW/)")
        self.var_img_lbl = ctk.StringVar(value="Aucun fichier sélectionné")
        self._file_row(scroll, self.var_img_lbl, self._pick_image,
                       "Choisir une image")

        self._lbl(scroll, "Vidéos  (VIDEO/)  — sélection multiple, optionnel")
        self.var_vid_lbl = ctk.StringVar(value="Aucun fichier sélectionné")
        self._file_row(scroll, self.var_vid_lbl, self._pick_videos,
                       "Choisir les vidéos")

        self._lbl(scroll, "URL Vimeo — optionnel")
        self.var_vimeo = ctk.StringVar()
        self._ent(scroll, self.var_vimeo)

        self._lbl(scroll, "Fichiers WIP  (WIP/)  — sélection multiple, optionnel")
        self.var_wip_lbl = ctk.StringVar(value="Aucun fichier sélectionné")
        self._file_row(scroll, self.var_wip_lbl, self._pick_wips,
                       "Choisir les WIPs")
        self.var_no_wip = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(scroll, text="Pas de WIP (section masquée sur le site)",
                        variable=self.var_no_wip).pack(
            anchor="w", padx=14, pady=(2, 0))

        self.var_webp    = ctk.BooleanVar(value=True)
        self.var_quality = ctk.IntVar(value=85)
        self._lbl_quality_ref = []
        self._webp_section(scroll, self.var_webp, self.var_quality,
                           self._lbl_quality_ref)

        ctk.CTkButton(scroll, text="  Ajouter le projet  →", height=46,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      command=self._submit).pack(fill="x", padx=12, pady=20)

    # ── Tab : Modifier un projet ──────────────────────────────────────────────

    def _build_edit_tab(self, parent):
        # horizontal split : list | form
        left = ctk.CTkFrame(parent, width=210, fg_color="gray17",
                            corner_radius=8)
        left.pack(side="left", fill="y", padx=(0, 10), pady=0)
        left.pack_propagate(False)

        ctk.CTkLabel(left, text="Projets",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(
            anchor="w", padx=10, pady=(10, 4))
        ctk.CTkButton(left, text="Actualiser", height=28, width=120,
                      command=self._reload_proj_list).pack(
            anchor="w", padx=10, pady=(0, 6))

        self.e_list_frame = ctk.CTkScrollableFrame(left, fg_color="transparent")
        self.e_list_frame.pack(fill="both", expand=True)

        right = ctk.CTkFrame(parent, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

        self.e_placeholder_lbl = ctk.CTkLabel(
            right, text="← Sélectionne un projet",
            font=ctk.CTkFont(size=13), text_color="gray")
        self.e_placeholder_lbl.place(relx=0.5, rely=0.45, anchor="center")

        self.e_form_scroll = ctk.CTkScrollableFrame(right, fg_color="transparent")

        self._build_edit_form(self.e_form_scroll)
        self._reload_proj_list()

    def _reload_proj_list(self):
        for w in self.e_list_frame.winfo_children():
            w.destroy()
        self._proj_btns = {}
        try:
            projects = load_all_projects()
        except Exception as e:
            ctk.CTkLabel(self.e_list_frame, text=str(e),
                         text_color="red", wraplength=190).pack(padx=6)
            return
        for p in projects:
            slug = p["slug"]
            label = f"{p['client']}\n{p['title']}" if p["client"] else p["title"]
            row = ctk.CTkFrame(self.e_list_frame, fg_color="transparent")
            row.pack(fill="x", padx=4, pady=2)
            btn = ctk.CTkButton(
                row, text=label, anchor="w",
                height=50, corner_radius=6,
                fg_color="transparent", hover_color="gray25",
                text_color="gray80", font=ctk.CTkFont(size=11),
                command=lambda s=slug, pr=p: self._load_edit(s, pr))
            btn.pack(side="left", fill="x", expand=True)
            ctk.CTkButton(
                row, text="🗑", width=32, height=50, corner_radius=6,
                fg_color="transparent", hover_color="#5a1a1a",
                text_color="gray50", font=ctk.CTkFont(size=14),
                command=lambda s=slug, pr=p: self._delete_project(s, pr["title"])
            ).pack(side="right")
            self._proj_btns[slug] = btn

    def _load_edit(self, slug: str, project: dict):
        for s, b in self._proj_btns.items():
            b.configure(fg_color=("gray30" if s == slug else "transparent"))
        self.e_current_slug  = slug
        self.e_image_file    = None
        self.e_video_files   = []
        self.e_wip_files     = []

        self.e_var_client.set(project.get("client", ""))
        self.e_var_title.set(project.get("title", ""))
        self.e_var_slug.set(project.get("slug", ""))
        self.e_var_folder.set("")
        self.e_var_year.set(project.get("year", ""))
        self.e_var_role.set(project.get("role", ""))
        self.e_var_vimeo.set(project.get("vimeo_url") or "")
        self.e_txt_desc.delete("1.0", "end")
        self.e_txt_desc.insert("1.0", project.get("description", ""))

        img = project.get("image", "")
        self.e_var_img_lbl.set(Path(img).name if img else "Aucun")
        self.e_existing_image = img

        existing_vids = project.get("videos") or ([project["video"]] if project.get("video") else [])
        if len(existing_vids) > 1:
            self.e_var_vid_lbl.set(f"{len(existing_vids)} vidéo(s) existante(s)")
        elif existing_vids:
            self.e_var_vid_lbl.set(Path(existing_vids[0]).name)
        else:
            self.e_var_vid_lbl.set("Aucun")
        self.e_existing_videos = existing_vids

        wips = project.get("wips", [])
        self.e_var_wip_lbl.set(f"{len(wips)} fichier(s) existant(s)" if wips else "Aucun")
        self.e_existing_wips = list(wips)
        self.e_var_no_wip.set(not bool(wips))

        checked = set(project.get("tags", []))
        for t, v in self.e_tag_vars.items():
            v.set(t in checked)

        self.e_placeholder_lbl.place_forget()
        self.e_form_scroll.pack(fill="both", expand=True)

    def _build_edit_form(self, parent):
        self._lbl(parent, "Client")
        self.e_var_client = ctk.StringVar()
        self._ent(parent, self.e_var_client)

        self._lbl(parent, "Titre du projet")
        self.e_var_title = ctk.StringVar()
        self._ent(parent, self.e_var_title)

        self._lbl(parent, "Slug (URL)")
        self.e_var_slug = ctk.StringVar()
        self._ent(parent, self.e_var_slug)

        self._lbl(parent, "Dossier assets  (laisser vide = conserver existant)")
        self.e_var_folder = ctk.StringVar()
        self._ent(parent, self.e_var_folder)

        row2 = ctk.CTkFrame(parent, fg_color="transparent")
        row2.pack(fill="x", padx=12, pady=(14, 4))
        ctk.CTkLabel(row2, text="Année",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     width=80).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(row2, text="Rôle",
                     font=ctk.CTkFont(size=12, weight="bold")).grid(
            row=0, column=1, sticky="w", padx=(20, 0))
        self.e_var_year = ctk.StringVar()
        ctk.CTkEntry(row2, textvariable=self.e_var_year,
                     width=90, height=34).grid(row=1, column=0, sticky="w")
        self.e_var_role = ctk.StringVar()
        ctk.CTkEntry(row2, textvariable=self.e_var_role, height=34).grid(
            row=1, column=1, sticky="ew", padx=(20, 0))
        row2.columnconfigure(1, weight=1)

        self._lbl(parent, "Tags")
        self.e_tag_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.e_tag_frame.pack(fill="x", padx=12, pady=4)
        self.e_tags_list = load_tags()
        self._tag_grid(self.e_tag_frame, self.e_tag_vars, self.e_tags_list)

        self._lbl(parent, "Description")
        self.e_txt_desc = ctk.CTkTextbox(parent, height=100)
        self.e_txt_desc.pack(fill="x", padx=12, pady=(0, 4))

        self._lbl(parent, "Image preview — laisser vide pour conserver")
        self.e_var_img_lbl = ctk.StringVar(value="Aucun")
        self._file_row(parent, self.e_var_img_lbl, self._e_pick_image,
                       "Choisir une image")

        self._lbl(parent, "Vidéos — laisser vide pour conserver")
        self.e_var_vid_lbl = ctk.StringVar(value="Aucun")
        self._file_row(parent, self.e_var_vid_lbl, self._e_pick_videos,
                       "Choisir les vidéos")

        self._lbl(parent, "URL Vimeo")
        self.e_var_vimeo = ctk.StringVar()
        self._ent(parent, self.e_var_vimeo)

        self._lbl(parent, "Fichiers WIP — laisser vide pour conserver")
        self.e_var_wip_lbl = ctk.StringVar(value="Aucun")
        self._file_row(parent, self.e_var_wip_lbl, self._e_pick_wips,
                       "Choisir les WIPs")
        self.e_var_no_wip = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(parent, text="Pas de WIP (section masquée sur le site)",
                        variable=self.e_var_no_wip).pack(
            anchor="w", padx=14, pady=(2, 0))

        self.e_var_webp    = ctk.BooleanVar(value=True)
        self.e_var_quality = ctk.IntVar(value=85)
        self._e_lbl_quality_ref = []
        self._webp_section(parent, self.e_var_webp, self.e_var_quality,
                           self._e_lbl_quality_ref)

        ctk.CTkButton(parent, text="  Sauvegarder  →", height=46,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      command=self._submit_edit).pack(
            fill="x", padx=12, pady=20)

    # ── Tab : Publier sur GitHub ──────────────────────────────────────────────

    def _build_publish_tab(self, parent):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(f, text="Statut Git",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     anchor="w").pack(fill="x", pady=(0, 6))
        self.txt_status = ctk.CTkTextbox(f, height=180, state="disabled")
        self.txt_status.pack(fill="x", pady=(0, 8))
        ctk.CTkButton(f, text="Actualiser", width=140,
                      command=self._refresh_status).pack(
            anchor="w", pady=(0, 16))

        ctk.CTkLabel(f, text="Message de commit",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     anchor="w").pack(fill="x", pady=(0, 6))
        self.var_commit = ctk.StringVar(value="ajout nouveau projet")
        ctk.CTkEntry(f, textvariable=self.var_commit, height=36).pack(
            fill="x", pady=(0, 16))

        ctk.CTkButton(f, text="  Publier sur GitHub  →", height=46,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color="#2ea043", hover_color="#238636",
                      command=self._publish).pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(f, text="Logs",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     anchor="w").pack(fill="x", pady=(12, 6))
        self.txt_logs = ctk.CTkTextbox(f, height=220, state="disabled")
        self.txt_logs.pack(fill="both", expand=True)

        self._refresh_status()

    # ── Actions : Nouveau projet ──────────────────────────────────────────────

    def _auto_slug_and_folder(self, *_):
        self.var_slug.set(slugify(self.var_title.get()))
        self._auto_folder()

    def _auto_folder(self, *_):
        c = self.var_client.get().strip().upper()
        t = self.var_title.get().strip().upper()
        self.var_folder.set(f"{c} - {t}" if c and t else t or c)

    def _add_tag(self):
        name = self.var_new_tag.get().strip()
        if not name:
            return
        if name in self.tags_list:
            messagebox.showwarning("Tag existant", f'"{name}" existe déjà.')
            return
        self.tags_list.append(name)
        save_tags(self.tags_list)
        self._tag_grid(self.tag_frame, self.tag_vars, self.tags_list)
        self.tag_vars[name].set(True)
        self.var_new_tag.set("")

    def _pick_image(self):
        f = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")])
        if f:
            self._image_file = f
            self.var_img_lbl.set(Path(f).name)

    def _pick_videos(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Vidéos", "*.mp4 *.mov *.webm")])
        if files:
            self._video_files = list(files)
            if len(files) == 1:
                self.var_vid_lbl.set(Path(files[0]).name)
            else:
                self.var_vid_lbl.set(f"{len(files)} vidéo(s) sélectionnée(s)")

    def _pick_wips(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Médias", "*.png *.jpg *.jpeg *.webp *.mp4 *.mov")])
        if files:
            self.wip_files = list(files)
            self.var_wip_lbl.set(f"{len(files)} fichier(s) sélectionné(s)")

    def _submit(self):
        client = self.var_client.get().strip()
        title  = self.var_title.get().strip()
        slug   = self.var_slug.get().strip()
        folder = self.var_folder.get().strip()
        year   = self.var_year.get().strip()
        role   = self.var_role.get().strip()
        desc   = self.txt_desc.get("1.0", "end").strip()
        tags   = [t for t, v in self.tag_vars.items() if v.get()]
        vimeo  = self.var_vimeo.get().strip()

        if not all([client, title, slug, folder, year, role]):
            messagebox.showerror("Champs manquants",
                "Merci de remplir : Client, Titre, Slug, Dossier, Année, Rôle.")
            return
        if not tags:
            messagebox.showerror("Tags manquants", "Sélectionne au moins un tag.")
            return
        if not self._image_file:
            messagebox.showerror("Image manquante",
                                 "Sélectionne une image de preview.")
            return

        to_webp = self.var_webp.get()
        quality = self.var_quality.get()
        try:
            project_dir = ASSETS_DIR / folder
            preview = copy_files([self._image_file], project_dir / "PREVIEW",
                                 to_webp=to_webp, quality=quality)
            video_paths = []
            if self._video_files:
                video_paths = copy_files(self._video_files, project_dir / "VIDEO")
            wip_paths = [] if self.var_no_wip.get() else (
                copy_files(self.wip_files, project_dir / "WIP",
                           to_webp=to_webp, quality=quality)
                if self.wip_files else [])
            inject_project({
                "client": client, "title": title, "slug": slug,
                "tags": tags, "role": role,
                "image": preview[0] if preview else "",
                "video": video_paths[0] if video_paths else None,
                "videos": video_paths,
                "vimeo_url": vimeo or None,
                "year": year, "description": desc, "wips": wip_paths,
            })
            messagebox.showinfo("Projet ajouté !",
                f'"{title}" a été ajouté à data.js.')
            self._reset_new()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _reset_new(self):
        for v in [self.var_client, self.var_title, self.var_slug,
                  self.var_folder, self.var_role, self.var_vimeo]:
            v.set("")
        self.var_year.set(str(datetime.now().year))
        self.txt_desc.delete("1.0", "end")
        for v in self.tag_vars.values():
            v.set(False)
        self.var_img_lbl.set("Aucun fichier sélectionné")
        self.var_vid_lbl.set("Aucun fichier sélectionné")
        self.var_wip_lbl.set("Aucun fichier sélectionné")
        self.var_no_wip.set(False)
        self._image_file   = None
        self._video_files  = []
        self.wip_files     = []

    # ── Actions : Modifier un projet ─────────────────────────────────────────

    def _e_pick_image(self):
        f = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")])
        if f:
            self.e_image_file = f
            self.e_var_img_lbl.set(Path(f).name)

    def _e_pick_videos(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Vidéos", "*.mp4 *.mov *.webm")])
        if files:
            self.e_video_files = list(files)
            if len(files) == 1:
                self.e_var_vid_lbl.set(Path(files[0]).name)
            else:
                self.e_var_vid_lbl.set(f"{len(files)} vidéo(s) sélectionnée(s)")

    def _delete_project(self, slug: str, title: str):
        if not messagebox.askyesno(
                "Confirmer la suppression",
                f'Supprimer "{title}" de data.js ?\n\n'
                "Les fichiers assets ne seront pas supprimés."):
            return
        try:
            delete_project_from_data_js(slug)
            if self.e_current_slug == slug:
                self.e_current_slug = None
                self.e_form_scroll.pack_forget()
                self.e_placeholder_lbl.place(relx=0.5, rely=0.45, anchor="center")
            self._reload_proj_list()
            messagebox.showinfo("Supprimé", f'"{title}" a été retiré de data.js.')
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _e_pick_wips(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Médias", "*.png *.jpg *.jpeg *.webp *.mp4 *.mov")])
        if files:
            self.e_wip_files = list(files)
            self.e_var_wip_lbl.set(f"{len(files)} nouveau(x) fichier(s)")

    def _submit_edit(self):
        if not self.e_current_slug:
            messagebox.showerror("Aucun projet",
                                 "Sélectionne un projet dans la liste.")
            return
        client = self.e_var_client.get().strip()
        title  = self.e_var_title.get().strip()
        slug   = self.e_var_slug.get().strip()
        folder = self.e_var_folder.get().strip()
        year   = self.e_var_year.get().strip()
        role   = self.e_var_role.get().strip()
        desc   = self.e_txt_desc.get("1.0", "end").strip()
        tags   = [t for t, v in self.e_tag_vars.items() if v.get()]
        vimeo  = self.e_var_vimeo.get().strip()

        if not all([client, title, slug, year, role]):
            messagebox.showerror("Champs manquants",
                "Merci de remplir : Client, Titre, Slug, Année, Rôle.")
            return
        if not tags:
            messagebox.showerror("Tags manquants", "Sélectionne au moins un tag.")
            return

        to_webp = self.e_var_webp.get()
        quality = self.e_var_quality.get()
        try:
            if folder:
                project_dir = ASSETS_DIR / folder
            else:
                img_path = self.e_existing_image.replace("%20", " ")
                parts = list(Path(img_path).parts)
                if "projects" in parts:
                    project_dir = ASSETS_DIR / parts[parts.index("projects") + 1]
                else:
                    project_dir = ASSETS_DIR / slugify(title)

            image_path = (copy_files([self.e_image_file], project_dir / "PREVIEW",
                                     to_webp=to_webp, quality=quality)[0]
                          if self.e_image_file else self.e_existing_image)
            if self.e_video_files:
                video_paths = copy_files(self.e_video_files, project_dir / "VIDEO")
            else:
                video_paths = self.e_existing_videos
            wip_paths = [] if self.e_var_no_wip.get() else (
                copy_files(self.e_wip_files, project_dir / "WIP",
                           to_webp=to_webp, quality=quality)
                if self.e_wip_files else self.e_existing_wips)

            update_project_in_data_js(self.e_current_slug, {
                "client": client, "title": title, "slug": slug,
                "tags": tags, "role": role,
                "image": image_path,
                "video": video_paths[0] if video_paths else None,
                "videos": video_paths,
                "vimeo_url": vimeo or None,
                "year": year, "description": desc, "wips": wip_paths,
            })
            self.e_current_slug = slug
            self._reload_proj_list()
            messagebox.showinfo("Sauvegardé !",
                f'"{title}" a été mis à jour dans data.js.')
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # ── Actions : Publier ─────────────────────────────────────────────────────

    def _refresh_status(self):
        _, out, err = run_git("status")
        self._set(self.txt_status, out + (("\n" + err) if err.strip() else ""))

    def _publish(self):
        msg = self.var_commit.get().strip()
        if not msg:
            messagebox.showerror("Message vide", "Entre un message de commit.")
            return
        for label, git_args in [
            ("── git add -A",  ["add", "-A"]),
            ("── git commit",  ["commit", "-m", msg]),
            ("── git push",    ["push"]),
        ]:
            self._log(label + " " + "─" * (34 - len(label)))
            code, out, err = run_git(*git_args)
            self._log(out + err)
            if code != 0:
                if label == "── git commit" \
                        and "nothing to commit" in (out + err):
                    continue
                messagebox.showerror(f"Erreur", err or out)
                self._refresh_status()
                return
        messagebox.showinfo("Publié !", "Le site est à jour sur GitHub.")
        self._refresh_status()

    def _log(self, text: str):
        self.txt_logs.configure(state="normal")
        self.txt_logs.insert("end", text + "\n")
        self.txt_logs.see("end")
        self.txt_logs.configure(state="disabled")

    def _set(self, widget, text: str):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")


# ── Lancement ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()

