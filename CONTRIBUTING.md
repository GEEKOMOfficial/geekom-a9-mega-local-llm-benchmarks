# Contributing

Thanks for your interest in this data set. It exists to be checked — reproductions, disagreements and additional data points are all welcome.

## Reproducing a result

Every record in `docs/` ships with the model file name, the launch command and the device (395 or 388) it was measured on. To reproduce:

1. Match the recorded environment as closely as you can (ROCm version, OS, model file and quant).
2. Run the same command and compare decode speed (tok/s), TTFT and memory readings.
3. If your numbers differ, open an issue (see below) — differences are data too.

## Reporting a reproduction or discrepancy

Open a GitHub Issue and include:

- Device and configuration (CPU, RAM, BIOS version if known)
- Model file (exact name and quant) and where you got it
- The exact launch command
- Your measured decode speed / TTFT / memory, and the record you compared against
- OS and ROCm / driver versions

We review new issues on business days and prioritise complete reports.

## Submitting your own measurements

Measured on an A9 Mega (or another Strix Halo machine) and want your run included? Open an issue with the same fields as above, plus the full output log. Submissions are reviewed against the same standard as our own records: measured on real hardware, reproducible, and reported with their limitations — slow and failed runs included.

## Citing this data

The benchmark data and documentation in this repository are licensed under CC BY 4.0 (the same terms as the [dataset release](https://huggingface.co/datasets/geekom-ai/a9-mega-local-llm-benchmarks)). Please cite with a link to the specific file you used. Code is under the MIT License (see LICENSE).
