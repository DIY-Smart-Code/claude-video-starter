#!/usr/bin/env python3
"""Start a new cinematic film from templates/cinematic.

Usage:
    python scripts/new-cinematic-video.py <slug> "Film title"

Copies the toolkit (lib/), fonts, GSAP, the demo cut (index.html) and film.json as the worked example
into videos/<slug>/, without the demo's score, renders or docs. Then follow /cinematic.
Python 3.8+, standard library only.
"""
import json
import re
import shutil
import sys
from pathlib import Path

SKIP = {"build", "out", "qa", "snapshots", "renders", "__pycache__", "finish.html", "contact.png", "storyboard.html", ".hyperframes",
        "README.md", "DESIGN.md", "API.md", "score"}        # docs stay in templates/cinematic/; the score is per film


def main() -> None:
    if len(sys.argv) < 2 or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", sys.argv[1]):
        sys.exit(__doc__)
    slug = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else slug.replace("-", " ").capitalize()
    repo = Path(__file__).resolve().parent.parent
    src, dst = repo / "templates" / "cinematic", repo / "videos" / slug
    if dst.exists():
        sys.exit(f"{dst} already exists")
    shutil.copytree(src, dst, ignore=lambda d, names: [n for n in names if n in SKIP or n.endswith(".pyc")])
    (dst / "assets" / "score" / "sfx").mkdir(parents=True, exist_ok=True)
    (dst / "meta.json").write_text(json.dumps({"id": slug, "name": title}, indent=2) + "\n", encoding="utf-8")
    pkg = dst / "package.json"
    pkg.write_text(pkg.read_text(encoding="utf-8").replace('"name": "cinematic"', f'"name": "{slug}"'), encoding="utf-8")
    film = json.loads((dst / "film.json").read_text(encoding="utf-8"))
    film["title"] = title
    (dst / "film.json").write_text(json.dumps(film, indent=2) + "\n", encoding="utf-8")
    print(f"created videos/{slug} from templates/cinematic (index.html and film.json are the Nocturne demo: replace them)")
    print("read templates/cinematic/DESIGN.md and API.md, then:\n"
          f"  python scripts/film.py score videos/{slug}   # music + hits from film.json\n"
          f"  python scripts/film.py all   videos/{slug}   # cut, mix, finish, contact sheet")


if __name__ == "__main__":
    main()
