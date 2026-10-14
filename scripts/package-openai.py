"""Build a portable public upload from Revelica's shared Codex source."""

import argparse
import copy
import json
import re
import struct
import zipfile
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "plugins" / "revelica"


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a new ZIP at this path; never overwrite an archive.")
    args = parser.parse_args()
    source_manifest = json.loads((SOURCE / ".codex-plugin/plugin.json").read_text())
    require(source_manifest["name"] == SOURCE.name, "Plugin name must match its folder.")
    version = source_manifest["version"]
    require(
        re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[\w.-]+)?(?:\+[\w.-]+)?", version),
        "An explicit semantic version is required.",
    )
    require(not (SOURCE / ".app.json").exists(), "Public uploads cannot contain .app.json.")
    require(source_manifest.get("apps") is None, "Public uploads cannot declare apps.")

    # Codex's compatibility manifest keeps interface at the top level. The
    # portable submission importer reads extensions.com.openai.interface.
    manifest = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        **{key: copy.deepcopy(source_manifest[key]) for key in (
            "name", "version", "description", "author", "homepage",
            "repository", "license", "keywords", "extensions",
        ) if key in source_manifest},
    }
    openai = manifest.setdefault("extensions", {}).setdefault("com.openai", {})
    require(openai.get("apps") is None, "Public uploads cannot declare OpenAI apps.")
    interface = copy.deepcopy(source_manifest["interface"])
    require(
        "interface" not in openai or openai["interface"] == interface,
        "Codex and portable listing fields disagree.",
    )
    openai["interface"] = interface

    for key, maximum in (("displayName", 30), ("shortDescription", 30),
                         ("longDescription", 4000), ("developerName", 80)):
        value = interface.get(key)
        require(isinstance(value, str) and 0 < len(value) <= maximum,
                f"Invalid listing field: {key}.")
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        value = interface.get(key, "")
        url = urlsplit(value)
        require(url.scheme == "https" and url.hostname and not url.username
                and not url.password and len(value) <= 1024,
                f"A public HTTPS {key} is required.")
    prompts = interface.get("defaultPrompt", [])
    if isinstance(prompts, str):
        prompts = [prompts]
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3,
            "Provide one to three starting prompts.")
    require(all(isinstance(p, str) and p.strip() and len(p) <= 128
                and "\n" not in p and "\r" not in p for p in prompts),
            "Starting prompts must be nonblank single lines of at most 128 characters.")
    require(len({" ".join(p.split()) for p in prompts}) == len(prompts),
            "Starting prompts must be unique.")

    mcp = json.loads((SOURCE / ".mcp.json").read_text())
    mcp["$schema"] = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
    servers = mcp["mcpServers"]
    require(len(servers) == 1, "Review cases currently describe exactly one MCP server.")
    for server in servers.values():
        require(server.get("url", "").startswith("https://") and not server.get("command"),
                "This public export requires a remote HTTPS MCP server.")
        # Claude/Codex name this transport http; Agent Plugins names it
        # streamable-http. Preserve the actual endpoint and authentication.
        if server.get("type") == "http":
            server["type"] = "streamable-http"

    cases = openai.get("review", {}).get("test_cases", {})
    for kind, minimum in (("positive", 5), ("negative", 3)):
        entries = cases.get(kind, [])
        require(len(entries) >= minimum, f"Review needs at least {minimum} {kind} cases.")
        fields = ("description", "prompt") + (
            ("tools_triggered", "expected_behavior") if kind == "positive" else ()
        )
        require(all(all(isinstance(case.get(k), str) and case[k].strip() for k in fields)
                    for case in entries), f"Incomplete {kind} review cases.")

    files = {"plugin.json": encode(manifest), "mcp.json": encode(mcp)}
    for folder in ("assets", "skills"):
        for path in sorted((SOURCE / folder).rglob("*")):
            require(not path.is_symlink(), f"Symlinks cannot be packaged: {path}")
            if path.is_file() and path.name != ".DS_Store":
                files[path.relative_to(SOURCE).as_posix()] = path.read_bytes()
    for key in ("logo", "composerIcon", "logoDark", "composerIconDark"):
        if key not in interface:
            continue
        data = files.get(interface[key].removeprefix("./"))
        require(data is not None and data[:8] == b"\x89PNG\r\n\x1a\n",
                f"{key} must reference a contained PNG file.")
        width, height = struct.unpack(">II", data[16:24])
        minimum = 256 if key.startswith("logo") else 48
        require(width == height and minimum <= width <= 4096 and len(data) <= 5 * 1024**2,
                f"{key} must be square, at least {minimum}px, and at most 5 MiB.")

    output = (args.output or ROOT / "dist" / f"revelica-openai-{version}.zip").resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        destination = output.open("xb")
    except FileExistsError:
        raise SystemExit(f"Refusing to overwrite {output}; choose a new --output path or bump the version.")
    with destination, zipfile.ZipFile(destination, "w") as archive:
        for name, data in sorted(files.items()):
            # Fixed timestamps and permissions make repeat builds reproducible
            # with the same Python/zlib toolchain, independent of file mtimes.
            info = zipfile.ZipInfo(f"{SOURCE.name}/{name}", date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    with zipfile.ZipFile(output) as archive:
        require(archive.testzip() is None, "ZIP integrity check failed.")
        exported = json.loads(archive.read("revelica/plugin.json"))
        require(exported["extensions"]["com.openai"]["interface"] == interface,
                "Exported listing metadata does not match its source.")
        for name in archive.namelist():
            print(name)
    print(f"\nBuilt {output}")
    if not openai.get("review", {}).get("demo_recording_url"):
        print("Demo recording is absent from source; check the saved portal draft.")
    print("Reviewer access, country targeting, scans, and attestations require portal verification.")


if __name__ == "__main__":
    main()
