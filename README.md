# Local LLM Inference on GEEKOM A9 Mega

This repository answers three questions for end customers, using data measured on physical GEEKOM hardware:

1. When running a large language model locally on a mini PC, **which quantization level should you choose?**
2. Once that level is chosen, **what performance can each GEEKOM A9 Mega model — the A9 Mega 388 (64 GB) and the A9 Mega 395 (128 GB) — actually deliver?**
3. **Which model should you pick for each device?**

The short answer: **4-bit quantization is the sweet spot between file size and accuracy**, and it is the level used for the recommended configurations in this repository.

Section 5 turns those results into a concrete shortlist: the **strongest model for the A9 Mega 395** and **three recommended models for the A9 Mega 388**. Because the 395 has twice the memory (128 GB vs. 64 GB), **every model the 388 can run also runs on the 395**.

All performance data was measured on physical GEEKOM units. **The device configuration, exact model versions, and launch commands are published together with the results**, and anything not tested is marked "Not tested".

Full records for each device, including test commands, VRAM usage, and notes:

- A9 Mega 388 — all 36 test records: [`docs/A9-Mega-388/`](./docs/A9-Mega-388/)
- A9 Mega 395 — all 42 test records: [`docs/A9-Mega-395/`](./docs/A9-Mega-395/)

> **Release status**: the results have not yet been reproduced by two independent clean QA installations, and hardware details (operating system, BIOS, driver, power profile) are still being collected. These will be completed before release.

## Contents

1. [Quantization bits vs. model file size](#1-quantization-bits-vs-model-file-size)
2. [Quantization bits vs. model accuracy](#2-quantization-bits-vs-model-accuracy)
3. [Conclusion: 4-bit is the sweet spot](#3-conclusion-4-bit-is-the-sweet-spot)
4. [Measured 4-bit performance by device](#4-measured-4-bit-performance-by-device)
5. [Recommended models by device](#5-recommended-models-by-device)

---

## 1. Quantization bits vs. model file size

Quantization means **representing a single weight with fewer bits** (often written as *bits per weight*, or **bpw**). Using this repository's primary model, **Qwen3.8-Flash-Next**, as the example:

| Quantization level | 1-bit | 2-bit | 3-bit | 4-bit | 5-bit | 8-bit | BF16 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Typical GGUF quantization | `IQ1_S` / `IQ1_M` | `Q2_K_XL` | `IQ3_XXS` / `Q3_K_XL` | `IQ4_XS` / `Q4_K_XL` | `Q5_K_XL` | `Q8_0` | BF16 |
| Model size (disk ≈ weight memory at runtime, excluding cache) | 75 GB | 79 GB | 90 GB | 96–114 GB | 163 GB | 200 GB | 355 GB |

Three points follow from this table:

- **Size grows monotonically with quantization bits**: the more bits used per weight, the larger the model file, and the more video memory / system memory it occupies at runtime.
- **Size grows gently at low quantization bits**: 1-bit to 4-bit only moves from 75 GB to 96–114 GB (roughly +30% to +50%), yet that is already enough to hold this hundred-gigabyte-class flagship model.
- **Size expands sharply at high quantization bits**: BF16 (355 GB) is more than three times the size of 4-bit, and 8-bit (200 GB) is likewise far beyond the memory capacity of a mainstream mini PC. Both place an order-of-magnitude higher demand on memory capacity and memory bandwidth.

**What this means when choosing a device**: quantization bits are not "the higher the better", they are "high enough is enough". Whether a given machine can run the model at all is decided mainly by whether its memory capacity can hold the corresponding file size, plus the runtime overhead carried on top of it — above all the context cache (KV cache), which grows with context length. In the 395 dual-node test in Section 4.2, the 111.4 GB 4-bit flagship occupies 101.41 GB at 128 tokens but 114.83 GB at 256K. Memory capacity therefore decides both the model size a device can carry and the context length it can serve.

## 2. Quantization bits vs. model accuracy

Both charts below come from Unsloth's evaluation of the Qwen3.8-Flash GGUF quantizations. The horizontal axis is disk space (GB) throughout. Because disk space maps one-to-one onto quantization level for a given model, **it can be read directly as quantization bits**.

### Top-1 accuracy

![Qwen3.8-Flash GGUF Model Top-1 Accuracy](docs/images/top-1-accuracy-gguf-model.png)

- The vertical axis is Top-1 accuracy (%). Accuracy improves as quantization bits rise, but the curve flattens progressively.
- Very low quantization bits lose a great deal: `IQ1_S-STUB` (about 72 GB) reaches only about 77%, and `IQ1_M` (about 73 GB) about 80%.
- There is still a large gain from `IQ3_XXS` (about 85%) to `Q4_K_XL` (about 92%), which places the 3–4 bit range at the value inflection point.
- Beyond `Q4_K_XL` (about 103 GB) the curve flattens: `Q5_K_XL`, `Q6_K_XL`, `Q8_0` and larger sizes add only about 1%–2%, converging at about 94%.

### KL divergence (KLD)

![Qwen3.8-Flash GGUF Model KLD](docs/images/kld-gguf-model.png)

- The vertical axis is mean KLD (Kullback-Leibler divergence) — the distribution gap against the full-precision model; **lower is better**.
- The curve falls monotonically as quantization bits rise and shows the same saturation:
  - `IQ1_S-STUB` is about 0.40 and `IQ1_M` about 0.31 — extremely low quantization bits differ substantially from the original model.
  - `Q2_K_XL` about 0.23, `IQ3_XXS` about 0.16, `Q3_K_XL` about 0.11, `IQ4_XS` about 0.08.
  - After `Q4_K_XL` (about 103 GB) it drops below 0.05; `Q5_K_XL` and higher quantization bits settle at around 0.03.

## 3. Conclusion: 4-bit is the sweet spot

Reading the file-size results (Section 1) and the accuracy results (Section 2) together:

1. **Size and accuracy are positively correlated**: higher quantization bits give higher Top-1 and lower KLD, and the two charts corroborate each other.
2. **Marginal returns diminish**: beyond roughly 100 GB (`Q4_K_XL`) the improvement is very small. Compared with 4-bit, 5-bit / 8-bit / BF16 are close to double or even triple the size for only about 1%–2% more Top-1 and a KLD improvement from about 0.05 to about 0.03 — a cost far out of proportion to the gain.
3. **Low-bit quantization costs a lot**: 1–2 bit is only slightly smaller than 3-bit, yet Top-1 is 5–10 percentage points lower and KLD is several times higher — capacity saved, model ruined.
4. **At the same file size, the quantization scheme matters**: `IQ1_S`, `IQ1_M`, `Q2_K_XL` and `IQ3_XXS` are all around 72–75 GB, yet accuracy spreads from 77% to 85% and KLD falls from 0.40 to 0.16.

> **4-bit quantization such as `Q4_K_XL` is therefore the sweet spot**: it delivers near-saturated accuracy (Top-1 about 92%, KLD below 0.05) at 96–114 GB, a size that mainstream high-memory machines can carry.
>
> This is why the recommended device configurations in this repository **use 4-bit quantization**. A small number of non-4-bit runs (for example the 2-bit `DeepSeek-V4-Flash-0731-UD-Q2_K_XL`) are kept only as test records; see the scope note in Section 4.4.

## 4. Measured 4-bit performance by device

### 4.1 Devices and hardware configuration

| Item | A9 Mega 388 | A9 Mega 395 |
| --- | --- | --- |
| Processor | AMD Ryzen AI MAX+ 388 | AMD Ryzen AI MAX+ 395 |
| Graphics | Radeon 8060S | Radeon 8060S |
| Memory bandwidth | 256 GB/s | 256 GB/s |
| Memory size | 64 GB | 128 GB |
| Operating system | Ubuntu 26.04 | Ubuntu 26.04 |
| Graphics driver | 31.50.0.0 | 31.50.0.0 |


> Both devices use the same graphics processor and the same memory bandwidth. **The main difference is memory capacity (64 GB vs. 128 GB)**, which directly determines the model sizes a single device can hold and the context lengths it can serve.

### 4.2 Primary model: Qwen3.8-Flash-Next UD-Q4_K_XL

Shared test conditions:

| Item | Configuration |
| --- | --- |
| Model | `Qwen3.8-Flash-Next-UD-Q4_K_XL.gguf` (111.4 GB, the upper end of the 4-bit range in Section 1) + draft model `mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf` (2.8 GB) |
| Acceleration | `Yes(MTP)`, `--spec-type draft-mtp --spec-draft-n-max 2` |
| Context length | `-c 256000`, `-fa on` |
| Deployment | Dual-node cascade (llama.cpp `ggml-rpc-server` with `--rpc`) |

> **Disclosed difference**: the 388 test used `-b 2048 -ub 1024`, while the 395 test used `-b 4096 -ub 2048`; the llama.cpp builds used may also differ. **The prefill rate and time-to-first-token columns in the table below should be read with that difference in mind.** Decode rate is the more directly comparable metric.

| Input length | 388 TTFT (s) | 388 decode (tokens/s) | 388 VRAM (GB) | 395 TTFT (s) | 395 decode (tokens/s) | 395 VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 0.67 | 30.76 | 62.4/57.5 | 0.84 | 34.27 | 101.41/64.86 |
| 8K | 27.36 | 26.14 | 63.8/57.7 | 19.86 | 30.66 | 102.47/64.95 |
| 16K | 55.33 | 25.62 | 63.7/57.8 | 41.1 | 27.78 | 103.06/64.97 |
| 32K | 129.85 | 23.68 | 64.7/57.8 | 90.73 | 27.9 | 103.70/64.88 |
| 128K | 858.93 | 10.62 | 65.7/58.05 | 566.14 | 15.16 | 107.35/64.77 |
| 256K | Not tested | Not tested | Not tested | 1619.07 | 10.5 | 114.83/64.95 |

VRAM is recorded as "host / worker".

**Reading the results**:

- Both devices can run the 111.4 GB flagship 4-bit model through a dual-node cascade, and the **395 (128 GB) also runs it on a single device** (see the [395 archive](./docs/A9-Mega-395/)) — the direct benefit of 4-bit being the sweet spot.
- On a **single 395**, the same flagship model ran at 128 tokens with TTFT 0.97 s and decode 32.43 tokens/s, and at 128K with TTFT 720.61 s and decode 15.45 tokens/s. Its VRAM column is reported at 131.68 to 134.06 GB, above the 128 GB memory size, so read those rows with that in mind.
- The A9 Mega 395 (128 GB memory) runs the full 256K context, decoding **10.5 tokens/s at 256K** and 15.16 tokens/s at 128K. The 388 was tested up to 128K (10.62 tokens/s); its 256K run was not tested.
- As context grows, decode rate falls clearly and time to first token rises sharply on both devices. This is inherent to long-context inference, not a defect of either device.

### 4.3 Other 4-bit models on the A9 Mega 388 (decode rate, tokens/s)

| Model | Size | Acceleration | 128 | 8K | 16K | 32K | 64K | 128K | 256K |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8-27B-UD-Q4_K_XL | Not recorded | MTP N=4 | 20.24 | 21.30 | 19.53 | 16.87 | 12.86 | 9.88 | 6.06 |
| Qwen3.6-35B-A3B-UD-Q4_K_M | 22.7 GB | MTP N=2 | 68.03 | 67.76 | 63.55 | 54.30 | 50.30 | 32.61 | 21.66 |
| MiniCPM5-2B-Q4_K_M | 1.56 GB | No | 103.10 | 87.08 | 75.15 | 61.74 | 44.76 | 29.03 | Not tested |

Corresponding time to first token (s):

| Model | 128 | 8K | 16K | 32K | 64K | 128K | 256K |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8-27B-UD-Q4_K_XL | 0.44 | 24.54 | 52.44 | 109.55 | 268.94 | 646.85 | 1780.14 |
| Qwen3.6-35B-A3B-UD-Q4_K_M | 0.16 | 6.61 | 14.79 | 32.51 | 103.58 | 218.14 | 645.04 |
| MiniCPM5-2B-Q4_K_M | 0.10 | 3.09 | 7.52 | 21.14 | 70.63 | 255.42 | Not tested |

**Reading the results**:

- **MoE models around 35B-A3B are the 388's comfort zone**: `Qwen3.6-35B-A3B-UD-Q4_K_M` (22.7 GB) still decodes at 54.3 tokens/s at 32K and 32.61 tokens/s at 128K.
- 27B-class dense models drop to 5–10 tokens/s at long context, so they suit medium context lengths.
- 2B-class small models (`MiniCPM5-2B-Q4_K_M`, a 1.56 GB file using roughly 15–18 GB of VRAM) reach the hundreds-of-tokens-per-second range, suited to lightweight assistant workloads.

> **Scope note**: Sections 4.2–4.3 record **every** 4-bit model tested on the 388, as test data. Only the three 388 models listed in **Section 5.2** are promoted to the recommendation shortlist; everything else here — for example `Qwen3.8-27B-UD-Q4_K_XL`, plus the triple-node cascade deployment of `Qwen3.8-Flash-Next-UD-Q4_K_XL` — is kept as a measured record only. Full records are in [`docs/A9-Mega-388/`](./docs/A9-Mega-388/).

### 4.4 Other 4-bit models on the A9 Mega 395 (decode rate, tokens/s)

| Model | Acceleration | 128 | 8K | 16K | 32K | 64K | 128K | 256K |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8-27B-FP4-FAST | MTP N=4 | 31.29 | 25.43 | 24.51 | 20.28 | 15.42 | 8.95 | 6.06 |

Corresponding time to first token (s):

| Model | 128 | 8K | 16K | 32K | 64K | 128K | 256K |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8-27B-FP4-FAST | 0.40 | 23.56 | 51.11 | 118.52 | 306.21 | 865.62 | 2775.48 |

> **Scope note**: the 395 was also tested with the **2-bit** `DeepSeek-V4-Flash-0731-UD-Q2_K_XL` (96.8 GB, in single-node, dual-node cascade, and triple-node cascade deployments) and with `MiniCPM5-2B-bf16`; neither is 4-bit, so they are not listed in this section. Within the 4-bit results, only `Qwen3.8-Flash-Next-UD-Q4_K_XL` — the model recommended in **Section 5.1** — is promoted to the recommendation shortlist, while `Qwen3.8-27B-FP4-FAST` is kept as a measured record only. Full records are in [`docs/A9-Mega-395/`](./docs/A9-Mega-395/).

### 4.5 Reproduction commands

<details>
<summary>388 — dual-node cascade, Qwen3.8-Flash-Next UD-Q4_K_XL</summary>

```bash
Worker: LD_LIBRARY_PATH="$PWD:$PWD/lib:$PWD/bin:$LD_LIBRARY_PATH" && env -u HSA_OVERRIDE_GFX_VERSION ./ggml-rpc-server -H 192.168.10.10 -p 50052 -t 16
Host: env -u HSA_OVERRIDE_GFX_VERSION ./llama-server -m /home/user/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf -ngl 99 -c 256000 -b 2048 -ub 1024 -fa on -np 1 --rpc 192.168.10.10:50052 --host 127.0.0.1 --port 8080 --metrics -lv 4 -md /home/user/Qwen3.8-Flash-Next-UD-Q4_K_XL/mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp --spec-draft-n-max 2
```

</details>

<details>
<summary>395 — dual-node cascade, Qwen3.8-Flash-Next UD-Q4_K_XL</summary>

```bash
Worker start command: env -u HSA_OVERRIDE_GFX_VERSION ./ggml-rpc-server -H 10.10.10.2 -p 50052 -t 16
Host start command: env -u HSA_OVERRIDE_GFX_VERSION /home/user/app-b10909-mix-bea84f7-linux-x64-rocm-gfx1151.tar./llama-server -m /home/user/mode/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf -ngl 99 -c 256000 -b 4096 -ub 2048 -fa on -np 1 --rpc 10.10.10.2:50052 --host 127.0.0.1 --port 8080 --metrics -lv 4 -md /home/user/mode/Qwen3.8-Flash-Next-UD-Q4_K_XL/mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp --spec-draft-n-max 2
```

</details>

The complete test command for every model is in the corresponding device archive.

---

## 5. Recommended models by device

The 4-bit results in Section 4 reduce to a short, device-specific shortlist. **Every model the A9 Mega 388 (64 GB) can run also runs on the A9 Mega 395 (128 GB)**; the reverse is not true, because the 395's larger memory can hold models the 388 cannot carry on its own.

### 5.1 A9 Mega 395 — strongest recommended model

| Role | Model | File size | Deployment |
| --- | --- | --- | --- |
| Strongest model | `Qwen3.8-Flash-Next-UD-Q4_K_XL.gguf` | 111.4 GB | Single device, or dual-node cascade |

The 395 runs this hundred-gigabyte-class 4-bit flagship **on a single device** — no cascade required — because its 128 GB memory can hold it (Section 4.2). On that single device it decoded at 32.43 tokens/s at 128 tokens and 15.45 tokens/s at 128K. The 395 also runs every model recommended for the 388 below.

### 5.2 A9 Mega 388 — three recommended models

| # | Role | Model | File size | Deployment | Why |
| --- | --- | --- | --- | --- | --- |
| 1 | Flagship (needs a second device) | `Qwen3.8-Flash-Next-UD-Q4_K_XL.gguf` | 111.4 GB | Dual-node cascade with a second A9 Mega | The 64 GB 388 cannot hold this model alone; in a two-node cascade it decoded at 30.76 tokens/s at 128 tokens (Section 4.2). |
| 2 | Balanced everyday default | `Qwen3.6-35B-A3B-UD-Q4_K_M-GGUF` | 22.7 GB | Single device | MoE 35B-A3B; 54.3 tokens/s at 32K and 32.61 tokens/s at 128K, with 256K measured working (Section 4.3). |
| 3 | Lightweight, high-throughput | `MiniCPM5-2B-Q4_K_M.GGUF` | 1.56 GB | Single device | 2B-class small model reaching hundreds of tokens per second at short context (Section 4.3). |

> **Compatibility note**: all three 388 recommendations — the dual-node flagship (1) and the two single-device models (2 and 3) — also run on the A9 Mega 395.

**In short**: pick the **A9 Mega 395** (128 GB) when you need the 111.4 GB flagship on a single device or the full 256K context; pick the **A9 Mega 388** (64 GB) for an everyday high-throughput assistant — its 35B-A3B model still decodes at 54.3 tokens/s at 32K — and add a second A9 Mega to reach the same flagship through a dual-node cascade.

> These conclusions apply only to the configurations recorded in this repository. Changing software versions, models, context length, or power profile may change the results, and data from a single device should not be generalized into guaranteed performance across all GEEKOM configurations.

## Known limitations

Only limitations actually observed in the tests recorded here are listed; anything not tested is marked as such rather than assumed.

| Item | Observed limitation |
| --- | --- |
| Maximum tested context | 256K (`-c 256000`) was measured working on the **A9 Mega 395** (dual-node cascade) and, on the **388**, for the single-device `Qwen3.8-27B-UD-Q4_K_XL` and `Qwen3.6-35B-A3B-UD-Q4_K_M`. For the flagship Qwen3.8-Flash-Next, 256K was tested only on the 395 dual-node cascade; the 388 dual-node and the 395 single-device runs stopped at 128K. |
| Memory capacity | The **388 (64 GB) cannot hold the 111.4 GB 4-bit flagship model on a single device**, so the 388 requires a **dual-node cascade**. The **395 (128 GB)** ran it on a single device as measured. Single-device models are otherwise limited to what 64 GB (388) or 128 GB (395) can hold. |
| Long-context throughput | Decode rate falls and time to first token rises sharply as context grows on both devices. |
| Test conditions not yet published | BIOS, NPU driver, power profile, and the exact llama.cpp build are still "To be confirmed". |
| Reproduction | The results have not yet been reproduced by two independent clean QA installations. |
| Offline use | Local operation does not mean every step works offline: models, software, dependencies, and required resources must be downloaded and configured before the device is disconnected from the internet. |

## Responsible use

This is an experimental reference project, not a guarantee that every model or third-party application will work on every configuration. Model outputs may be inaccurate. Do not use generated output as the sole basis for medical, legal, financial, safety-critical, or other high-impact decisions.

The performance data here was measured on specific, disclosed configurations. Background applications, software versions, model settings, ambient conditions, and power profiles can affect performance, so results from one device should not be read as guaranteed performance for every GEEKOM configuration.

Support scope and issue-response expectations will be added before public release.

## Related resources

- [GEEKOM Resource Center](https://github.com/GEEKOMOfficial/geekom-resource-center)
- [GEEKOM Official Website](https://www.geekompc.com/)
- [GEEKOM Support](https://www.geekompc.com/support/)
