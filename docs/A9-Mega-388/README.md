# A9 Mega 388 — Local LLM Inference Test Records

This directory archives the local large language model inference performance tests measured on the **GEEKOM A9 Mega 388** configuration.

- Source: tests measured on physical GEEKOM A9 Mega 388 hardware
- Records: **36**, covering **6** model / deployment combinations
- Raw details are also available as [`test-records.csv`](./test-records.csv) in this directory (UTF-8, opens directly in Excel)

## 1. Device and hardware configuration

| Item | Configuration |
| --- | --- |
| Device model | GEEKOM A9 Mega 388 |
| Processor | AMD Ryzen AI MAX+ 388 |
| Graphics | Radeon 8060S |
| Memory bandwidth | 256 GB/s |
| Memory | 64 GB |
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
| VRAM (GB) | Video memory usage; for multi-node cascades listed as "host / worker" or "host / worker 1 / worker 2" |

## 3. Test results

### 3.1 Dual-node cascade Qwen3.8-Flash-Next-UD-Q4_K_XL.gguf (111.4GB) mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf (2.8GB)

- Acceleration: `Yes(MTP) N=2`
- Records: 5

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 7954 | 0.67 | 191.97 | 30.76 | 259.25 | 62.4/57.5 |
| 8K | 4160 | 27.36 | 299.42 | 26.14 | 186.5 | 63.8/57.7 |
| 16K | 11079 | 55.33 | 296.09 | 25.62 | 487.77 | 63.7/57.8 |
| 32K | 2316 | 129.85 | 252.36 | 23.68 | 227.65 | 64.7/57.8 |
| 128K | 4452 | 858.93 | 152.6 | 10.62 | 1278.14 | 65.7/58.05 |

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
| 128 | 5774 | 0.68 | 187.52 | 28 | 206.89 | 56.5/50.8/49.4 |
| 8K | 3790 | 27.57 | 297.14 | 26.9 | 168.46 | 58.3/51.1/49.6 |
| 16K | 3581 | 59.16 | 276.94 | 23.94 | 208.74 | 59.5/51.2/49.5 |
| 32K | 6925 | 136.32 | 240.37 | 22.85 | 439.38 | 60.1/51.6/49.56 |
| 128K | 2354 | 910.03 | 144.03 | 12.28 | 1101.72 | 64.6/51.7/49.97 |

<details>
<summary>Test commands</summary>

```bash
Worker 1: LD_LIBRARY_PATH="$PWD:$PWD/lib:$PWD/bin:$LD_LIBRARY_PATH" && env -u HSA_OVERRIDE_GFX_VERSION ./ggml-rpc-server -H 192.168.10.10 -p 50052 -t 16
Worker 2: LD_LIBRARY_PATH="$PWD:$PWD/lib:$PWD/bin:$LD_LIBRARY_PATH" && env -u HSA_OVERRIDE_GFX_VERSION ./ggml-rpc-server -H 192.168.10.30 -p 50053 -t 16
Host: env -u HSA_OVERRIDE_GFX_VERSION ./llama-server -m /home/user/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf -ngl 99 -c 256000 -b 4096 -ub 2048 -fa on -np 1 --rpc 192.168.10.10:50052,192.168.10.30:50053 --host 127.0.0.1 --port 8080 --metrics -lv 4 -md /home/user/Qwen3.8-Flash-Next-UD-Q4_K_XL/mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp --spec-draft-n-max 2
```

</details>

### 3.3 Qwen3.8-27B-UD-Q4_K_XL-GGUF

- Acceleration: `Yes(MTP) N=4`
- Records: 7

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 3000 | 0.44 | 291.89 | 20.24 | 148.66 | 39.07 |
| 8K | 727 | 24.54 | 333.83 | 21.3 | 58.67 | 39.12 |
| 16K | 2131 | 52.44 | 312.45 | 19.53 | 161.55 | 39.19 |
| 32K | 854 | 109.55 | 299.12 | 16.87 | 160.17 | 39.66 |
| 64K | 3000 | 268.94 | 243.68 | 12.86 | 502.22 | 41.09 |
| 128K | 2195 | 646.85 | 202.63 | 9.88 | 869.02 | 40.25 |
| 256K | 3000 | 1780.14 | 147.26 | 6.06 | 2275.19 | 41.14 |

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
| 128 | 1477 | 4.77 | 26.83 | 11.28 | 135.71 | 40.8 |
| 8K | 1986 | 117.82 | 69.53 | 10.2 | 312.53 | 40.8 |
| 16K | 2054 | 266.54 | 61.47 | 9.64 | 479.61 | 40.8 |
| 32K | 1686 | 790.54 | 41.45 | 8.56 | 987.5 | 40.8 |
| 128K | 2489 | 10312.51 | 12.71 | 5 | 10810.31 | 40.8 |
| 256K | N/A |  |  |  |  |  |

<details>
<summary>Test commands</summary>

```bash
llama-server.exe  -m ..\gemma-4-31b\gemma-4-31B_q4_0-it.gguf --mmproj ..\gemma-4-31b\gemma-4-31B-it-mmproj.gguf  -c 262144 -ngl 99 -ngld 99 -t 12 -np 1 --cont-batching --flash-attn on --host 0.0.0.0 --port 8082 --metrics -lv  3  --fit off
```

</details>

### 3.5 Qwen3.6-35B-A3B-UD-Q4_K_M-GGUF(22.7GB) llama-b11065

- Acceleration: `Yes(MTP) N=2`
- Records: 7

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 3094 | 0.16 | 822.22 | 68.03 | 45.64 | 33.31 |
| 8K | 3000 | 6.61 | 1239.7 | 67.76 | 50.88 | 33.35 |
| 16K | 2039 | 14.79 | 1107.6 | 63.55 | 46.87 | 33.42 |
| 32K | 2408 | 32.51 | 1007.86 | 54.3 | 76.86 | 33.46 |
| 64K | 2832 | 103.58 | 632.7 | 50.3 | 159.88 | 33.57 |
| 128K | 1023 | 218.14 | 600.87 | 32.61 | 249.51 | 33.81 |
| 256K | 1575 | 645.04 | 406.4 | 21.66 | 717.75 | 34.28 |

<details>
<summary>Test commands</summary>

```bash
./llama-server -m /home/user/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -ngl 99 --spec-type draft-mtp --spec-draft-n-max 4 -c 256000 -fa on --cache-type-k q8_0 --cache-type-v q8_0 --host 127.0.0.1 --port 8080
```

</details>

### 3.6 MiniCPM5-2B-Q4_K_M.GGUF (1.56GB)

- Acceleration: `No`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 285 | 0.1 | 1320.23 | 103.1 | 2.86 | 14.81 |
| 8K | 557 | 3.09 | 2654.18 | 87.08 | 9.49 | 15.01 |
| 16K | 2110 | 7.52 | 2179.93 | 75.15 | 35.6 | 15.27 |
| 32K | 1218 | 21.14 | 1550.16 | 61.74 | 40.87 | 16.1 |
| 64K | 2567 | 70.63 | 927.87 | 44.76 | 127.98 | 17.41 |
| 128K | 661 | 255.42 | 513.16 | 29.03 | 278.19 | 17.65 |

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
| Qwen3.8-27B-UD-Q4_K_XL | MTP N=4 | 128 / 8K / 16K / 32K / 64K / 128K / 256K | None |
| Gemma-4-31B_q4_0-it | No | 128 / 8K / 16K / 32K / 128K | 64K; 256K failed |
| Qwen3.6-35B-A3B-UD-Q4_K_M | MTP N=2 | 128 / 8K / 16K / 32K / 64K / 128K / 256K | None |
| MiniCPM5-2B-Q4_K_M | No | 128 / 8K / 16K / 32K / 64K / 128K | 256K |

## 5. Data notes and known issues

1. **Gemma-4-31B 256K test failed**: the record marks the output length as `N/A` together with the note "256K test error"; that row contains no usable performance metric.
2. **Uneven context coverage**: the six test groups do not cover the same context lengths (see the table above); keep this in mind when comparing across models. The 64K scenario has since been added for `Qwen3.8-27B-UD-Q4_K_XL` and `Qwen3.6-35B-A3B-UD-Q4_K_M`.
3. **VRAM recording format**: a single device records a plain value; a dual-node cascade records `host / worker`; a triple-node cascade records `host / worker 1 / worker 2`. The original 388 records already use `/` as the separator, and this directory matches their format and values exactly.
4. **Draft acceptance rate**: the "draft acceptance rate" in the MTP records is taken from the original records and explains the speedup effect; it is not a throughput metric, so it is omitted from the result tables above and kept in [`test-records.csv`](./test-records.csv).
5. **Device attribution resolved**: a data set was previously labelled "A9-Mega-388 inference performance data", but its six rows match the 395 records (128 length: TTFT 0.84, prefill 151.58, decode 34.27). The root [`README.md`](../../README.md) now attributes that data set to the 395.
6. **To be completed before release**: these records have not been reproduced through two independent clean QA installations, and the hardware details (operating system, BIOS, driver, power profile) have not been fully collected. Do not publish as is.

## 6. Related files

| File | Description |
| --- | --- |
| [`test-records.csv`](./test-records.csv) | Flat data table of all 36 records for the 388 |
| `../A9-Mega-395/README.md` | Test records for the 395 configuration (same structure, for comparison) |
| `../../README.md` | Quantization level selection (bits vs. size / accuracy) and the 4-bit measurements per device |
| `../qa-handoff-template.md` | QA handoff template for installation and functional verification records |
