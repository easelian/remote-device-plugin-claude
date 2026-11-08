#!/usr/bin/env python3
"""Check public source consistency without contacting a server or using credentials."""

import json
import re
import struct
from pathlib import Path
from urllib.parse import unquote, urlsplit


HAN_CHARACTERS = re.compile(
    r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
    r"\U00020000-\U0002fa1f\U00030000-\U000323af]"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_source(root, files):
    root = root.resolve()
    packaged = set(files)
    require(len(packaged) == len(files), "Duplicate package path")
    for relative in files:
        source = root / relative
        require(not source.is_symlink() and source.resolve() == source and source.is_file(),
                f"Expected regular package file: {relative}")
        require(not HAN_CHARACTERS.search(relative.as_posix()),
                f"Package paths must use English: {relative}")
        if relative.suffix != ".png":
            body = source.read_text(encoding="utf-8")
            require(not HAN_CHARACTERS.search(body),
                    f"Repository text must use English: {relative}")
        if relative.suffix == ".json":
            decoded = json.loads(body)
            require(not HAN_CHARACTERS.search(json.dumps(decoded, ensure_ascii=False)),
                    f"JSON text must use English: {relative}")

    plugin = root / "plugins/remote-device-hub"
    manifest = json.loads((plugin / ".claude-plugin/plugin.json").read_text())
    market = json.loads((root / ".claude-plugin/marketplace.json").read_text())
    servers = json.loads((plugin / ".mcp.json").read_text())["mcpServers"]
    connection = json.loads((root / "connector/connection.json").read_text())
    require(manifest["name"] == "remote-device-hub", "Unexpected plugin identity")
    require(market["name"] == "easelian-rdh", "Unexpected marketplace identity")
    require(len(market["plugins"]) == 1, "Expected one marketplace plugin")
    entry = market["plugins"][0]
    require(entry["name"] == manifest["name"] and entry["source"] == "./plugins/remote-device-hub",
            "Marketplace source differs from plugin")
    require(servers == {"remote-device-hub": {
        "type": connection["transport"], "url": connection["mcp_url"]}},
        "Plugin MCP configuration differs from public connection reference")
    require(connection["transport"] == "http", "Expected HTTP MCP transport")
    require(manifest["author"]["name"] == connection["publisher"] == market["owner"]["name"],
            "Publisher names differ")
    require(manifest["author"]["email"] == connection["support_email"] == market["owner"]["email"],
            "Contact emails differ")
    require(manifest["privacyPolicyUrl"] == connection["privacy_url"], "Privacy URLs differ")
    require(manifest["homepage"].rstrip("/") == connection["website_url"].rstrip("/"),
            "Product URLs differ")
    require(manifest["license"] == "Apache-2.0", "Unexpected license")
    require((plugin / "LICENSE").read_bytes() == (root / "LICENSE").read_bytes(),
            "Plugin and repository licenses differ")

    oauth = connection["oauth"]
    require(oauth["required"] is True and oauth["method"] == "oauth_dcr"
            and oauth["pkce"] == "S256" and oauth["scope"] == "devices:control",
            "Unexpected OAuth reference")
    urls = [v for k, v in connection.items() if k.endswith("_url")]
    urls += [oauth["issuer"], oauth["authorization_server_metadata_url"], oauth["hosted_callback"]]
    for url in urls:
        parsed = urlsplit(url)
        require(parsed.scheme == "https" and parsed.hostname and not parsed.username
                and not parsed.password and not parsed.query and not parsed.fragment,
                "Public connection URLs must be HTTPS and contain no credentials or parameters")

    links = 0
    for relative in files:
        if relative.suffix != ".md":
            continue
        source = root / relative
        body = source.read_text()
        for target in re.findall(r"\]\(([^\s)]+)\)", body):
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path:
                continue
            resolved = (source.parent / unquote(parsed.path)).resolve()
            require(resolved.is_relative_to(root) and resolved.is_file(),
                    f"Missing or external local link in {relative}: {target}")
            require(resolved.relative_to(root) in packaged,
                    f"Linked file is absent from archive: {target}")
            if source.is_relative_to(plugin):
                require(resolved.is_relative_to(plugin), f"Plugin link leaves its install folder: {target}")
            links += 1

    readme = (plugin / "README.md").read_text()
    require(len(re.sub(r"```.*?```", "", readme, flags=re.S).split()) >= 40,
            "Plugin README is too short")
    icon = (plugin / "assets/icon.png").read_bytes()
    require(icon.startswith(b"\x89PNG\r\n\x1a\n") and len(icon) >= 24, "Invalid PNG header")
    width, height = struct.unpack(">II", icon[16:24])
    require(width == height == 512, "Expected shared 512 x 512 icon")
    for source in plugin.rglob("*"):
        if source.is_file():
            require(source.relative_to(root) in packaged, f"Unpackaged plugin file: {source.name}")
            require(source.stat().st_size < 5 * 1024 * 1024, "Plugin file exceeds directory size limit")
    return {"package_files": len(files), "local_links": links, "icon": f"{width}x{height}"}


if __name__ == "__main__":
    from package import FILES, ROOT

    print(json.dumps(check_source(ROOT, FILES), indent=2))
