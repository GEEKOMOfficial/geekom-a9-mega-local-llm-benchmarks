# A9 Mega 388 — Local LLM Inference Test Records

This directory archives the local large language model inference performance tests measured on the **GEEKOM A9 Mega 388** configuration.

- Source: tests measured on physical GEEKOM A9 Mega 388 hardware
- Records: **34**, covering **6** model / deployment combinations
- Raw details are also available as [`test-records.csv`](./test-records.csv) in this directory (UTF-8, opens directly in Excel)

## 1. Device and hardware configuration

| Item | Configuration |
| --- | --- |
| Device model | GEEKOM A9 Mega 388 |
| Processor | AMD Ryzen AI MAX+ 388 |
| Graphics | Radeon 8060S |
| Memory bandwidth | 256 GB/s |
| Memory | 64 GB |
| Operating system | To be confirmed |
| BIOS version | To be confirmed |
| Graphics / NPU driver | To be confirmed |
| Power profile | To be confirmed |

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
| VRAM (GB) | Video memory usage; for multi-node cascades listed as "host / worker" or "host / worker 1 / worker 2" |

## 3. Test results

### 3.1 Dual-node cascade Qwen3.8-Flash-Next-UD-Q4_K_XL.gguf (111.4GB) mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf (2.8GB)

- Acceleration: `Yes(MTP) N=2`
- Records: 5

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 7954 | 2.59 | 191.97 | 30.76 | 261.17 | 62.4/57.5 |
| 8K | 4160 | 28.62 | 299.42 | 26.14 | 187.76 | 63.8/57.7 |
| 16K | 11079 | 56.61 | 296.09 | 25.62 | 489.05 | 63.7/57.8 |
| 32K | 2316 | 131.34 | 252.36 | 23.68 | 229.14 | 64.7/57.8 |
| 128K | 4452 | 861.41 | 152.6 | 10.62 | 1280.62 | 65.7/58.05 |

<details>
<summary>Test commands</summary>

```bash
Worker: LD_LIBRARY_PATH="$PWD:$PWD/lib:$PWD/bin:$LD_LIBRARY_PATH" && env -u HSA_OVERRIDE_GFX_VERSION ./ggml-rpc-server -H 192.168.10.10 -p 50052 -t 16
Host: env -u HSA_OVERRIDE_GFX_VERSION ./llama-server -m /home/user/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf -ngl 99 -c 256000 -b 2048 -ub 1024 -fa on -np 1 --rpc 192.168.10.10:50052 --host 127.0.0.1 --port 8080 --metrics -lv 4 -md /home/user/Qwen3.8-Flash-Next-UD-Q4_K_XL/mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp --spec-draft-n-max 2
```

</details>

### 3.2 Triple-node cascade Qwen3.8-Flash-Next-UD-Q4_K_XL.gguf (111.4GB) mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf (2.8GB)

- Acceleration: `Yes(MTP) N=2`
- Records: 5

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 5774 | 2.66 | 187.52 | 28 | 208.87 | 56.5/50.8/49.4 |
| 8K | 3790 | 28.84 | 297.14 | 26.9 | 169.73 | 58.3/51.1/49.6 |
| 16K | 3581 | 60.52 | 276.94 | 23.94 | 210.1 | 59.5/51.2/49.5 |
| 32K | 6925 | 137.89 | 240.37 | 22.85 | 440.95 | 60.1/51.6/49.56 |
| 128K | 2354 | 912.65 | 144.03 | 12.28 | 1104.34 | 64.6/51.7/49.97 |

<details>
<summary>Test commands</summary>

```bash
Worker 1: LD_LIBRARY_PATH="$PWD:$PWD/lib:$PWD/bin:$LD_LIBRARY_PATH" && env -u HSA_OVERRIDE_GFX_VERSION ./ggml-rpc-server -H 192.168.10.10 -p 50052 -t 16
Worker 2: LD_LIBRARY_PATH="$PWD:$PWD/lib:$PWD/bin:$LD_LIBRARY_PATH" && env -u HSA_OVERRIDE_GFX_VERSION ./ggml-rpc-server -H 192.168.10.30 -p 50053 -t 16
Host: env -u HSA_OVERRIDE_GFX_VERSION ./llama-server -m /home/user/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf -ngl 99 -c 256000 -b 4096 -ub 2048 -fa on -np 1 --rpc 192.168.10.10:50052,192.168.10.30:50053 --host 127.0.0.1 --port 8080 --metrics -lv 4 -md /home/user/Qwen3.8-Flash-Next-UD-Q4_K_XL/mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp --spec-draft-n-max 2
```

</details>

### 3.3 Qwen3.8-27B-Q4_K_M-GGUF

- Acceleration: `Yes(MTP) N=4`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 3000 | 1.5 | 291.89 | 20.24 | 149.72 | 39.07 |
| 8K | 727 | 25 | 333.83 | 21.3 | 59.13 | 39.12 |
| 16K | 2131 | 66 | 312.45 | 19.53 | 175.11 | 39.19 |
| 32K | 854 | 109 | 299.12 | 16.87 | 159.62 | 39.66 |
| 128K | 2195 | 582 | 202.63 | 9.88 | 804.17 | 40.25 |
| 256K | 3000 | 1466 | 147.26 | 6.06 | 1961.05 | 41.14 |

<details>
<summary>Test commands</summary>

```bash
./llama-server -m /home/user/Qwen3.8-27B-UD-Q4_K_XL.gguf -ngl 99 --spec-type draft-mtp --spec-draft-n-max 4 -c 256000 -fa on --cache-type-k q8_0 --cache-type-v q8_0 --host 127.0.0.1 --port 8080
```

</details>

### 3.4 Gemma-4-31B_q4_0-it-GGUF

- Acceleration: `No`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 1477 | 8.68 | 26.83 | 11.28 | 139.62 | 40.8 |
| 8K | 1986 | 127.53 | 69.53 | 10.2 | 322.24 | 40.8 |
| 16K | 2054 | 283.61 | 61.47 | 9.64 | 496.68 | 40.8 |
| 32K | 1686 | 844.18 | 41.45 | 8.56 | 1041.14 | 40.8 |
| 128K | 2489 | 10895.64 | 12.71 | 5 | 11393.44 | 40.8 |
| 256K | N/A (test error, no output) |  |  |  |  |  |

<details>
<summary>Test commands</summary>

```bash
llama-server.exe  -m ..\gemma-4-31b\gemma-4-31B_q4_0-it.gguf --mmproj ..\gemma-4-31b\gemma-4-31B-it-mmproj.gguf  -c 262144 -ngl 99 -ngld 99 -t 12 -np 1 --cont-batching --flash-attn on --host 0.0.0.0 --port 8082 --metrics -lv  3  --fit off
```

</details>

### 3.5 Qwen3.6-35B-A3B-UD-Q4_K_M-GGUF(22.7GB) llama-b11065

- Acceleration: `Yes(MTP) N=2`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 3094 | 0.5 | 822.22 | 68.03 | 45.98 | 33.31 |
| 8K | 3000 | 6.7 | 1239.7 | 67.76 | 50.97 | 33.35 |
| 16K | 2039 | 18 | 1107.6 | 63.55 | 50.08 | 33.42 |
| 32K | 2408 | 32 | 1007.86 | 54.3 | 76.35 | 33.46 |
| 128K | 1023 | 196 | 600.87 | 32.61 | 227.37 | 33.81 |
| 256K | 1575 | 542 | 406.4 | 21.66 | 614.71 | 34.28 |

<details>
<summary>Test commands</summary>

```bash
./llama-server -m /home/user/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -ngl 99 --spec-type draft-mtp --spec-draft-n-max 4 -c 256000 -fa on --cache-type-k q8_0 --cache-type-v q8_0 --host 127.0.0.1 --port 8080
```

</details>

### 3.6 MiniCPM5-2B-Q4_K_M.GGUF

- Acceleration: `No`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 285 | 0.2 | 1320.23 | 103.1 | 2.96 | 14.81 |
| 8K | 557 | 3.1 | 2654.18 | 87.08 | 9.5 | 15.01 |
| 16K | 2110 | 7.4 | 2179.93 | 75.15 | 35.48 | 15.27 |
| 32K | 1218 | 20 | 1550.16 | 61.74 | 39.73 | 16.1 |
| 64K | 2567 | 67 | 927.87 | 44.76 | 124.35 | 17.41 |
| 128K | 661 | 243 | 513.16 | 29.03 | 265.77 | 17.65 |

<details>
<summary>Test commands</summary>

```bash
./llama-server   -m /home/user/MiniCPM5-2B-Q4_K_M.gguf   --host 127.0.0.1 --port 18083   -c 131072 -b 2048 -ub 512 -ngl 99 -fa on -t 16 -np 1   --warmup
```

</details>

## 4. Coverage overview

| Model / deployment | Acceleration | Context lengths tested | Missing context lengths |
| --- | --- | --- | --- |
| Dual-node cascade Qwen3.8-Flash-Next-UD-Q4_K_XL | MTP N=2 | 128 / 8K / 16K / 32K / 128K | 64K, 256K |
| Triple-node cascade Qwen3.8-Flash-Next-UD-Q4_K_XL | MTP N=2 | 128 / 8K / 16K / 32K / 128K | 64K, 256K |
| Qwen3.8-27B-Q4_K_M | MTP N=4 | 128 / 8K / 16K / 32K / 128K / 256K | 64K |
| Gemma-4-31B_q4_0-it | No | 128 / 8K / 16K / 32K / 128K | 64K; 256K failed |
| Qwen3.6-35B-A3B-UD-Q4_K_M | MTP N=2 | 128 / 8K / 16K / 32K / 128K / 256K | 64K |
| MiniCPM5-2B-Q4_K_M | No | 128 / 8K / 16K / 32K / 64K / 128K | 256K |

## 5. Data notes and known issues

1. **Gemma-4-31B 256K test failed**: the original record marks the output length column as "N/A (test error, no output)"; that row contains no usable performance metric.
2. **Uneven context coverage**: the six test groups do not cover the same context lengths (see the table above); keep this in mind when comparing across models.
3. **VRAM recording format**: a single device records a plain value; a dual-node cascade records `host / worker`; a triple-node cascade records `host / worker 1 / worker 2`. The original 388 records already use `/` as the separator, and this directory matches their format and values exactly.
4. **Draft acceptance rate**: the "draft acceptance rate" in the MTP records is taken from the original records and explains the speedup effect; it is not a throughput metric, so it is omitted from the result tables above and kept in [`test-records.csv`](./test-records.csv).
5. **Device attribution resolved**: a data set was previously labelled "A9-Mega-388 inference performance data", but its six rows match the 395 records (128 length: TTFT 1.19, prefill 151.58, decode 34.27). The root [`README.md`](../../README.md) now attributes that data set to the 395.
6. **To be completed before release**: these records have not been reproduced through two independent clean QA installations, and the hardware details (operating system, BIOS, driver, power profile) have not been fully collected. Do not publish as is.

## 6. Related files

| File | Description |
| --- | --- |
| [`test-records.csv`](./test-records.csv) | Flat data table of all 34 records for the 388 |
| `../A9-Mega-395/README.md` | Test records for the 395 configuration (same structure, for comparison) |
| `../../README.md` | Quantization level selection (bits vs. size / accuracy) and the 4-bit measurements per device |
| `../qa-handoff-template.md` | QA handoff template for installation and functional verification records |
