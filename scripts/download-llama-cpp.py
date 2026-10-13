#!/usr/bin/env python3
"""Fetch the ROCm gfx1151 llama.cpp release recorded for a device/profile."""
import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request

RELEASES = {
    "395": ("unslothai/llama.cpp", "b10909-mix-bea84f7"),
    "388-flagship": ("unslothai/llama.cpp", "b10830-mix-d5c17a0"),
    "388-balanced": ("ggml-org/llama.cpp", "b11065"),
}


def release_data(repo, tag):
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/releases/tags/{tag}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "geekom-local-ai-assistant/1"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", choices=RELEASES)
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("bin/ubuntu"))
    parser.add_argument("--list-assets", action="store_true")
    parser.add_argument("--source", action="store_true", help="Download the tagged source instead of a prebuilt archive")
    args = parser.parse_args()
    repo, tag = RELEASES[args.profile]
    assets = release_data(repo, tag)["assets"] if args.list_assets or not args.source else []
    if args.list_assets:
        print("\n".join(asset["name"] for asset in assets))
        return
    matches = [a for a in assets if re.search(r"linux-x64-rocm-gfx1151.*\.tar(?:\.gz|\.xz)?$", a["name"])]
    target = args.output.expanduser().resolve() / f"{args.profile}-{tag}"
    if target.exists():
        raise SystemExit(f"Target already exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if args.source or not matches:
        print(f"No selected prebuilt ROCm gfx1151 archive; fetching tagged source {repo}@{tag}")
        subprocess.run(["git", "clone", "--depth", "1", "--branch", tag,
                        f"https://github.com/{repo}.git", str(target)], check=True)
        print(f"Source installed in {target}")
        print('Build with: HIPCXX="$(hipconfig -l)/clang" HIP_PATH="$(hipconfig -R)" '
              'cmake -S . -B build -DGGML_HIP=ON -DGPU_TARGETS=gfx1151 '
              '-DCMAKE_BUILD_TYPE=Release && cmake --build build -j')
        return
    if len(matches) != 1:
        raise SystemExit(f"Found {len(matches)} matching gfx1151 archives; inspect with --list-assets")
    asset = matches[0]
    with tempfile.TemporaryDirectory(dir=target.parent) as scratch:
        archive = pathlib.Path(scratch) / asset["name"]
        request = urllib.request.Request(asset["browser_download_url"],
                                         headers={"User-Agent": "geekom-local-ai-assistant/1"})
        print(f"Downloading {asset['browser_download_url']}")
        with urllib.request.urlopen(request, timeout=120) as response, archive.open("wb") as output:
            shutil.copyfileobj(response, output)
        if archive.stat().st_size != asset["size"]:
            raise SystemExit("Archive size differs from GitHub release metadata")
        digest = asset.get("digest")
        if digest and digest.startswith("sha256:"):
            sha = hashlib.sha256()
            with archive.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    sha.update(block)
            if sha.hexdigest() != digest.removeprefix("sha256:"):
                raise SystemExit("Archive SHA-256 differs from GitHub release metadata")
        extracted = pathlib.Path(scratch) / "unpacked"
        extracted.mkdir()
        with tarfile.open(archive) as bundle:
            for member in bundle.getmembers():
                member_path = pathlib.PurePosixPath(member.name)
                if member_path.is_absolute() or ".." in member_path.parts or not (
                    member.isfile() or member.isdir() or member.issym() or member.islnk()
                ):
                    raise SystemExit(f"Unsafe archive member: {member.name}")
            bundle.extractall(extracted, filter="data")
        if not list(extracted.rglob("llama-server")):
            raise SystemExit("Archive does not contain llama-server")
        (extracted / "download-source.json").write_text(json.dumps({
            "repository": repo, "tag": tag, "asset": asset["name"],
            "url": asset["browser_download_url"], "size": asset["size"]}, indent=2) + "\n")
        extracted.rename(target)
    print(f"Installed in {target}")


if __name__ == "__main__":
    main()
