"""Check original SVGs and static browser demonstration asset integrity."""
import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images_without_alt = 0

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if tag == "img" and not props.get("alt"):
            self.images_without_alt += 1
        for key in ("src", "href"):
            url = props.get(key)
            if url:
                self.links.append(url)

def validate(root: Path = ROOT) -> dict:
    images = sorted((root / "docs" / "images").glob("*.svg"))
    if len(images) != 10:
        raise AssertionError(f"Expected 10 original project SVG illustrations; found {len(images)}")
    for path in images:
        doc = ET.parse(path)
        if doc.getroot().tag != "{http://www.w3.org/2000/svg}svg":
            raise AssertionError(f"Invalid SVG root: {path}")
    gallery = (root / "docs" / "IMAGE_GALLERY.md").read_text(encoding="utf-8")
    for path in images:
        if path.name not in gallery:
            raise AssertionError(f"Gallery missing {path.name}")
    html_path = root / "site" / "index.html"
    refs = References()
    refs.feed(html_path.read_text(encoding="utf-8"))
    if refs.images_without_alt:
        raise AssertionError("Static site has an image without alt text")
    valid_files = 0
    for uri in refs.links:
        parsed = urlsplit(uri)
        if parsed.scheme or parsed.netloc or not parsed.path or parsed.path == "/":
            continue
        rel = unquote(parsed.path)
        if rel.startswith("/"):
            continue  # Absolute root URLs are host-owned.
        candidate = (html_path.parent / rel).resolve()
        if not candidate.is_relative_to(html_path.parent.resolve()) or not candidate.exists():
            raise AssertionError(f"Broken static reference: {uri}")
        valid_files += 1
    policies = json.loads((root / "site" / "policies.json").read_text(encoding="utf-8"))
    if len(policies) != 6 or len({p["source"] for p in policies}) != 6:
        raise AssertionError("Expected six uniquely sourced fictional demo policy articles")
    for policy in policies:
        if not policy["source"].endswith(".md") or not policy["text"].strip():
            raise AssertionError("Invalid fictional policy source")
    return {"original_svg_count":len(images),"browser_demo_policies":len(policies),
            "verified_internal_references": valid_files,
            "status":"ok", "description":"Source/asset integrity only, not live HTTP or browser correctness"}

if __name__ == "__main__":
    print(json.dumps(validate(), indent=2))
