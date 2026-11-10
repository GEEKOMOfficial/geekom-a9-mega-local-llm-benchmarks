# A9 Mega 388 — Local LLM Inference Test Records

This directory archives the local large language model inference performance tests measured on the **GEEKOM A9 Mega 388** configuration.

- Source: tests measured on physical GEEKOM A9 Mega 388 hardware
- Records: **63**, covering **10** model / deployment / acceleration combinations
- Raw details are also available as [`test-records.csv`](./test-records.csv) in this directory (UTF-8, opens directly in Excel)

## Strata on a single A9 Mega 388

The [dedicated Qwen3.8-Flash-Next benchmark](./Qwen3.8-Flash-Next-Strata.md) covers IQ3_S on the 64 GB 388 and compares it with the single-device Q4 `llama.cpp` run on the 128 GB 395.

Strata 0.2.2 ran the **83.6 GB Qwen3.8-Flash-Next GSQ-RCO-IQ3_S** model on one **64 GB A9 Mega 388** using SSD-resident weights. With multi-token prediction (MTP N=4), it decoded at **24.7–31.3 tokens/s** across all seven tested input lengths, from 128 tokens to 128K. [Strata project](https://github.com/niko1221/strata)

| Input length | Decode with MTP N=4 (tokens/s) | Decode with MTP and suffix off (tokens/s) | Time to first token with MTP N=4 (s) |
| --- | ---: | ---: | ---: |
| 128 | 31.3 | 23.6 | 1.69 |
| 32K | 30.6 | 23.8 | 50.60 |
| 128K | 24.9 | 22.5 | 208.42 |

At 128K, this single-device Strata configuration decoded **2.34× as fast** and had **76% lower time to first token** than the archived dual-node `llama.cpp` run with the 111.4 GB UD-Q4_K_XL model. The two runs used different quantizations, deployments, and MTP settings. [Dual-node benchmark](#31-dual-node-cascade-qwen38-flash-next-ud-q4_k_xlgguf-1114gb-mtp-qwen38-flash-next-q4_k_mgguf-28gb)

The full IQ3_S results and launch commands are in the [MTP N=4 run](#39-strata-ssd-resident-qwen38-flash-next-gsq-rco-iq3_sgguf-836-gb-mtp-n4) and the [run with MTP and suffix off](#310-strata-ssd-resident-qwen38-flash-next-gsq-rco-iq3_sgguf-836-gb-mtp-and-suffix-off).

For the repository-wide model shortlist, see [Section 5.2 of the root README](../../README.md#52-a9-mega-388--three-recommended-models).

## 1. Device and hardware configuration

| Item | Configuration |
| --- | --- |
| Device model | GEEKOM A9 Mega 388 |
| Processor | AMD Ryzen AI MAX+ 388 |
| Graphics | Radeon 8060S |
| Memory bandwidth | 256 GB/s |
| Memory | 64 GB |
| Operating system | Ubuntu 26.04 |
| Graphics driver | 31.50.0.0 |
| ROCm version | 10.0.0 |

## 2. Field descriptions

| Field | Meaning |
| --- | --- |
| Input length (tokens) | Context input length used for the test (128 / 4K / 8K / 16K / 32K / 64K / 128K / 256K) |
| Output length (tokens) | Number of tokens actually generated |
| Time to first token, TTFT (s) | Time from sending the request to receiving the first token |
| Prefill rate (tokens/s) | Prompt processing (prefill) throughput |
| Decode rate (tokens/s) | Generation (decode) throughput |
| End-to-end time (s) | Total time for a single request |
| VRAM (GB) | Video memory usage; for multi-node cascades listed as "host / worker" or "host / worker 1 / worker 2". Strata rows retain both values from the source VRAM / memory column in `value (+value)` format. |

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
| 128K | 4452 | 858.93 | 152.6 | 10.62 | 1278.13 | 65.7/58.05 |

<details>
<summary>Test commands</summary>

```bash
Worker: LD_LIBRARY_PATH="$PWD:$PWD/lib:$PWD/bin:$LD_LIBRARY_PATH" && ./ggml-rpc-server -H 192.168.10.10 -p 50052 -t 16
Host: ./llama-server -m /home/user/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf -ngl 99 -c 256000 -b 2048 -ub 1024 -fa on -np 1 --rpc 192.168.10.10:50052 --host 127.0.0.1 --port 8080 --metrics -lv 4 -md /home/user/Qwen3.8-Flash-Next-UD-Q4_K_XL/mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp --spec-draft-n-max 2
```

</details>

### Inference Engine

- Framework: `llama.cpp`
- Build: `b10830-mix-d5c17a0`
- Source: https://github.com/unslothai/llama.cpp/releases/tag/b10830-mix-d5c17a0

### 3.2 Triple-node cascade Qwen3.8-Flash-Next-UD-Q4_K_XL.gguf (111.4GB) mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf (2.8GB)

- Acceleration: `Yes(MTP) N=2`
- Records: 5

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 5774 | 0.68 | 187.52 | 28 | 206.9 | 56.5/50.8/49.4 |
| 8K | 3790 | 27.57 | 297.14 | 26.9 | 168.46 | 58.3/51.1/49.6 |
| 16K | 3581 | 59.16 | 276.94 | 23.94 | 208.74 | 59.5/51.2/49.5 |
| 32K | 6925 | 136.32 | 240.37 | 22.85 | 439.39 | 60.1/51.6/49.56 |
| 128K | 2354 | 910.03 | 144.03 | 12.28 | 1101.73 | 64.6/51.7/49.97 |

<details>
<summary>Test commands</summary>

```bash
Worker 1: LD_LIBRARY_PATH="$PWD:$PWD/lib:$PWD/bin:$LD_LIBRARY_PATH" && ./ggml-rpc-server -H 192.168.10.10 -p 50052 -t 16
Worker 2: LD_LIBRARY_PATH="$PWD:$PWD/lib:$PWD/bin:$LD_LIBRARY_PATH" && ./ggml-rpc-server -H 192.168.10.30 -p 50053 -t 16
Host: ./llama-server -m /home/user/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf -ngl 99 -c 256000 -b 4096 -ub 2048 -fa on -np 1 --rpc 192.168.10.10:50052,192.168.10.30:50053 --host 127.0.0.1 --port 8080 --metrics -lv 4 -md /home/user/Qwen3.8-Flash-Next-UD-Q4_K_XL/mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp --spec-draft-n-max 2
```

</details>

### Inference Engine

- Framework: `llama.cpp`
- Build: `b10830-mix-d5c17a0`
- Source: https://github.com/unslothai/llama.cpp/releases/tag/b10830-mix-d5c17a0

### 3.3 Qwen3.8-27B-UD-Q4_K_XL-GGUF (17.6GB)

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

### Inference Engine

- Framework: `llama.cpp`
- Build: `b11065`
- Source: https://github.com/ggml-org/llama.cpp/releases?page=31#release-b11065

### 3.4 Gemma-4-31B_q4_0-it-GGUF

- Acceleration: `No`
- Records: 5

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 1477 | 4.77 | 26.83 | 11.28 | 135.71 | 40.8 |
| 8K | 1986 | 117.82 | 69.53 | 10.2 | 312.53 | 40.8 |
| 16K | 2054 | 266.54 | 61.47 | 9.64 | 479.61 | 40.8 |
| 32K | 1686 | 790.54 | 41.45 | 8.56 | 987.51 | 40.8 |
| 128K | 2489 | 10312.51 | 12.71 | 5 | 10810.31 | 40.8 |

<details>
<summary>Test commands</summary>

```bash
llama-server.exe  -m ..\gemma-4-31b\gemma-4-31B_q4_0-it.gguf --mmproj ..\gemma-4-31b\gemma-4-31B-it-mmproj.gguf  -c 262144 -ngl 99 -ngld 99 -t 12 -np 1 --cont-batching --flash-attn on --host 0.0.0.0 --port 8082 --metrics -lv  3  --fit off
```

</details>

### 3.5 Qwen3.6-35B-A3B-UD-Q4_K_M-GGUF (22.7GB) llama-b11065

- Acceleration: `Yes(MTP) N=2`
- Records: 7

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 3094 | 0.16 | 822.22 | 68.03 | 45.64 | 33.31 |
| 8K | 3000 | 6.61 | 1239.7 | 67.76 | 50.88 | 33.35 |
| 16K | 2039 | 14.79 | 1107.6 | 63.55 | 46.88 | 33.42 |
| 32K | 2408 | 32.51 | 1007.86 | 54.3 | 76.86 | 33.46 |
| 64K | 2832 | 103.58 | 632.7 | 50.3 | 159.88 | 33.57 |
| 128K | 1023 | 218.14 | 600.87 | 32.61 | 249.51 | 33.81 |
| 256K | 1575 | 645.04 | 406.4 | 21.66 | 717.75 | 34.28 |

<details>
<summary>Test commands</summary>

```bash
./llama-server -m /home/user/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -ngl 99 --spec-type draft-mtp --spec-draft-n-max 2 -c 256000 -fa on --cache-type-k q8_0 --cache-type-v q8_0 --host 127.0.0.1 --port 8080
```

</details>

### Inference Engine

- Framework: `llama.cpp`
- Build: `b11065`
- Source: https://github.com/ggml-org/llama.cpp/releases?page=31#release-b11065

### 3.6 MiniCPM5-2B-Q4_K_M.GGUF (1.56GB)

- Acceleration: `No`
- Records: 6

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 285 | 0.1 | 1320.23 | 103.1 | 2.86 | 14.81 |
| 8K | 557 | 3.09 | 2654.18 | 87.08 | 9.48 | 15.01 |
| 16K | 2110 | 7.52 | 2179.93 | 75.15 | 35.59 | 15.27 |
| 32K | 1218 | 21.14 | 1550.16 | 61.74 | 40.87 | 16.1 |
| 64K | 2567 | 70.63 | 927.87 | 44.76 | 127.98 | 17.41 |
| 128K | 661 | 255.42 | 513.16 | 29.03 | 278.19 | 17.65 |

<details>
<summary>Test commands</summary>

```bash
./llama-server   -m /home/user/MiniCPM5-2B-Q4_K_M.gguf   --host 127.0.0.1 --port 18083   -c 131072 -b 2048 -ub 512 -ngl 99 -fa on -t 16 -np 1   --warmup
```

</details>

### 3.7 Strata SSD-resident Qwen3.8-Flash-Next-UD-Q4_K_XL.gguf (111.4 GB) (MTP N=4)

Sections 3.7 to 3.10 use Strata 0.2.2 with SSD-resident model weights. The measurements and test commands come from rows 67 to 98 of the `Strata性能测试` sheet. [Source workbook](../大模型推理性能测试记录表.xlsx)

- Acceleration: `Yes(MTP) N=4`
- Records: 7

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM / memory (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 501 | 3.33 | 39 | 18.9 | 29.79 | 52.63 (+11.06) |
| 4K | 710 | 11.25 | 366 | 17 | 52.96 | 52.23 (+11.26) |
| 8K | 633 | 22.19 | 370 | 19.5 | 54.6 | 52.35 (+11.86) |
| 16K | 901 | 38.97 | 421 | 19.7 | 84.65 | 51.91 (+11.60) |
| 32K | 602 | 74.36 | 441 | 18.1 | 107.56 | 52.00 (+11.42) |
| 64K | 900 | 144.4 | 454 | 20.2 | 189.1 | 52.30 (+11.61) |
| 128K | 2874 | 309.91 | 423 | 19.9 | 454.28 | 51.95 (+11.85) |

<details>
<summary>Test commands</summary>

```bash
.venv/bin/python -m serve.server --engine strata --port 8082 --config /dev/stdin <<'EOF'
{"exe":"engine/strata","args":["--pack","/home/u2604/Strata-data/packs/unsloth-ud-q4_k_xl","--native","/home/u2604/model/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf","--expert-profile","data/expert-profile.bin","--expert-cache","auto","--prefill","auto","--spec","4","--spec-min-p","0.5","--mtp","/home/u2604/Strata-data/mtp/rt","--resident-budget-gib", "71","--max-context","256000","--kv","int8","--vision","--vram-reserve-mib","700"],"cwd":".","tokenizer":"/home/u2604/Strata-data/packs/unsloth-ud-q4_k_xl/tokenizer","model_name":"qwen3.8-flash-next-unsloth-ud-q4_k_xl","log":"strata-unsloth-ud-q4_k_xl.log","host":"127.0.0.1","lib_dirs":["/home/u2604/Strata-0.2.2/.venv/lib/python3.14/site-packages/_rocm_sdk_devel/lib","/home/u2604/Strata-0.2.2/.venv/lib/python3.14/site-packages/_rocm_sdk_libraries_gfx1151/lib"],"env":{"STRATA_HIPBLASLT_TUNING":"/home/u2604/Strata-0.2.2/tools/hip/gfx1151-hipblaslt-100400.txt"},"vision":{"exe":"engine/strata-vision-hip","mmproj":"/home/u2604/Strata-data/models/mmproj-Qwen3.8-Flash-Next-BF16.gguf","model":"/home/u2604/model/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf","gpu":true,"max_tokens":1024,"cpu_exe":"engine/strata-vision"}}
EOF
```

</details>

### 3.8 Strata SSD-resident Qwen3.8-Flash-Next-UD-Q4_K_XL.gguf (111.4 GB) (MTP and suffix off)

- Acceleration: `No (MTP and suffix off)`
- Records: 7

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM / memory (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 249 | 3.19 | 41 | 15.7 | 18.98 | 51.54 (+10.47) |
| 4K | 631 | 11.26 | 366 | 14.9 | 53.54 | 51.54 (+10.48) |
| 8K | 626 | 20.75 | 396 | 17.2 | 57.08 | 51.64 (+11.85) |
| 16K | 676 | 38.52 | 426 | 17.3 | 77.54 | 51.37 (+11.70) |
| 32K | 1255 | 75.39 | 435 | 17.3 | 147.87 | 52.48 (+11.13) |
| 64K | 425 | 144.41 | 454 | 16.7 | 169.8 | 52.46 (+11.44) |
| 128K | 602 | 307.75 | 426 | 15.5 | 346.52 | 52.41 (+11.15) |

<details>
<summary>Test commands</summary>

```bash
.venv/bin/python -m serve.server --engine strata --port 8082 --config /dev/stdin <<'EOF'
{"exe":"engine/strata","args":["--pack","/home/u2604/Strata-data/packs/unsloth-ud-q4_k_xl","--native","/home/u2604/model/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf","--expert-profile","data/expert-profile.bin","--expert-cache","auto","--prefill","auto","--spec","4","--spec-min-p","0.5","--suffix-draft","0","--resident-budget-gib", "71","--max-context","256000","--kv","int8","--vision","--vram-reserve-mib","700"],"cwd":".","tokenizer":"/home/u2604/Strata-data/packs/unsloth-ud-q4_k_xl/tokenizer","model_name":"qwen3.8-flash-next-unsloth-ud-q4_k_xl","log":"strata-unsloth-ud-q4_k_xl.log","host":"127.0.0.1","lib_dirs":["/home/u2604/Strata-0.2.2/.venv/lib/python3.14/site-packages/_rocm_sdk_devel/lib","/home/u2604/Strata-0.2.2/.venv/lib/python3.14/site-packages/_rocm_sdk_libraries_gfx1151/lib"],"env":{"STRATA_HIPBLASLT_TUNING":"/home/u2604/Strata-0.2.2/tools/hip/gfx1151-hipblaslt-100400.txt"},"vision":{"exe":"engine/strata-vision-hip","mmproj":"/home/u2604/Strata-data/models/mmproj-Qwen3.8-Flash-Next-BF16.gguf","model":"/home/u2604/model/Qwen3.8-Flash-Next-UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf","gpu":true,"max_tokens":1024,"cpu_exe":"engine/strata-vision"}}
EOF
```

</details>

### 3.9 Strata SSD-resident Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S.gguf (83.6 GB) (MTP N=4)

- Acceleration: `Yes(MTP) N=4`
- Records: 7

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM / memory (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 615 | 1.69 | 77 | 31.3 | 21.31 | 52.92 (+5.03) |
| 4K | 780 | 7.97 | 516 | 28.4 | 35.4 | 52.93 (+5.04) |
| 8K | 680 | 15.67 | 524 | 28.4 | 39.58 | 52.57 (+4.87) |
| 16K | 990 | 26.85 | 611 | 30 | 59.82 | 52.96 (+4.92) |
| 32K | 1673 | 50.6 | 648 | 30.6 | 105.24 | 52.18 (+4.92) |
| 64K | 644 | 101.8 | 644 | 24.7 | 127.84 | 53.12 (+5.16) |
| 128K | 551 | 208.42 | 629 | 24.9 | 230.51 | 53.10 (+4.61) |

<details>
<summary>Test commands</summary>

```bash
.venv/bin/python -m serve.server --engine strata --port 8082 --config /dev/stdin <<'EOF'
{"exe":"engine/strata","args":["--pack","/home/u2604/Strata-data/packs/iq3_s","--native","/home/u2604/model/iq3/Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S-00001-of-00002.gguf","--ple-gguf","/home/u2604/model/iq3/Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S-00002-of-00002.gguf","--mmap-experts","--expert-profile","data/expert-profile.bin","--expert-cache","auto","--prefill","auto","--spec","4","--spec-min-p","0.5","--mtp","/home/u2604/Strata-data/mtp/rt","--max-context","256000","--kv","int8","--vision","--vram-reserve-mib","700"],"cwd":".","tokenizer":"/home/u2604/Strata-data/packs/iq3_s/tokenizer","model_name":"qwen3.8-flash-next-iq3_s","log":"strata-iq3_s.log","host":"127.0.0.1","lib_dirs":["/home/u2604/Strata-0.2.2/.venv/lib/python3.14/site-packages/_rocm_sdk_devel/lib","/home/u2604/Strata-0.2.2/.venv/lib/python3.14/site-packages/_rocm_sdk_libraries_gfx1151/lib"],"env":{"STRATA_HIPBLASLT_TUNING":"/home/u2604/Strata-0.2.2/tools/hip/gfx1151-hipblaslt-100400.txt"},"vision":{"exe":"engine/strata-vision-hip","mmproj":"/home/u2604/Strata-data/models/mmproj-Qwen3.8-Flash-Next-BF16.gguf","model":"/home/u2604/model/iq3/Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S-00001-of-00002.gguf","gpu":true,"max_tokens":1024,"cpu_exe":"engine/strata-vision"}}
EOF
```

</details>

### 3.10 Strata SSD-resident Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S.gguf (83.6 GB) (MTP and suffix off)

- Acceleration: `No (MTP and suffix off)`
- Records: 7

| Input length | Output length | TTFT (s) | Prefill (tokens/s) | Decode (tokens/s) | End-to-end (s) | VRAM / memory (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 328 | 1.7 | 77 | 23.6 | 15.56 | 52.73 (+4.76) |
| 4K | 762 | 8.54 | 482 | 22.4 | 42.52 | 52.88 (+5.04) |
| 8K | 550 | 14.96 | 549 | 23.4 | 38.43 | 52.26 (+5.15) |
| 16K | 560 | 26.34 | 623 | 24.1 | 49.54 | 52.24 (+5.17) |
| 32K | 654 | 50.15 | 654 | 23.8 | 77.58 | 52.04 (+4.81) |
| 64K | 511 | 100.87 | 650 | 23.2 | 122.85 | 52.13 (+5.55) |
| 128K | 549 | 214.21 | 612 | 22.5 | 238.57 | 52.41 (+4.72) |

<details>
<summary>Test commands</summary>

```bash
.venv/bin/python -m serve.server --engine strata --port 8082 --config /dev/stdin <<'EOF'
{"exe":"engine/strata","args":["--pack","/home/u2604/Strata-data/packs/iq3_s","--native","/home/u2604/model/iq3/Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S-00001-of-00002.gguf","--ple-gguf","/home/u2604/model/iq3/Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S-00002-of-00002.gguf","--mmap-experts","--expert-profile","data/expert-profile.bin","--expert-cache","auto","--prefill","auto","--spec","4","--spec-min-p","0.5","--suffix-draft","0","--max-context","256000","--kv","int8","--vision","--vram-reserve-mib","700"],"cwd":".","tokenizer":"/home/u2604/Strata-data/packs/iq3_s/tokenizer","model_name":"qwen3.8-flash-next-iq3_s","log":"strata-iq3_s.log","host":"127.0.0.1","lib_dirs":["/home/u2604/Strata-0.2.2/.venv/lib/python3.14/site-packages/_rocm_sdk_devel/lib","/home/u2604/Strata-0.2.2/.venv/lib/python3.14/site-packages/_rocm_sdk_libraries_gfx1151/lib"],"env":{"STRATA_HIPBLASLT_TUNING":"/home/u2604/Strata-0.2.2/tools/hip/gfx1151-hipblaslt-100400.txt"},"vision":{"exe":"engine/strata-vision-hip","mmproj":"/home/u2604/Strata-data/models/mmproj-Qwen3.8-Flash-Next-BF16.gguf","model":"/home/u2604/model/iq3/Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S-00001-of-00002.gguf","gpu":true,"max_tokens":1024,"cpu_exe":"engine/strata-vision"}}
EOF
```

</details>

## 4. Coverage overview

| Model / deployment | Acceleration | Context lengths tested | Missing context lengths |
| --- | --- | --- | --- |
| Dual-node cascade Qwen3.8-Flash-Next-UD-Q4_K_XL | MTP N=2 | 128 / 8K / 16K / 32K / 128K | 4K, 64K, 256K |
| Triple-node cascade Qwen3.8-Flash-Next-UD-Q4_K_XL | MTP N=2 | 128 / 8K / 16K / 32K / 128K | 4K, 64K, 256K |
| Qwen3.8-27B-UD-Q4_K_XL | MTP N=4 | 128 / 8K / 16K / 32K / 64K / 128K / 256K | 4K |
| Gemma-4-31B_q4_0-it | No | 128 / 8K / 16K / 32K / 128K | 4K, 64K, 256K |
| Qwen3.6-35B-A3B-UD-Q4_K_M | MTP N=2 | 128 / 8K / 16K / 32K / 64K / 128K / 256K | 4K |
| MiniCPM5-2B-Q4_K_M | No | 128 / 8K / 16K / 32K / 64K / 128K | 4K, 256K |
| Strata SSD-resident Qwen3.8-Flash-Next-UD-Q4_K_XL | MTP N=4 | 128 / 4K / 8K / 16K / 32K / 64K / 128K | 256K |
| Strata SSD-resident Qwen3.8-Flash-Next-UD-Q4_K_XL | MTP and suffix off | 128 / 4K / 8K / 16K / 32K / 64K / 128K | 256K |
| Strata SSD-resident Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S | MTP N=4 | 128 / 4K / 8K / 16K / 32K / 64K / 128K | 256K |
| Strata SSD-resident Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S | MTP and suffix off | 128 / 4K / 8K / 16K / 32K / 64K / 128K | 256K |

## 5. Data notes and known issues

1. **Gemma-4-31B 256K test failed**: the `Gemma-4-31B_q4_0-it` 256K scenario failed with a test error and produced no usable performance metric, so it is not included in the results above.
2. **Uneven context coverage**: test groups cover different context lengths (see the table above). Compare results at the same input length.

## 6. Related files

| File | Description |
| --- | --- |
| [`test-records.csv`](./test-records.csv) | Flat data table of all 63 records for the 388 |
| `../A9-Mega-395/README.md` | Test records for the 395 configuration (same structure, for comparison) |
| `../../README.md` | Quantization level selection (bits vs. size / accuracy) and the 4-bit measurements per device |
