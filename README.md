# Run a Local AI Assistant on the GEEKOM A9 Mega

> **Project status: Draft / Technical validation**
>
> This repository is not ready for public release. Installation steps, model compatibility, and performance results are still being verified on physical GEEKOM hardware.

This project documents how to run and evaluate a browser-based local AI assistant on two configurations of the GEEKOM A9 Mega.

The initial validation uses Ollama and Open WebUI for local text-based chat. Installation steps shared by both configurations will be documented once, while hardware information and performance results will be recorded separately.

## What This Project Will Demonstrate

- Run a language model locally on a GEEKOM Mini PC.
- Access the assistant through a web browser on the same device.
- Compare one or two verified model configurations.
- Record model loading time, time to first token, generation speed, and memory usage.
- Explain known limitations and the conditions required for offline use.

## Validation Status

| Item | Status | Notes |
| --- | --- | --- |
| A9 Mega 388 configuration confirmed | Pending | Add exact processor, memory, storage, BIOS, and driver details. |
| A9 Mega 395 configuration confirmed | Pending | Add exact processor, memory, storage, BIOS, and driver details. |
| Operating system confirmed | Pending | Add the exact operating system edition, build, and update information. |
| Ollama version confirmed | Pending | Record the exact version used during testing. |
| Open WebUI version confirmed | Pending | Record the exact version and deployment method. |
| Primary model verified | Pending | Add the complete model tag, quantization, source, and license. |
| Secondary model verified | Pending | Include only if fully tested. |
| Installation reproduced | Pending | Confirm that the documented steps can be repeated. |
| Benchmark results reviewed | Pending | Publish the test conditions with the results. |
| Third-party licenses reviewed | Pending | Required before public release. |

## Tested Hardware

The initial validation covers two configurations of the GEEKOM A9 Mega. Hardware information and performance results will be recorded separately.

### GEEKOM A9 Mega — 388 Configuration

| Component | Tested configuration |
| --- | --- |
| Product | GEEKOM A9 Mega |
| Processor | To be confirmed |
| Graphics | To be confirmed |
| NPU | To be confirmed |
| Memory | To be confirmed |
| Storage | To be confirmed |
| Operating system | To be confirmed |
| BIOS | To be confirmed |
| Graphics/NPU driver | To be confirmed |
| Power profile | To be confirmed |

### GEEKOM A9 Mega — 395 Configuration

| Component | Tested configuration |
| --- | --- |
| Product | GEEKOM A9 Mega |
| Processor | To be confirmed |
| Graphics | To be confirmed |
| NPU | To be confirmed |
| Memory | To be confirmed |
| Storage | To be confirmed |
| Operating system | To be confirmed |
| BIOS | To be confirmed |
| Graphics/NPU driver | To be confirmed |
| Power profile | To be confirmed |

## Software Stack

| Component | Version | Source | License |
| --- | --- | --- | --- |
| Ollama | Pending | Pending | Pending |
| Open WebUI | Pending | Pending | Pending |
| Primary model | Pending | Pending | Pending |
| Secondary model | Pending | Pending | Pending |

Do not use `latest` as a version in the public guide. Record the exact application version, model tag, revision, and quantization used during testing.

## Quick Start

> This section will be completed after the setup has been reproduced and reviewed. Do not publish unverified commands.

The final quick start will cover:

1. Confirm the supported hardware and operating system.
2. Install the verified software versions.
3. Download the tested model configuration.
4. Start the local service.
5. Open the verified local address in a browser.

## Benchmark Methodology

The two configurations should use the same operating system, software versions, model versions, quantization settings, context length, test prompts, and measurement method wherever possible.

If any test condition differs, the difference must be disclosed with the corresponding result.

The first release will record:

- Model loading time
- Time to first token
- Generation speed in tokens per second
- Idle and peak memory usage
- CPU, GPU, and NPU utilization where measurable
- Model download size and total storage requirements

### Results

| Device configuration | Model | Quantization | Context | Load time | First token | Generation speed | Peak memory |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A9 Mega 388 | Pending | Pending | Pending | Pending | Pending | Pending | Pending |
| A9 Mega 395 | Pending | Pending | Pending | Pending | Pending | Pending | Pending |

Results from one configuration should not be presented as guaranteed performance for every GEEKOM configuration. Background applications, software versions, model settings, ambient conditions, and power profiles can affect performance.

## Offline-Use Note

Local operation does not automatically mean that every installation step works offline. Models, software, dependencies, and required resources must be downloaded and configured before the device is disconnected from the internet.

The final guide will identify any feature that still requires an online service.

## Known Limitations

This section will be completed after testing. It will cover only verified limitations, including:

- Maximum tested context length
- Memory constraints
- First-run download requirements
- Features that require internet access
- Unsupported operating system or driver versions
- Setup steps that require manual intervention

## Troubleshooting

The public version will cover only issues actually encountered during validation, including the observed error, cause, fix, and affected software version.

## Validation Principles

- Results from different hardware configurations will be reported separately.
- Performance results will include the relevant test conditions and measurement method.
- Hardware acceleration will be described only when it has been verified.
- Commands and scripts will be published only after they have been reproduced and reviewed.
- Third-party model files will not be uploaded unless their licenses and redistribution terms have been confirmed.

## Responsible Use and Support

This is an experimental reference project, not a guarantee that every model or third-party application will work on every configuration. Model outputs may be inaccurate. Do not use generated output as the sole basis for medical, legal, financial, safety-critical, or other high-impact decisions.

Support scope and issue-response expectations will be added before public release.

## Related Resources

- [GEEKOM Resource Center](https://github.com/GEEKOMOfficial/geekom-resource-center)
- [GEEKOM Official Website](https://www.geekompc.com/)
- [GEEKOM Support](https://www.geekompc.com/support/)

## Third-Party Software and Models

This project may reference third-party open-source software and AI models. Their names and trademarks belong to their respective owners. Applicable licenses and original project sources will be identified before public release.
