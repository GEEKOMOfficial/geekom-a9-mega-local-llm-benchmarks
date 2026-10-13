#!/usr/bin/env python3
"""Download recommended and separately recorded GGUF files from Hugging Face."""
import argparse
import json
import pathlib
import subprocess
import urllib.request

MODELS = {
    "flagship": {
        "repo": "unsloth/Qwen3.8-Flash-Next-GGUF",
        "files": [
            *[f"UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-{i:05d}-of-00004.gguf" for i in range(1, 5)],
            "MTP/mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf",
        ],
        "destination": "Qwen3.8-Flash-Next-UD-Q4_K_XL",
    },
    "balanced": {
        "repo": "unsloth/Qwen3.6-35B-A3B-MTP-GGUF",
        "files": ["Qwen3.6-35B-A3B-UD-Q4_K_M.gguf"],
        "destination": "Qwen3.6-35B-A3B-MTP-UD-Q4_K_M",
    },
    "lightweight": {
        "repo": "openbmb/MiniCPM5-2B-GGUF",
        "files": ["MiniCPM5-2B-Q4_K_M.gguf"],
        "destination": "MiniCPM5-2B-Q4_K_M",
    },
    "deepseek-q2": {
        "repo": "unsloth/DeepSeek-V4-Flash-0731-GGUF",
        "files": [
            f"UD-Q2_K_XL/DeepSeek-V4-Flash-0731-UD-Q2_K_XL-{i:05d}-of-00003.gguf"
            for i in range(1, 4)
        ],
        "destination": "DeepSeek-V4-Flash-0731-UD-Q2_K_XL",
    },
    "qwen27b-fp4": {
        "repo": "julianmb/Qwen-3.8-27B-ROCmFP4-FAST-GGUF",
        "files": ["Qwen3.8-27B-ROCmFP4-FAST.gguf"],
        "destination": "Qwen3.8-27B-ROCmFP4-FAST",
    },
    "gemma4-q4": {
        "repo": "google/gemma-4-31B-it-qat-q4_0-gguf",
        "files": ["gemma-4-31B_q4_0-it.gguf", "gemma-4-31B-it-mmproj.gguf"],
        "destination": "gemma-4-31B-it-qat-q4_0",
    },
    "flash-q4km": {
        "repo": "DhruvalLabs/Qwen3.8-Flash-Next-GGUF",
        "files": [
            f"Qwen3.8-Flash-Next-Q4_K_M-{i:05d}-of-00003.gguf"
            for i in range(1, 4)
        ],
        "destination": "Qwen3.8-Flash-Next-Q4_K_M",
    },
}

RECOMMENDED = ("flagship", "balanced", "lightweight")


def repo_revision(repo):
    request = urllib.request.Request(
        f"https://huggingface.co/api/models/{repo}",
        headers={"User-Agent": "geekom-local-ai-assistant/1"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["sha"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profiles", nargs="+", choices=[*MODELS, "recommended", "all"])
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("models"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if "all" in args.profiles:
        selected = list(MODELS)
    elif "recommended" in args.profiles:
        selected = list(dict.fromkeys([*RECOMMENDED, *(p for p in args.profiles if p != "recommended")]))
    else:
        selected = list(dict.fromkeys(args.profiles))
    root = args.output.expanduser().resolve()
    local_hf = pathlib.Path(__file__).resolve().parent.parent / ".venv" / "bin" / "hf"
    hf = str(local_hf) if local_hf.is_file() else "hf"
    for name in selected:
        entry = MODELS[name]
        target = root / entry["destination"]
        lock = target / "download-source.json"
        if lock.exists():
            metadata = json.loads(lock.read_text())
            if metadata.get("repository") != entry["repo"]:
                raise SystemExit(f"Repository mismatch in {lock}")
            revision = metadata["revision"]
        elif args.dry_run:
            revision = "<resolved from Hugging Face at download time>"
        else:
            revision = repo_revision(entry["repo"])
        print(f"{name}: {entry['repo']} @ {revision} -> {target}")
        for filename in entry["files"]:
            print(f"  {filename}")
        if args.dry_run:
            continue
        target.mkdir(parents=True, exist_ok=True)
        if not lock.exists():
            lock.write_text(json.dumps({"repository": entry["repo"], "revision": revision,
                                        "files": entry["files"]}, indent=2) + "\n")
        # hf download handles Xet and verifies transfers. Keep upstream subdirectories
        # so split GGUF files and the MTP head can be identified unambiguously.
        command = [hf, "download", entry["repo"], *entry["files"],
                   "--revision", revision, "--local-dir", str(target)]
        try:
            subprocess.run(command, check=True)
        except FileNotFoundError:
            raise SystemExit("Missing 'hf' CLI. Run scripts/setup-ubuntu-26.04.sh first.")
        missing = [filename for filename in entry["files"] if not (target / filename).is_file()]
        if missing:
            raise SystemExit(f"Download incomplete: {missing}")
        print(f"Saved source lock: {lock}")


if __name__ == "__main__":
    main()
