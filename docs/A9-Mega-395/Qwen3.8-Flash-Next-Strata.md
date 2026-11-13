# Qwen3.8-Flash-Next with Strata on the A9 Mega 395

The **GEEKOM A9 Mega 395 with 128 GB of unified memory** runs Qwen3.8-Flash-Next with Strata in both memory-resident and SSD-backed modes. In these Strata measurements, **GSQ-RCO-IQ3_S (83.6 GB) reaches 47.9 tokens/s**, while **UD-Q4_K_XL (111.4 GB) reaches 42.4 tokens/s**, both at 4K input with multi-token prediction (MTP N=4).

The advantage continues at long context. At **128K input tokens**, the memory-resident configurations generate **37.2 tokens/s for IQ3_S** and **33.2 tokens/s for Q4_K_XL**. Q4_K_XL returns the first token in **111.58 seconds**, compared with **720.61 seconds** in the earlier single-device `llama.cpp` record: an **85% reduction in TTFT**, alongside **2.15× decode throughput**.

## Test setup and coverage

| Item | Recorded configuration |
| --- | --- |
| Device | One GEEKOM A9 Mega 395, AMD Ryzen AI MAX+ 395, Radeon 8060S, 128 GB memory |
| Device environment | Ubuntu 26.04 and ROCm 10.0.0 in the [395 hardware archive](./README.md#1-device-and-hardware-configuration) |
| Strata build | Launch paths identify `Strata-0.2.2-100400` and the `build-halo-100400/strata` executable; no commit hash is recorded |
| Models | `Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S.gguf` (83.6 GB) and `Qwen3.8-Flash-Next-UD-Q4_K_XL.gguf` (111.4 GB) |
| Residency | Memory-resident experts (`--resident-experts`) or SSD-backed experts (`--mmap-experts`) |
| Acceleration | MTP N=4, plus a baseline labeled MTP off / suffix drafting off |
| Context and KV cache | `--max-context 256000`, `--kv int8`; measured inputs from 128 to 128K tokens |
| Coverage | 56 measurements: two models × two residency modes × two acceleration settings × seven input lengths |

The Strata commands source `strata-rocm100400/scripts/env-100400.sh` and load the corresponding ROCm SDK libraries. The device environment above comes from the existing hardware archive.

Decode measures generation speed, prefill measures prompt processing speed, and time to first token (TTFT) measures the wait before the response starts. In the tables below, **baseline** means the MTP-off / suffix-off configuration. Prefill and TTFT columns report the MTP N=4 runs.

## Memory-resident performance

### GSQ-RCO-IQ3_S, 83.6 GB

| Input tokens | Decode, MTP N=4 (tok/s) | Decode, baseline (tok/s) | Prefill, MTP N=4 (tok/s) | TTFT, MTP N=4 (s) |
| --- | ---: | ---: | ---: | ---: |
| 128 | 42.9 | 32.4 | 258 | 0.52 |
| 4K | 47.9 | 31.7 | 971 | 4.24 |
| 8K | 42.0 | 32.0 | 1112 | 7.39 |
| 16K | 39.1 | 31.9 | 1185 | 13.85 |
| 32K | 40.0 | 31.6 | 1231 | 26.64 |
| 64K | 36.8 | 31.2 | 1214 | 54.01 |
| 128K | 37.2 | 25.9 | 1116 | 117.47 |

MTP increases recorded decode throughput by **18%–51%** across these input lengths. At 128K, decode rises from **25.9 to 37.2 tokens/s**, a **44% gain**. Prefill stays above 1100 tokens/s from 8K through 128K input.

### UD-Q4_K_XL, 111.4 GB

| Input tokens | Decode, MTP N=4 (tok/s) | Decode, baseline (tok/s) | Prefill, MTP N=4 (tok/s) | TTFT, MTP N=4 (s) |
| --- | ---: | ---: | ---: | ---: |
| 128 | 37.7 | 28.1 | 294 | 0.46 |
| 4K | 42.4 | 28.0 | 963 | 4.28 |
| 8K | 38.3 | 28.2 | 1043 | 7.88 |
| 16K | 35.8 | 27.2 | 1146 | 14.32 |
| 32K | 35.1 | 27.9 | 1212 | 27.06 |
| 64K | 31.9 | 27.5 | 1219 | 53.79 |
| 128K | 33.2 | 25.4 | 1175 | 111.58 |

MTP increases recorded decode throughput by **16%–51%**. At 128K, Q4_K_XL generates **31% faster** than its Strata baseline. Its MTP run also records a lower TTFT at that input length (**111.58 s vs 151.57 s**), although prefill and TTFT are close between the two settings at shorter inputs.

## SSD-backed performance

SSD-backed experts reduce the recorded memory readings while retaining **31.0 tokens/s for IQ3_S** and **29.1 tokens/s for Q4_K_XL** at 128K input with MTP N=4.

### GSQ-RCO-IQ3_S, 83.6 GB

| Input tokens | Decode, MTP N=4 (tok/s) | Decode, baseline (tok/s) | Prefill, MTP N=4 (tok/s) | TTFT, MTP N=4 (s) |
| --- | ---: | ---: | ---: | ---: |
| 128 | 33.5 | 28.3 | 24 | 7.90 |
| 4K | 44.8 | 27.9 | 620 | 6.52 |
| 8K | 36.6 | 28.1 | 860 | 9.62 |
| 16K | 36.1 | 27.8 | 992 | 16.62 |
| 32K | 34.2 | 27.2 | 1073 | 30.64 |
| 64K | 35.5 | 27.4 | 1093 | 60.06 |
| 128K | 31.0 | 26.5 | 1050 | 124.93 |

### UD-Q4_K_XL, 111.4 GB

| Input tokens | Decode, MTP N=4 (tok/s) | Decode, baseline (tok/s) | Prefill, MTP N=4 (tok/s) | TTFT, MTP N=4 (s) |
| --- | ---: | ---: | ---: | ---: |
| 128 | 30.4 | 24.1 | 33 | 5.76 |
| 4K | 34.8 | 23.8 | 505 | 8.00 |
| 8K | 30.7 | 24.0 | 709 | 11.67 |
| 16K | 31.1 | 24.0 | 810 | 20.35 |
| 32K | 30.4 | 23.8 | 890 | 36.93 |
| 64K | 28.9 | 23.3 | 870 | 75.45 |
| 128K | 29.1 | 23.3 | 862 | 152.18 |

At 128K, memory residency is **20% faster for IQ3_S decode** and **14% faster for Q4_K_XL decode** than the corresponding SSD-backed MTP run. The SSD-backed IQ3_S 128-token run records **7.90 seconds TTFT**, longer than its 4K run. The cause and cache state were not recorded, so this value is retained as measured.

### Memory readings at 128K input

Memory usage is reported as two-part readings. The accounting of the parenthesized component was not recorded, so these values should not be treated as total physical memory requirements or combined with SSD model sizes.

| Configuration | MTP N=4 reading (GB) | Baseline reading (GB) |
| --- | ---: | ---: |
| IQ3_S, memory-resident | 61.93 (+9.65) | 60.49 (+9.41) |
| Q4_K_XL, memory-resident | 91.26 (+10.14) | 89.91 (+10.23) |
| IQ3_S, SSD-backed | 22.67 (+6.48) | 21.05 (+6.59) |
| Q4_K_XL, SSD-backed | 30.50 (+7.60) | 29.05 (+7.67) |

## Comparison with the earlier 395 llama.cpp record

This comparison uses **memory-resident Q4_K_XL with Strata MTP N=4** and the earlier **single-device Q4_K_XL with `llama.cpp` MTP N=2**, both on the 128 GB 395. The earlier engine build is `b10909-mix-bea84f7`. [Earlier measurements and launch command](./README.md#31-qwen38-flash-next-ud-q4_k_xlgguf-1114gb-mtp-qwen38-flash-next-q4_k_mgguf-28gb)

| Input tokens | Strata decode (tok/s) | llama.cpp decode (tok/s) | Strata TTFT (s) | llama.cpp TTFT (s) |
| --- | ---: | ---: | ---: | ---: |
| 128 | 37.7 | 32.43 | 0.46 | 0.97 |
| 8K | 38.3 | 28.48 | 7.88 | 26.96 |
| 16K | 35.8 | 25.88 | 14.32 | 58.33 |
| 32K | 35.1 | 23.58 | 27.06 | 112.14 |
| 64K | 31.9 | 18.06 | 53.79 | 283.41 |
| 128K | 33.2 | 15.45 | 111.58 | 720.61 |

Strata records higher decode throughput and lower TTFT at every shared input length. At 128K, prefill rises from **181.89 to 1175 tokens/s (6.46×)**, and the first-token wait falls from about **12 minutes to 1 minute 52 seconds**. Decode throughput rises from **15.45 to 33.2 tokens/s (2.15×)**.

These figures compare the complete recorded configurations. The engine, MTP implementation and depth, memory handling, and runtime settings differ. They do not isolate an engine-only speedup. The earlier archive has no 4K single-device result.

## Runtime settings and data limits

The following key settings distinguish the tested configurations. They summarize the launch options rather than provide complete launch commands.

| Setting | Memory-resident | SSD-backed |
| --- | --- | --- |
| Expert residency | `--resident-experts` | `--mmap-experts` |
| Expert cache | `--expert-cache auto` | `--expert-cache 4096` |
| Prefill | `--prefill auto` | `--prefill auto` |
| Context and KV cache | `--max-context 256000 --kv int8` | `--max-context 256000 --kv int8` |
| VRAM reserve | `--vram-reserve-mib 700` | `--vram-reserve-mib 700` |

MTP runs specify `--mtp` and `--spec 4`; the baseline commands omit `--mtp` and set `--suffix-draft 0`. The resident MTP commands also set `--mtp-q4 all` and `--mtp-window 8192`. Settings beyond these options vary between runs.

Each configuration has one recorded measurement per input length. Generated output lengths differ between tests, so end-to-end totals should not be used as direct speedup ratios. Test dates, repeated-run variability, output-quality evaluations, and SSD model specifications were not recorded. The configured context limit is 256000, but no 256K Strata measurement is recorded for the 395.

## Related records

- [395 hardware and earlier llama.cpp archive](./README.md)
- [Earlier 395 llama.cpp CSV](./test-records.csv)
- [388 Strata performance summary](../A9-Mega-388/Qwen3.8-Flash-Next-Strata.md)
