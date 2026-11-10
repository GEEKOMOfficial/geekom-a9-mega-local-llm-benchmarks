# Qwen3.8-Flash-Next with Strata on the A9 Mega 388

The GEEKOM A9 Mega 388 hits a practical sweet spot for running large Qwen mixture-of-experts (MoE) models locally. It pairs an **AMD Ryzen AI Max+ 388 and 64 GB of unified LPDDR5X memory** with **Strata's SSD offload**, which lets the engine load SSD-backed expert weights as needed. [GEEKOM A9 Mega specifications](https://www.geekompc.com/geekom-a9-mega-ai-mini-pc/)

In the benchmark, Strata 0.2.2 ran the **83.6 GB Qwen3.8-Flash-Next GSQ-RCO-IQ3_S** model on one 64 GB device. With multi-token prediction (MTP N=4), it generated **24.7–31.3 tokens/s** across seven prompt lengths, from 128 tokens to 128K.

## Test setup

| Item | Recorded configuration |
| --- | --- |
| Device | One GEEKOM A9 Mega 388 with 64 GB unified LPDDR5X memory |
| Processor and graphics | AMD Ryzen AI Max+ 388 with Radeon 8060S. [AMD specifications](https://www.amd.com/en/products/processors/laptop/ryzen/ai-300-series/amd-ryzen-ai-max-plus-388.html) |
| Software | Ubuntu 26.04, ROCm 10.0.0, Strata 0.2.2 |
| Model weights | SSD-resident GSQ-RCO-IQ3_S (83.6 GB on disk) |
| Acceleration settings | MTP N=4 and a baseline with MTP and suffix drafting both off |
| Context | `--max-context 256000` with an INT8 KV cache. Measurements cover 128 through 128K input tokens. |

Each acceleration setting has one recorded run per input length, for 14 measurements in total. [Strata project](https://github.com/Niko1221/Strata)

## IQ3_S results on the 64 GB 388

Decode measures generation speed, prefill measures prompt processing speed, and time to first token (TTFT) measures the wait from sending the request to receiving the first token. The baseline disables both MTP and suffix drafting.

| Input tokens | Decode, MTP N=4 (tok/s) | Decode, baseline (tok/s) | Prefill, MTP N=4 (tok/s) | TTFT, MTP N=4 (s) |
| --- | ---: | ---: | ---: | ---: |
| 128 | 31.3 | 23.6 | 77 | 1.69 |
| 4K | 28.4 | 22.4 | 516 | 7.97 |
| 8K | 28.4 | 23.4 | 524 | 15.67 |
| 16K | 30.0 | 24.1 | 611 | 26.85 |
| 32K | 30.6 | 23.8 | 648 | 50.60 |
| 64K | 24.7 | 23.2 | 644 | 101.80 |
| 128K | 24.9 | 22.5 | 629 | 208.42 |

At 128K, the MTP N=4 configuration decoded about **11% faster** than the baseline. With MTP N=4, generation stayed near 25 tokens/s at 64K and 128K, while the first-token wait grew from about **1 minute 42 seconds** to **3 minutes 28 seconds**.

## Single-device comparison with the 128 GB A9 Mega 395

The 64 GB 388 uses **Strata 0.2.2, GSQ-RCO-IQ3_S (83.6 GB), and MTP N=4**. The 128 GB 395 uses **`llama.cpp` (`b10909-mix-bea84f7`), UD-Q4_K_XL (111.4 GB), and MTP N=2**. The comparison covers all six input lengths measured on both single-device configurations. [A9 Mega 395 benchmark and launch command](../A9-Mega-395/README.md#31-qwen38-flash-next-ud-q4_k_xlgguf-1114gb-mtp-qwen38-flash-next-q4_k_mgguf-28gb)

| Input tokens | 388 decode (tok/s) | 395 decode (tok/s) | 388 TTFT (s) | 395 TTFT (s) |
| --- | ---: | ---: | ---: | ---: |
| 128 | 31.3 | 32.43 | 1.69 | 0.97 |
| 8K | 28.4 | 28.48 | 15.67 | 26.96 |
| 16K | 30.0 | 25.88 | 26.85 | 58.33 |
| 32K | 30.6 | 23.58 | 50.60 | 112.14 |
| 64K | 24.7 | 18.06 | 101.80 | 283.41 |
| 128K | 24.9 | 15.45 | 208.42 | 720.61 |

The 395 led on both metrics at 128 input tokens. At 8K, decode was nearly tied and the 388 returned the first token sooner. From 16K to 128K, the 388 led on both metrics at every shared input length. At 128K, it decoded **61% faster** and cut first-token wait by **71%** while using a machine with half the installed memory.

Hardware, quantization, engine, and MTP settings all vary between the two configurations. The measurements show how the complete setups performed. A separate evaluation would be needed to compare output quality.

## Full measurements and reproduction

The 388 archive includes generated token counts, end-to-end timings, VRAM and memory readings, and the original launch commands. [MTP N=4 run](./README.md#39-strata-ssd-resident-qwen38-flash-next-gsq-rco-iq3_sgguf-836-gb-mtp-n4) · [Baseline run](./README.md#310-strata-ssd-resident-qwen38-flash-next-gsq-rco-iq3_sgguf-836-gb-mtp-and-suffix-off) · [388 CSV](./test-records.csv) · [395 CSV](../A9-Mega-395/test-records.csv)
