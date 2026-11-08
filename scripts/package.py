#!/usr/bin/env python3
"""Build a deterministic archive of the plugin and its public connector materials."""

import hashlib
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = Path("plugins/remote-device-hub")
SKILL = PLUGIN / "skills/remote-device-operations"
FILES = [
    Path("README.md"),
    Path("LICENSE"),
    Path(".gitignore"),
    Path(".claude-plugin/marketplace.json"),
    Path("scripts/package.py"),
    Path("scripts/check.py"),
    Path("connector/README.md"),
    Path("connector/connection.json"),
    Path("connector/tools.md"),
    Path("docs/data-handling.md"),
    PLUGIN / ".claude-plugin/plugin.json",
    PLUGIN / ".mcp.json",
    PLUGIN / "LICENSE",
    PLUGIN / "README.md",
    PLUGIN / "assets/icon.png",
    SKILL / "SKILL.md",
    *(SKILL / "references" / f"{name}.md" for name in ("files", "processes", "browser", "recovery")),
]


def main():
    from check import check_source

    check_source(ROOT, FILES)
    manifest = json.loads((ROOT / PLUGIN / ".claude-plugin/plugin.json").read_text())
    version = manifest["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
        raise ValueError("Invalid plugin version")
    payload = {}
    for relative in FILES:
        source = ROOT / relative
        if source.is_symlink() or source.resolve() != source or not source.is_file():
            raise ValueError(f"Expected regular package file: {relative}")
        data = source.read_bytes()
        if relative.suffix == ".json":
            json.loads(data)
        payload[f"remote-device-plugin-claude/{relative.as_posix()}"] = data

    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    archive = output / f"remote-device-hub-claude-{version}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, data in sorted(payload.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, data)
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None or set(bundle.namelist()) != set(payload):
            raise ValueError("Archive verification failed")
        for name, data in payload.items():
            if bundle.read(name) != data:
                raise ValueError(f"Archive content mismatch: {name}")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(".zip.sha256").write_text(f"{digest}  {archive.name}\n")
    print(f"{archive}\n{len(payload)} files; SHA-256 {digest}")


if __name__ == "__main__":
    main()
