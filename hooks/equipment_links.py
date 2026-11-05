"""
MkDocs-хук: подставляет ссылки из equipment-links.txt в таблицы страницы «Оборудование».

Файл equipment-links.txt (корень репозитория) — одна строка = одна ссылка:
    Паяльник: https://www.ozon.ru/product/...
    Термоклеевой пистолет: https://... — Склеить детали
Название ищется в первой колонке таблиц docs/equipment.md (регистр, «ё/е» и кавычки не важны).
Ссылки — кнопками магазинов столбиком; несколько ссылок на один инструмент встают друг под другом. Незнакомое название — новой строкой
в разделе «Другое» (текст после « — » идёт в колонку «Для чего»).
Строка без ссылки — предупреждение, при `mkdocs build --strict` сборка остановится.
"""
from __future__ import annotations

import logging
import os
import re
from urllib.parse import urlparse

log = logging.getLogger("mkdocs.hooks.equipment")

LINKS_FILE = "equipment-links.txt"
PAGE = "equipment.md"
OTHER_HEADING = "## :material-dots-horizontal: Другое"
TABLE_HEADER = ("| Инструмент | Для чего | Ссылка |", "|---|---|---|")
PLACEHOLDER = "*скоро*"

URL_RE = re.compile(r"https?://\S+", re.I)
ROW_RE = re.compile(r"^\|(?P<name>[^|]*)\|(?P<desc>[^|]*)\|(?P<link>.*)\|\s*$")

SHOPS = [  # (часть домена, подпись)
    ("ozon.", "Ozon"),
    ("wildberries.", "Wildberries"),
    ("wb.ru", "Wildberries"),
    ("market.yandex.", "Яндекс Маркет"),
    ("aliexpress.", "AliExpress"),
    ("ali.click", "AliExpress"),
    ("chipdip.", "ЧипДип"),
    ("amperka.", "Амперка"),
    ("megamarket.", "Мегамаркет"),
    ("avito.", "Авито"),
]


def norm(name: str) -> str:
    s = name.lower().replace("ё", "е")
    s = re.sub(r"[«»\"'*`_]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def _cell(text: str) -> str:
    return re.sub(r"\s+", " ", text).replace("|", "\\|").strip()


def _url(url: str) -> str:
    return url.strip().replace(" ", "%20").replace("(", "%28").replace(")", "%29")


def shop_label(url: str) -> str:
    host = (urlparse(url).netloc or url).lower()
    for part, label in SHOPS:
        if part in host:
            return label
    return host.removeprefix("www.") or "Ссылка"


def parse_links(text: str) -> list[tuple[str, str, str]]:
    """[(название, url, описание)] из текста файла; строки с # и пустые пропускаются."""
    out = []
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = URL_RE.search(line)
        if not m:
            log.warning("%s, строка %d: нет ссылки (нужно «Название: https://…»): %s", LINKS_FILE, n, line)
            continue
        url = m.group(0).rstrip(".,;")
        name = line[:m.start()].strip(" \t:—–-|")
        desc = line[m.end():].strip(" \t:—–-|")
        if not name:
            log.warning("%s, строка %d: нет названия перед ссылкой: %s", LINKS_FILE, n, line)
            continue
        out.append((name, url, desc))
    return out


SOON = '<span class="mr-soon">скоро</span>'


def _links_md(urls: list[str]) -> str:
    """Кнопки магазинов (на сайте — столбиком, см. .mr-buy в extra.css); повторы нумеруются."""
    seen: dict[str, int] = {}
    out = []
    for u in urls:
        label = shop_label(u)
        seen[label] = seen.get(label, 0) + 1
        if seen[label] > 1:
            label = f"{label} №{seen[label]}"
        out.append(f"[:material-cart-outline: {label}]({_url(u)}){{ .mr-buy }}")
    return " ".join(out)


def apply_links(markdown: str, entries: list[tuple[str, str, str]]) -> str:
    # группируем по нормализованному названию, сохраняя порядок
    groups: dict[str, dict] = {}
    for name, url, desc in entries:
        g = groups.setdefault(norm(name), {"name": name, "urls": [], "desc": ""})
        if url not in g["urls"]:
            g["urls"].append(url)
        g["desc"] = g["desc"] or desc

    used: set[str] = set()
    lines = markdown.split("\n")
    in_comment = False
    for i, line in enumerate(lines):
        if "<!--" in line:
            in_comment = True
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        m = ROW_RE.match(line)
        if not m:
            continue
        key = norm(m.group("name"))
        if re.fullmatch(r"[\s:-]*", m.group("name")):
            continue
        old = m.group("link").strip()
        empty = old in ("", PLACEHOLDER, "—")
        g = groups.get(key)
        if g:
            used.add(key)
            new = _links_md(g["urls"])
            cell = new if empty else f"{old} {new}"
        elif old == PLACEHOLDER:
            cell = SOON
        else:
            continue
        lines[i] = f"|{m.group('name')}|{m.group('desc')}| {cell} |"

    rest = [g for k, g in groups.items() if k not in used]
    if rest:
        rows = [f"| {_cell(g['name'])} | {_cell(g['desc']) or '—'} | {_links_md(g['urls'])} |" for g in rest]
        while lines and not lines[-1].strip():
            lines.pop()
        lines += ["", OTHER_HEADING, "", *TABLE_HEADER, *rows, ""]
    return "\n".join(lines)


def on_page_markdown(markdown, page, config, files, **kwargs):
    if page.file.src_uri != PAGE:
        return markdown
    path = os.path.join(os.path.dirname(config.config_file_path), LINKS_FILE)
    try:
        with open(path, encoding="utf-8-sig") as f:
            text = f.read()
    except FileNotFoundError:
        return markdown
    return apply_links(markdown, parse_links(text))
