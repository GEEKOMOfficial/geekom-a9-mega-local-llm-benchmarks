# DeepSeek-V4-Flash on the DwarfStar (ds4) engine — A9 Mega 395

This page records the **DeepSeek-V4-Flash** test data measured on the A9 Mega 395 using the **DwarfStar** inference engine (repository name **ds4**). The full measurements are reproduced in Section 3 below. This page is a companion to the main [`README.md`](./README.md) in this directory, which archives the same class of models under `llama.cpp`.

- Engine: **DwarfStar / ds4** — https://github.com/antirez/ds4
- Deployment: two-node pipeline (coordinator + worker) over ROCm
- Records: **5** (8K / 16K / 32K / 64K / 128K input tokens)

> **Scope note**: the DwarfStar engine uses its own model files and its own runtime; it is **not** a drop-in replacement for the `llama.cpp` records in [`test-records.csv`](./test-records.csv). The DeepSeek figures on this page come from a different engine, a different model file, and a different deployment than the DeepSeek rows in [`./README.md`](./README.md) §3.3–3.5. Read Section 4 before comparing them.

## 1. About the DwarfStar (ds4) engine

[DwarfStar](https://github.com/antirez/ds4) (`ds4`) is a self-contained local inference engine by Salvatore Sanfilippo (`antirez`, the author of Redis), released under the **MIT** license. Its distinguishing traits:

- **Purpose-built, not general-purpose**: it targets a small, deliberately chosen set of models rather than acting as a universal GGUF runner. It works only with GGUFs produced by the project itself.
- **DeepSeek-first**: DeepSeek V4 Flash / V4.1 Flash / V4 PRO are the primary optimization targets (GLM 5.x and Qwen3.8 Flash Next are also supported). This DeepSeek focus is exactly why it can be tuned for **much faster prompt processing (prefill)** and **lower end-to-end latency** than a general runner on the same hardware.
- **Backends**: Apple Silicon (Metal), NVIDIA CUDA (DGX Spark and multi-GPU), and **ROCm for Strix Halo-class systems** — the backend used for the A9 Mega tests below.
- **Multi-node**: pipeline parallelism (`--role coordinator` / `--role worker` with a layer split) lets several machines pool their memory to run a model larger than any single node, which is the mode used here.
- **Status**: the project describes itself as a fast-moving beta. Behavior and performance can change between releases.

The engine is an alternative to the `llama.cpp` / `ggml-rpc-server` stack documented in [`./README.md`](./README.md) §3.3–3.5. Where those DeepSeek runs used `llama.cpp`, the runs on this page used `ds4` / `ds4-server`.

## 2. Test configuration

| Item | Configuration |
| --- | --- |
| Model | `DeepSeek-V4-Flash-IQ2.gguf` (86.7 GB, **IQ2** quantization) |
| Engine | DwarfStar `ds4` / `ds4-server` (ROCm backend) |
| Deployment | Two-node pipeline — coordinator: layers `0:20`; worker: layers `21:output` |
| Context | `--ctx 256000`, measured through 128K input tokens |
| Memory reporting | Recorded per node as `host / worker` (GB) |

**How to read this against the `llama.cpp` DeepSeek record.** The DeepSeek rows in [`./README.md`](./README.md) use `llama.cpp` with **`DeepSeek-V4-Flash-0731-UD-Q2_K_XL` (96.8 GB)**. This page uses the DwarfStar engine with **`DeepSeek-V4-Flash-IQ2` (86.7 GB)**. The engine, the quantization scheme, the file size, and the multi-node mechanism all differ, so the two are not the same test repeated on a different runner.

## 3. Measured results

Values are reproduced exactly as recorded; this page is the published record for these measurements.

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | Memory host / worker (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 8K | 78 | 21.55 | 380.14 | 13.44 | 28.37 | 62.87 / 60.90 |
| 16K | 85 | 40.89 | 400.23 | 13.25 | 49.34 | 62.93 / 60.96 |
| 32K | 78 | 73.60 | 442.40 | 12.72 | 81.75 | 63.24 / 61.31 |
| 64K | 135 | 153.53 | 422.75 | 11.62 | 166.97 | 63.44 / 61.74 |
| 128K | 87 | 351.66 | 368.44 | 10.10 | 363.16 | 63.48 / 61.53 |

<details>
<summary>Test commands (as recorded)</summary>

```bash
# Worker
./ds4 --rocm -m DeepSeek-V4-Flash-IQ2.gguf --role worker --layers 21:output --coordinator 10.10.10.1 9911 --ctx 256000

# Coordinator / host
./ds4-server --rocm -m /home/user/mode/DeepSeek-V4-Flash-IQ2/DeepSeek-V4-Flash-IQ2.gguf --role coordinator --layers 0:20 --listen 10.10.10.1 9911 --ctx 256000
```

</details>

The two commands start a **two-node pipeline**: the coordinator hosts the first 21 layers (`0:20`) and the worker hosts the remainder (`21:output`), connected over the network at port `9911`. Both nodes report roughly 61–63 GB of memory in use, and prefill throughput stays remarkably flat (368–442 tokens/s) across the whole 8K–128K range.

## 4. Prefill and latency improvement vs the `llama.cpp` record

The clearest signal in the data is **prompt-processing (prefill) speed**. The table below compares the DwarfStar numbers with the `llama.cpp` **dual-node cascade** DeepSeek record from [`./README.md`](./README.md) §3.4 — the closest like-for-like deployment (two nodes, same context lengths). Prefill rate and time-to-first-token are directly comparable metrics; both are governed by the engine's prompt-processing path.

| Context | DwarfStar prefill (tokens/s) | `llama.cpp` dual-node prefill (tokens/s) | Prefill speed-up | DwarfStar TTFT (s) | `llama.cpp` dual-node TTFT (s) |
| --- | ---: | ---: | :---: | ---: | ---: |
| 8K | 380.14 | 179.68 | ≈ 2.1× | 21.55 | 45.59 |
| 16K | 400.23 | *not tested* | — | 40.89 | *not tested* |
| 32K | 442.40 | 135.27 | ≈ 3.3× | 73.60 | 242.24 |
| 64K | 422.75 | 112.11 | ≈ 3.8× | 153.53 | 584.57 |
| 128K | 368.44 | 78.42 | ≈ 4.7× | 351.66 | 1671.41 |

**What this shows:**

- **Prefill is roughly 2×–4.7× faster**, and the advantage grows with context length: the `llama.cpp` prefill rate degrades under long prompts (179 → 78 tokens/s), while DwarfStar holds steady at 368–442 tokens/s.
- **Time to first token drops by the same factor.** At 128K input tokens, DwarfStar returns the first token in **351.66 s** versus **1671.41 s** in the `llama.cpp` record — about **4.8× lower latency**.
- **End-to-end delay follows the prefill gain.** For long-context requests the prompt-processing time dominates end-to-end latency, so the ~2×–4.7× reduction in TTFT translates directly into a large cut in wall-clock delay on long inputs. (Direct end-to-end totals cannot be compared between the two record sets — see the caveats below.)
- **Decode throughput is broadly similar**, not worse: 13.44 vs 14.21 tokens/s at 8K and 10.10 vs 9.09 tokens/s at 128K. The standout improvement is prefill, not generation.

<details>
<summary>Why the two record sets cannot be compared on end-to-end totals alone</summary>

The `ds4` rows were recorded with very short generations (output length 78–135 tokens), whereas the `llama.cpp` DeepSeek rows generated 233–2135 tokens per request. End-to-end time is dominated by generation whenever the output is long, so the raw totals in the two record sets are not on equal footing. Comparing **prefill rate** and **TTFT** — which depend on the input prompt, not the output length — is the meaningful comparison, and that is where the DwarfStar advantage appears.

</details>

## 5. Reading the results

- **DwarfStar is markedly faster at prompt processing on this hardware.** Across 8K–128K input tokens it sustains 368–442 tokens/s of prefill, versus 78–180 tokens/s for the `llama.cpp` dual-node record — a 2×–4.7× improvement that keeps growing as the prompt gets longer.
- **The DeepSeek focus pays off.** Because `ds4` is specialized for DeepSeek models rather than being a general runner, it makes large gains exactly in the workload that matters for a long-context assistant: getting the first token back quickly.
- **Generation speed is comparable.** Decode rates are within a few percent of the `llama.cpp` figures, so the improvement is concentrated in prefill/TTFT rather than in token streaming.

## 6. Related files

| File | Description |
| --- | --- |
| [`./README.md`](./README.md) | A9 Mega 395 test archive — the `llama.cpp` records, including the DeepSeek-V4-Flash deployments |
| [`test-records.csv`](./test-records.csv) | Flat data table of all 42 `llama.cpp` records for the 395 |
| [`../../README.md`](../../README.md) | Quantization level selection and the measured performance by device |
| https://github.com/antirez/ds4 | DwarfStar (`ds4`) project home (MIT) |
