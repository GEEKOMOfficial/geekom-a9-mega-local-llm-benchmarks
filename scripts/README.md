# Script setup and downloads

Run the commands below from the repository root.

## Ubuntu 26.04 setup and downloads

Run these commands on a **native Ubuntu 26.04 x86-64** A9 Mega after cloning this repository. Downloads are large; choose a disk with sufficient free space. The setup script installs system prerequisites, a local Hugging Face CLI virtual environment, and AMD ROCm 10.0.0. AMD's Ubuntu 26.04 guidance uses the inbox kernel driver for supported Ryzen APUs, so the script does not replace it with a DKMS driver. The benchmark archive records graphics driver `31.50.0.0`; check your actual driver and ROCm versions before comparing results. [AMD ROCm 10.0.0 installation guide](https://rocm.docs.amd.com/en/docs-10.0.0/install/rocm.html)

```bash
bash scripts/setup-ubuntu-26.04.sh
python3 scripts/download-models.py balanced lightweight
python3 scripts/download-llama-cpp.py 388-balanced
```

For the A9 Mega 395 flagship, run `python3 scripts/download-models.py flagship` and `python3 scripts/download-llama-cpp.py 395`. For the A9 Mega 388 dual-node flagship, download the flagship model on the host, install the same llama.cpp profile on **both** devices with `python3 scripts/download-llama-cpp.py 388-flagship`, and configure the worker address in the recorded launch command. The 388's 64 GB memory cannot host the 111.4 GB model alone.

Model downloads default to `models/`. The flagship directory contains four GGUF shards in `UD-Q4_K_XL/` and the draft model in `MTP/`. Point `-m` and `-md` at those paths when adapting the recorded commands. The script resolves and saves each Hugging Face repository's commit in `download-source.json` on first download, then reuses that commit on retries. Pass `--output /path/to/storage` to use another disk; `--dry-run` previews the selection without network access. `recommended` selects the three recommended models, while `all` also selects every optional model below and needs substantially more disk space.

| Download profile | Hugging Face source | Use |
| --- | --- | --- |
| `flagship` | [Unsloth Qwen3.8 Flash Next `UD-Q4_K_XL`](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF/tree/main/UD-Q4_K_XL) and its MTP file | Recorded 395 and 388 flagship; four shards plus draft |
| `balanced` | [Unsloth Qwen3.6 35B A3B MTP](https://huggingface.co/unsloth/Qwen3.6-35B-A3B-MTP-GGUF/blob/main/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf) | Recorded 22.7 GB 388 recommendation |
| `lightweight` | [OpenBMB MiniCPM5](https://huggingface.co/openbmb/MiniCPM5-2B-GGUF) | Recorded 388 recommendation |
| `deepseek-q2` | [Unsloth DeepSeek V4 Flash `UD-Q2_K_XL`](https://huggingface.co/unsloth/DeepSeek-V4-Flash-0731-GGUF/tree/main/UD-Q2_K_XL) | Hugging Face counterpart to the ModelScope link; three shards |
| `qwen27b-fp4` | [julianmb Qwen3.8 27B ROCmFP4 FAST](https://huggingface.co/julianmb/Qwen-3.8-27B-ROCmFP4-FAST-GGUF) | Recorded 395 FP4 model; its test used the separate `q38rocm` fork |
| `gemma4-q4` | [Google Gemma 4 31B QAT Q4_0](https://huggingface.co/google/gemma-4-31B-it-qat-q4_0-gguf) | Recorded Gemma model and vision projector |
| `flash-q4km` | [DhruvalLabs Qwen3.8 Flash Next `Q4_K_M`](https://huggingface.co/DhruvalLabs/Qwen3.8-Flash-Next-GGUF) | Hugging Face counterpart to the `hf-mirror.com` link in the supplied source list; separate three-shard quantization |

The supplied Qwen3.8 Flash Next `Q4_K_M` link names a different, approximately 119 GB quantization from the repository's measured 111.4 GB `UD-Q4_K_XL` flagship. The `flash-q4km` option does not stand in for the flagship benchmark. The downloader uses Hugging Face directly for the two supplied ModelScope sources and the `hf-mirror.com` source. Current repository commits are saved on download; the benchmark archives do not record model commit hashes, so these downloads cannot establish byte-for-byte identity with the original tests.

The llama.cpp script selects the recorded release: [Unsloth `b10909-mix-bea84f7`](https://github.com/unslothai/llama.cpp/releases/tag/b10909-mix-bea84f7) for 395, [Unsloth `b10830-mix-d5c17a0`](https://github.com/unslothai/llama.cpp/releases/tag/b10830-mix-d5c17a0) for 388 flagship, and [upstream `b11065`](https://github.com/ggml-org/llama.cpp/releases/tag/b11065) for 388 balanced. It selects a Linux ROCm `gfx1151` archive where that release provides one. If a matching binary is absent, it downloads the tagged source and prints the HIP build command. `--list-assets` displays the upstream release assets; `--source` explicitly downloads source. Downloads go to `bin/ubuntu/` by default. These scripts prepare software and files; the device archive commands still need local paths, network addresses, and suitable context settings.
