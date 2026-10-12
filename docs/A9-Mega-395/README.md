# A9 Mega 395 — Local LLM Inference Test Records

This directory archives the local large language model inference performance tests measured on the **GEEKOM A9 Mega 395** configuration.

- Source: tests measured on physical GEEKOM A9 Mega 395 hardware
- Records: **42**, covering **7** model / deployment combinations
- Raw details are also available as [`test-records.csv`](./test-records.csv) in this directory (UTF-8, opens directly in Excel)

> **Recommended model**: this directory is a full test archive. Only `Qwen3.8-Flash-Next-UD-Q4_K_XL` is promoted as a recommendation in Section 5.1 of the root [`README.md`](../../README.md); all other combinations here — the DeepSeek-V4-Flash deployments, `Qwen3.8-27B-FP4-FAST`, and `MiniCPM5-2B-bf16` — are recorded as test data only.

## 1. Device and hardware configuration

| Item | Configuration |
| --- | --- |
| Device model | GEEKOM A9 Mega 395 |
| Processor | AMD Ryzen AI MAX+ 395 |
| Graphics | Radeon 8060S |
| Memory bandwidth | 256 GB/s |
| Memory | 128 GB |
| Operating system | Ubuntu 26.04 |
| Graphics driver | 31.50.0.0 |
| ROCm version | 10.0.0 |


> Note: beyond the processor, graphics, memory bandwidth, memory, operating system, graphics driver, and ROCm version listed above, the remaining hardware details — BIOS, NPU driver, power profile, storage, and the exact llama.cpp build — have not been collected yet and must be added before release.

## 2. Field descriptions

| Field | Meaning |
| --- | --- |
| Input length (tokens) | Context input length used for the test (128 / 8K / 16K / 32K / 64K / 128K / 256K) |
| Output length (tokens) | Number of tokens actually generated |
| Time to first token, TTFT (s) | Time from sending the request to receiving the first token |
| Prefill rate (tokens/s) | Prompt processing (prefill) throughput |
| Decode rate (tokens/s) | Generation (decode) throughput |
| End-to-end time (s) | Total time for a single request |
| VRAM (GB) | Video memory usage; for a dual-node cascade `host / worker`, for a triple-node cascade `host / worker 1 / worker 2` |

## 3. Test results

### 3.1 Qwen3.8-Flash-Next-UD-Q4_K_XL.gguf (111.4GB) mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf (2.8GB)

- Deployment: single device
- Acceleration: `Yes(MTP) N=2`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 5000 | 0.97 | 132.22 | 32.43 | 155.15 | 131.68 |
| 8K | 1604 | 26.96 | 303.83 | 28.48 | 83.28 | 132.58 |
| 16K | 2617 | 58.33 | 280.89 | 25.88 | 159.45 | 132.73 |
| 32K | 2695 | 112.14 | 292.21 | 23.58 | 226.43 | 132.74 |
| 64K | 1965 | 283.41 | 231.24 | 18.06 | 392.22 | 133.68 |
| 128K | 5000 | 720.61 | 181.89 | 15.45 | 1044.24 | 134.06 |

<details>
<summary>Test commands</summary>

```bash
./llama-server -m /home/user/mode/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf -ngl 99 -c 256000 -b 4096 -ub 2048 -fa on -np 1 --host 127.0.0.1 --port 8080 --metrics -lv 4 -md /home/user/mode/Qwen3.8-Flash-Next-UD-Q4_K_XL/mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp --spec-draft-n-max 2
```

</details>

### 3.2 Dual-node cascade Qwen3.8-Flash-Next-UD-Q4_K_XL.gguf (111.4GB) mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf (2.8GB)

- Acceleration: `Yes(MTP) N=2`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 2876 | 0.84 | 151.58 | 34.27 | 84.77 | 101.41/64.86 |
| 8K | 618 | 19.86 | 412.4 | 30.66 | 40.02 | 102.47/64.95 |
| 16K | 5000 | 41.1 | 398.65 | 27.78 | 221.08 | 103.06/64.97 |
| 32K | 971 | 90.73 | 361.15 | 27.9 | 125.54 | 103.70/64.88 |
| 128K | 2150 | 566.14 | 231.52 | 15.16 | 707.96 | 107.35/64.77 |
| 256K | 5000 | 1619.07 | 161.91 | 10.5 | 2095.26 | 114.83/64.95 |

<details>
<summary>Test commands</summary>

```bash
Worker start command: env -u HSA_OVERRIDE_GFX_VERSION ./ggml-rpc-server -H 10.10.10.2 -p 50052 -t 16
Host start command: env -u HSA_OVERRIDE_GFX_VERSION /home/user/app-b10909-mix-bea84f7-linux-x64-rocm-gfx1151.tar./llama-server -m /home/user/mode/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf -ngl 99 -c 256000 -b 4096 -ub 2048 -fa on -np 1 --rpc 10.10.10.2:50052 --host 127.0.0.1 --port 8080 --metrics -lv 4 -md /home/user/mode/Qwen3.8-Flash-Next-UD-Q4_K_XL/mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp --spec-draft-n-max 2
```

</details>

### 3.3 DeepSeek-V4-Flash-0731-UD-Q2_K_XL-GGUF (96.8 GB)

- Deployment: single device
- Acceleration: `No`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 1641 | 0.99 | 129.24 | 14.71 | 112.55 | 112.96 |
| 8K | 368 | 58.14 | 140.9 | 14.65 | 83.26 | 112.86 |
| 32K | 242 | 302.15 | 108.45 | 12.87 | 320.95 | 112.99 |
| 64K | 452 | 741.94 | 88.33 | 11.61 | 780.88 | 113.12 |
| 128K | 1735 | 2098.83 | 62.45 | 9.71 | 2277.51 | 113.14 |
| 256K | 472 | 7237.55 | 36.22 | 7.16 | 7303.47 | 114.12 |

<details>
<summary>Test commands</summary>

```bash
./llama-server --model /home/user/UD-Q2_K_XL/DeepSeek-V4-Flash-0731-UD-Q2_K_XL-00001-of-00003.gguf --ctx-size 256000 --gpu-layers 999 --flash-attn on --threads 16 --host 0.0.0.0 --port 8000 --path /home/user/xiangmu/llama.cpp-master/tools/ui/dist
```

</details>

### 3.4 Dual-node cascade DeepSeek-V4-Flash-0731-UD-Q2_K_XL-GGUF (96.8 GB)

- Acceleration: `No`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 1553 | 0.99 | 129.87 | 14.21 | 110.27 | 60.72/56.98 |
| 8K | 233 | 45.59 | 179.68 | 13.74 | 62.55 | 60.52/56.97 |
| 32K | 2135 | 242.24 | 135.27 | 12.48 | 413.32 | 60.71/56.97 |
| 64K | 419 | 584.57 | 112.11 | 11.06 | 622.45 | 60.73/56.98 |
| 128K | 478 | 1671.41 | 78.42 | 9.09 | 1724 | 61.06/56.98 |
| 256K | 712 | 4940.52 | 53.06 | 7.21 | 5039.27 | 61.59/57.21 |

<details>
<summary>Test commands</summary>

```bash
Host start command: ./llama-server   --model /home/user/UD-Q2_K_XL/DeepSeek-V4-Flash-0731-UD-Q2_K_XL-00001-of-00003.gguf   --ctx-size 256000   --gpu-layers 999   --flash-attn on   --threads 16   --rpc 192.168.10.30:50052  --host 0.0.0.0 --port 8000  --path /home/user/xiangmu/llama.cpp-master/tools/ui/dist
Worker start command: ./ggml-rpc-server -H 0.0.0.0 -p 50052
```

</details>

### 3.5 Triple-node cascade DeepSeek-V4-Flash-0731-UD-Q2_K_XL-GGUF (96.8 GB)

- Acceleration: `No`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 1229 | 1.07 | 119.39 | 13.4 | 92.79 | 47.89/47.70/26.72 |
| 8K | 530 | 51.81 | 158.11 | 12.94 | 92.77 | 47.92/47.62/26.72 |
| 32K | 2481 | 270.27 | 121.24 | 11.75 | 481.42 | 47.88/47.71/26.73 |
| 64K | 417 | 644.09 | 101.75 | 10.37 | 684.3 | 47.94/47.65/26.72 |
| 128K | 873 | 1786.7 | 73.36 | 8.97 | 1884.02 | 48.56/47.65/26.72 |
| 256K | 2265 | 5433.04 | 48.25 | 7.06 | 5753.86 | 48.92/47.65/26.72 |

<details>
<summary>Test commands</summary>

```bash
Host start command: ./llama-server   --model /home/user/UD-Q2_K_XL/DeepSeek-V4-Flash-0731-UD-Q2_K_XL-00001-of-00003.gguf   --ctx-size 256000   --gpu-layers 999   --flash-attn on   --threads 16   --rpc 192.168.10.30:50052,192.168.10.10:50052  --host 0.0.0.0 --port 8000  --path /home/user/xiangmu/llama.cpp-master/tools/ui/dist
Worker start command: ./ggml-rpc-server -H 0.0.0.0 -p 50052
```

</details>

### 3.6 Qwen3.8-27B-FP4-FAST-GGUF

- Acceleration: `Yes(MTP) N=4`
- Records: 7

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 3000 | 0.4 | 318.64 | 31.29 | 96.28 | 26.8 |
| 8K | 2087 | 23.56 | 347.73 | 25.43 | 105.63 | 26.8 |
| 16K | 3000 | 51.11 | 320.57 | 24.51 | 173.51 | 26.9 |
| 32K | 3000 | 118.52 | 276.48 | 20.28 | 266.45 | 26.8 |
| 64K | 3000 | 306.21 | 214.02 | 15.42 | 500.77 | 26.7 |
| 128K | 3000 | 865.62 | 151.42 | 8.95 | 1200.81 | 26.7 |
| 256K | 392 | 2775.48 | 94.45 | 6.06 | 2840.17 | 26.8 |

<details>
<summary>Test commands</summary>

```bash
./llama-server -m /home/user/workspace/Qwen3.8-27B-ROCmFP4-FAST.gguf -dev ROCm0 -ngl 99 -fa on -c 256000 -b 2048 -ub 1024 -t 16 -ctk q8_0 -ctv q8_0 --temperature 0 --no-mmap --cont-batching --kv-unified --port 8000 --host 0.0.0.0 --spec-type draft-mtp --spec-draft-n-max 4 --spec-draft-p-min 0.0
```

</details>

### 3.7 MiniCPM5-2B-bf16-GGUF

- Acceleration: `No`
- Records: 5

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 923 | 0.17 | 731.97 | 33.05 | 28.1 | 8.7 |
| 8K | 1258 | 10.89 | 752.38 | 31.52 | 50.8 | 8.7 |
| 16K | 966 | 25.59 | 640.34 | 30.48 | 57.28 | 8.7 |
| 32K | 779 | 68.53 | 478.15 | 28.26 | 96.1 | 8.7 |
| 128K | 1163 | 878.03 | 149.28 | 20.49 | 934.79 | 8.7 |

<details>
<summary>Test commands</summary>

```bash
llama-server.exe  -m  D:\model\MiniCPM5-2B-bf16.gguf -c 131072 -ngl 99 -ngld 99 -t 12 -np 1 --cont-batching --flash-attn on --host 0.0.0.0 --port 8082 --metrics -lv  3 --cache-type-k q8_0 --cache-type-v q8_0 --fit off
```

</details>

## 4. Coverage overview

| Model / deployment | Acceleration | Context lengths tested | Missing context lengths |
| --- | --- | --- | --- |
| Qwen3.8-Flash-Next-UD-Q4_K_XL (single device) | MTP N=2 | 128 / 8K / 16K / 32K / 64K / 128K | 256K |
| Dual-node cascade Qwen3.8-Flash-Next-UD-Q4_K_XL | MTP N=2 | 128 / 8K / 16K / 32K / 128K / 256K | 64K |
| DeepSeek-V4-Flash-0731-UD-Q2_K_XL (single device) | No | 128 / 8K / 32K / 64K / 128K / 256K | 16K |
| Dual-node cascade DeepSeek-V4-Flash-0731-UD-Q2_K_XL | No | 128 / 8K / 32K / 64K / 128K / 256K | 16K |
| Triple-node cascade DeepSeek-V4-Flash-0731-UD-Q2_K_XL | No | 128 / 8K / 32K / 64K / 128K / 256K | 16K |
| Qwen3.8-27B-FP4-FAST | MTP N=4 | 128 / 8K / 16K / 32K / 64K / 128K / 256K | None |
| MiniCPM5-2B-bf16 | No | 128 / 8K / 16K / 32K / 128K | 64K, 256K |

## 5. Data notes and known issues

1. **VRAM format normalized**: in the original records the 395 data is written as "host: x / worker: y" with mixed full-width and half-width colons; this directory normalizes it to `x/y`, and to `host / worker 1 / worker 2` for triple-node cascades. Only the written format was adjusted; no value was changed.
2. **Typo corrected**: the decode rate in the 32K row of MiniCPM5-2B-bf16 was previously recorded as "28，26" (full-width comma); the original record has since been corrected to `28.26` tokens/s, and this directory matches at `28.26`.
3. **DeepSeek-V4-Flash is missing 16K in every deployment**: the single-device, dual-node cascade, and triple-node cascade tests only covered 128 / 8K / 32K / 64K / 128K / 256K, so 16K is missing. Keep this in mind for cross-deployment comparison.
4. **Speedup metrics**: the original records also carried "speedup xx%" values (the improvement of MTP acceleration over the unaccelerated baseline) and "draft acceptance" rates. Both are supporting indicators of the acceleration effect rather than throughput metrics, and because the source notes are not republished they are not included in this directory.
5. **Model context limit**: the original note for MiniCPM5-2B-bf16 reads "context length set to 128k; the model supports up to 128k only", which is why 256K was not tested.
6. **Device attribution resolved**: a data set was previously labelled "A9-Mega-388 inference performance data"; its six rows match Section 3.2 of this directory (395, dual-node cascade, Qwen3.8-Flash-Next). The root [`README.md`](../../README.md) now attributes that data set to the 395.
7. **Single-device flagship VRAM reading**: the single-device Qwen3.8-Flash-Next rows report 131.68 to 134.06 GB of VRAM, above the 128 GB memory size listed in Section 1; the values are recorded as measured and the basis for that column has not been confirmed.
8. **To be completed before release**: these records have not been reproduced through two independent clean QA installations, and several hardware details (BIOS, NPU driver, power profile, storage) have not been collected. Do not publish as is.

## 6. Related files

| File | Description |
| --- | --- |
| [`test-records.csv`](./test-records.csv) | Flat data table of all 42 records for the 395 |
| `../A9-Mega-388/README.md` | Test records for the 388 configuration (same structure, for comparison) |
| `../../README.md` | Quantization level selection (bits vs. size / accuracy) and the 4-bit measurements per device |
| `../qa-handoff-template.md` | QA handoff template for installation and functional verification records |
