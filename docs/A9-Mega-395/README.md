# A9 Mega 395 — Local LLM Inference Test Records

This directory archives the local large language model inference performance tests measured on the **GEEKOM A9 Mega 395** configuration.

- Source: tests measured on physical GEEKOM A9 Mega 395 hardware
- Records: **35**, covering **6** model / deployment combinations
- Raw details are also available as [`test-records.csv`](./test-records.csv) in this directory (UTF-8, opens directly in Excel)

## 1. Device and hardware configuration

| Item | Configuration |
| --- | --- |
| Device model | GEEKOM A9 Mega 395 |
| Processor | AMD Ryzen AI MAX+ 395 |
| Graphics | Radeon 8060S |
| Memory bandwidth | 256 GB/s |
| Memory | 128 GB |
| Operating system | Ubuntu 26.04 |
| ROCm version | 10.0.0 |


> Note: the original records contain only the processor, graphics, memory bandwidth, and memory configuration. The remaining hardware details have not been collected yet and must be added before release.

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

### 3.1 Dual-node cascade Qwen3.8-Flash-Next-UD-Q4_K_XL.gguf (111.4GB) mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf (2.8GB)

- Acceleration: `Yes(MTP) N=2`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 2876 | 1.19 | 151.58 | 34.27 | 85.11 | 101.41/64.86 |
| 8K | 618 | 20.01 | 412.4 | 30.66 | 40.17 | 102.47/64.95 |
| 16K | 5000 | 41.26 | 398.65 | 27.78 | 221.25 | 103.06/64.97 |
| 32K | 971 | 90.93 | 361.15 | 27.9 | 125.73 | 103.70/64.88 |
| 128K | 2150 | 566.5 | 231.52 | 15.16 | 708.32 | 107.35/64.77 |
| 256K | 5000 | 1544.66 | 161.91 | 10.5 | 2020.85 | 114.83/64.95 |

<details>
<summary>Test commands</summary>

```bash
Worker start command: env -u HSA_OVERRIDE_GFX_VERSION ./ggml-rpc-server -H 10.10.10.2 -p 50052 -t 16
Host start command: env -u HSA_OVERRIDE_GFX_VERSION /home/user/app-b10909-mix-bea84f7-linux-x64-rocm-gfx1151.tar./llama-server -m /home/user/mode/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf -ngl 99 -c 256000 -b 4096 -ub 2048 -fa on -np 1 --rpc 10.10.10.2:50052 --host 127.0.0.1 --port 8080 --metrics -lv 4 -md /home/user/mode/Qwen3.8-Flash-Next-UD-Q4_K_XL/mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp --spec-draft-n-max 2
```

</details>

### 3.2 DeepSeek-V4-Flash-0731-UD-Q2_K_XL-GGUF (96.8 GB)

- Deployment: single device
- Acceleration: `No`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 1641 | 3.49 | 129.24 | 14.71 | 115.05 | 112.96 |
| 8K | 368 | 61.54 | 140.9 | 14.65 | 86.66 | 112.86 |
| 32K | 242 | 299.91 | 108.45 | 12.87 | 318.71 | 112.99 |
| 64K | 452 | 743.7 | 88.33 | 11.61 | 782.63 | 113.12 |
| 128K | 1735 | 2007 | 62.45 | 9.71 | 2185.68 | 113.14 |
| 256K | 472 | 6448.83 | 36.22 | 7.16 | 6514.75 | 114.12 |

<details>
<summary>Test commands</summary>

```bash
./llama-server --model /home/user/UD-Q2_K_XL/DeepSeek-V4-Flash-0731-UD-Q2_K_XL-00001-of-00003.gguf --ctx-size 256000 --gpu-layers 999 --flash-attn on --threads 16 --host 0.0.0.0 --port 8000 --path /home/user/xiangmu/llama.cpp-master/tools/ui/dist
```

</details>

### 3.3 Dual-node cascade DeepSeek-V4-Flash-0731-UD-Q2_K_XL-GGUF (96.8 GB)

- Acceleration: `No`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 1553 | 3.47 | 129.87 | 14.21 | 112.76 | 60.72/56.98 |
| 8K | 233 | 48.26 | 179.68 | 13.74 | 65.22 | 60.52/56.97 |
| 32K | 2135 | 242.83 | 135.27 | 12.48 | 413.9 | 60.71/56.97 |
| 64K | 419 | 586.03 | 112.11 | 11.06 | 623.91 | 60.73/56.98 |
| 128K | 478 | 1598.95 | 78.42 | 9.09 | 1651.54 | 61.06/56.98 |
| 256K | 712 | 4402.39 | 53.06 | 7.21 | 4501.14 | 61.59/57.21 |

<details>
<summary>Test commands</summary>

```bash
Host start command: ./llama-server   --model /home/user/UD-Q2_K_XL/DeepSeek-V4-Flash-0731-UD-Q2_K_XL-00001-of-00003.gguf   --ctx-size 256000   --gpu-layers 999   --flash-attn on   --threads 16   --rpc 192.168.10.30:50052  --host 0.0.0.0 --port 8000  --path /home/user/xiangmu/llama.cpp-master/tools/ui/dist
Worker start command: ./ggml-rpc-server -H 0.0.0.0 -p 50052
```

</details>

### 3.4 Triple-node cascade DeepSeek-V4-Flash-0731-UD-Q2_K_XL-GGUF (96.8 GB)

- Acceleration: `No`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 1229 | 3.78 | 119.39 | 13.4 | 95.5 | 47.89/47.70/26.72 |
| 8K | 530 | 54.84 | 158.11 | 12.94 | 95.8 | 47.92/47.62/26.72 |
| 32K | 2481 | 270.93 | 121.24 | 11.75 | 482.08 | 47.88/47.71/26.73 |
| 64K | 417 | 645.64 | 101.75 | 10.37 | 685.85 | 47.94/47.65/26.72 |
| 128K | 873 | 1709.1 | 73.36 | 8.97 | 1806.42 | 48.56/47.65/26.72 |
| 256K | 2265 | 4840.73 | 48.25 | 7.06 | 5161.55 | 48.92/47.65/26.72 |

<details>
<summary>Test commands</summary>

```bash
Host start command: ./llama-server   --model /home/user/UD-Q2_K_XL/DeepSeek-V4-Flash-0731-UD-Q2_K_XL-00001-of-00003.gguf   --ctx-size 256000   --gpu-layers 999   --flash-attn on   --threads 16   --rpc 192.168.10.30:50052,192.168.10.10:50052  --host 0.0.0.0 --port 8000  --path /home/user/xiangmu/llama.cpp-master/tools/ui/dist
Worker start command: ./ggml-rpc-server -H 0.0.0.0 -p 50052
```

</details>

### 3.5 Qwen3.8-27B-FP4-FAST-GGUF

- Acceleration: `Yes(MTP) N=4`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 3000 | 1.5 | 318.64 | 31.29 | 97.38 | 26.8 |
| 8K | 2087 | 24 | 347.73 | 25.43 | 106.07 | 26.8 |
| 16K | 3000 | 54 | 320.57 | 24.51 | 176.4 | 26.9 |
| 32K | 3000 | 125 | 276.48 | 20.28 | 272.93 | 26.8 |
| 128K | 3000 | 868 | 151.42 | 8.95 | 1203.2 | 26.7 |
| 256K | 392 | 2696 | 94.45 | 6.06 | 2760.69 | 26.8 |

<details>
<summary>Test commands</summary>

```bash
./llama-server -m /home/user/workspace/Qwen3.8-27B-ROCmFP4-FAST.gguf -dev ROCm0 -ngl 99 -fa on -c 256000 -b 2048 -ub 1024 -t 16 -ctk q8_0 -ctv q8_0 --temperature 0 --no-mmap --cont-batching --kv-unified --port 8000 --host 0.0.0.0 --spec-type draft-mtp --spec-draft-n-max 4 --spec-draft-p-min 0.0
```

</details>

### 3.6 MiniCPM5-2B-bf16-GGUF

- Acceleration: `No`
- Records: 5

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 923 | 0.54 | 731.97 | 33.05 | 28.47 | 8.7 |
| 8K | 1258 | 10.81 | 752.38 | 31.52 | 50.72 | 8.7 |
| 16K | 966 | 24.62 | 640.34 | 30.48 | 56.31 | 8.7 |
| 32K | 779 | 65.59 | 478.15 | 28.26 | 93.16 | 8.7 |
| 128K | 1163 | 835.54 | 149.28 | 20.49 | 892.3 | 8.7 |

<details>
<summary>Test commands</summary>

```bash
llama-server.exe  -m  D:\model\MiniCPM5-2B-bf16.gguf -c 131072 -ngl 99 -ngld 99 -t 12 -np 1 --cont-batching --flash-attn on --host 0.0.0.0 --port 8082 --metrics -lv  3 --cache-type-k q8_0 --cache-type-v q8_0 --fit off
```

</details>

## 4. Coverage overview

| Model / deployment | Acceleration | Context lengths tested | Missing context lengths |
| --- | --- | --- | --- |
| Dual-node cascade Qwen3.8-Flash-Next-UD-Q4_K_XL | MTP N=2 | 128 / 8K / 16K / 32K / 128K / 256K | 64K |
| DeepSeek-V4-Flash-0731-UD-Q2_K_XL (single device) | No | 128 / 8K / 32K / 64K / 128K / 256K | 16K |
| Dual-node cascade DeepSeek-V4-Flash-0731-UD-Q2_K_XL | No | 128 / 8K / 32K / 64K / 128K / 256K | 16K |
| Triple-node cascade DeepSeek-V4-Flash-0731-UD-Q2_K_XL | No | 128 / 8K / 32K / 64K / 128K / 256K | 16K |
| Qwen3.8-27B-FP4-FAST | MTP N=4 | 128 / 8K / 16K / 32K / 128K / 256K | 64K |
| MiniCPM5-2B-bf16 | No | 128 / 8K / 16K / 32K / 128K | 64K, 256K |

## 5. Data notes and known issues

1. **VRAM format normalized**: in the original records the 395 data is written as "host: x / worker: y" with mixed full-width and half-width colons; this directory normalizes it to `x/y`, and to `host / worker 1 / worker 2` for triple-node cascades. Only the written format was adjusted; no value was changed.
2. **Typo corrected**: the decode rate in the 32K row of MiniCPM5-2B-bf16 was previously recorded as "28，26" (full-width comma); the original record has since been corrected to `28.26` tokens/s, and this directory matches at `28.26`.
3. **DeepSeek-V4-Flash is missing 16K in every deployment**: the single-device, dual-node cascade, and triple-node cascade tests only covered 128 / 8K / 32K / 64K / 128K / 256K, so 16K is missing. Keep this in mind for cross-deployment comparison.
4. **Speedup metrics**: the "speedup xx%" values in the original records are the improvement of MTP acceleration over the unaccelerated baseline, and "draft acceptance" is the draft acceptance rate. Both are supporting indicators of the acceleration effect, not throughput metrics, so they are omitted from the result tables above and kept in [`test-records.csv`](./test-records.csv).
5. **Model context limit**: the original note for MiniCPM5-2B-bf16 reads "context length set to 128k; the model supports up to 128k only", which is why 256K was not tested.
6. **Device attribution resolved**: a data set was previously labelled "A9-Mega-388 inference performance data"; its six rows match Section 3.1 of this directory (395, dual-node cascade, Qwen3.8-Flash-Next). The root [`README.md`](../../README.md) now attributes that data set to the 395.
7. **To be completed before release**: these records have not been reproduced through two independent clean QA installations, and the hardware details (operating system, BIOS, driver, power profile) have not been fully collected. Do not publish as is.

## 6. Related files

| File | Description |
| --- | --- |
| [`test-records.csv`](./test-records.csv) | Flat data table of all 35 records for the 395 |
| `../A9-Mega-388/README.md` | Test records for the 388 configuration (same structure, for comparison) |
| `../../README.md` | Quantization level selection (bits vs. size / accuracy) and the 4-bit measurements per device |
| `../qa-handoff-template.md` | QA handoff template for installation and functional verification records |
