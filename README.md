# Run a Local AI Chatbot on the GEEKOM A9 Mega

> **Project status: Draft / Internal validation**  
> This repository is not ready for public release. The setup, model compatibility, and benchmark results are still being verified on physical GEEKOM hardware.

This project documents how to run a browser-based local AI chatbot on the **GEEKOM A9 Mega**. The final guide will include a reproducible Windows setup, verified model configurations, measured performance, and troubleshooting notes.

## What this project will demonstrate

- Run an AI language model locally on a GEEKOM Mini PC.
- Access the chatbot through a web browser on the same device.
- Compare one or two verified model configurations.
- Record installation time, model loading time, response latency, generation speed, and memory usage.
- Explain known limitations and the conditions required for offline use.

## Validation status

| Item | Status | Notes |
|---|---|---|
| Hardware configuration confirmed | Pending | Add exact A9 Mega SKU and memory/storage configuration. |
| Windows environment confirmed | Pending | Add Windows build, BIOS, and driver versions. |
| Local inference framework selected | Pending | Add exact name and version after technical review. |
| Browser interface selected | Pending | Add exact name and version after technical review. |
| Primary model verified | Pending | Add model repository, revision, quantization, and license. |
| Secondary model verified | Pending | Optional; include only if fully tested. |
| Clean installation reproduced twice | Pending | QA must complete two independent runs. |
| Benchmark results reviewed | Pending | Publish raw conditions together with results. |
| Third-party licenses reviewed | Pending | Required before public release. |

## Tested hardware

Complete this section using the final QA record. Do not combine results from different configurations.

| Component | Tested configuration |
|---|---|
| Product | GEEKOM A9 Mega |
| Processor | AMD Ryzen AI Max 388 **or** Ryzen AI Max+ 395 — confirm tested SKU |
| Graphics | To be confirmed |
| NPU | To be confirmed |
| Memory | To be confirmed |
| Storage | To be confirmed |
| Operating system | To be confirmed |
| BIOS | To be confirmed |
| Graphics/NPU driver | To be confirmed |
| Power profile | To be confirmed |

## Software stack

| Component | Version | Source | License |
|---|---|---|---|
| Inference framework | Pending | Pending | Pending |
| Browser UI | Pending | Pending | Pending |
| Primary model | Pending | Pending | Pending |
| Secondary model | Pending | Pending | Pending |

Do not use `latest` as a version in the public guide. Record the exact application version, model revision, and quantization used during testing.

## Quick start

> This section must be completed by the technical maintainer after the setup has been reproduced. Do not publish unverified commands.

The final quick start should contain no more than five main steps:

1. Confirm the supported hardware and Windows version.
2. Download or run the verified installer.
3. Download the tested model configuration.
4. Start the local service.
5. Open the verified local URL in a browser.

## Benchmark methodology

All published results must identify the tested hardware, model, quantization, context length, prompt, power profile, software versions, and whether the result was measured during a cold or warm run.

Planned measurements:

- Total installation time
- Model download size
- Cold model loading time
- Time to first token
- Generation speed in tokens per second
- Idle and peak memory usage
- CPU, GPU, and NPU utilization where measurable
- Temperature and stability during a 30-minute session
- Behavior after a Windows restart
- Behavior without internet access after all required resources are installed

### Results

| Model | Quantization | Context | Load time | First token | Generation speed | Peak memory |
|---|---:|---:|---:|---:|---:|---:|
| Pending | Pending | Pending | Pending | Pending | Pending | Pending |

Results from one configuration should not be presented as guaranteed performance for every A9 Mega configuration. Background applications, software versions, model settings, ambient conditions, and power profiles can affect performance.

## Offline-use note

Local operation does not automatically mean that every installation step works offline. Models, software, dependencies, and required resources must be downloaded and configured before the device is disconnected from the internet. The final guide must identify any feature that still requires an online service.

## Known limitations

Complete this section after testing. At minimum, document:

- Model-specific accuracy and hallucination limitations
- Maximum tested context length
- Memory constraints
- First-run download requirements
- Features that require internet access
- Unsupported Windows or driver versions
- Any setup step that still requires manual intervention

## Troubleshooting

The public version should cover only issues actually encountered during validation, including the observed error, cause, fix, and affected software version.

## Project structure

```text
.
├── README.md
├── THIRD_PARTY_NOTICES.md
├── docs/
│   ├── qa-handoff-template.md
│   └── publishing-checklist.md
├── scripts/                 # Added by the technical maintainer after validation
└── assets/                  # Approved screenshots and demo media
```

## Responsible use and support

This is an experimental reference project, not a guarantee that every model or third-party application will work on every configuration. Model outputs may be inaccurate. Do not use generated output as the sole basis for medical, legal, financial, safety-critical, or other high-impact decisions.

Support scope and issue-response expectations will be added before public release.

## About GEEKOM

GEEKOM designs Mini PCs for work, creation, entertainment, and emerging local AI workflows. Learn more at [geekompc.com](https://www.geekompc.com/).

<!-- Add the campaign-specific UTM link and promotional code only after internal approval. -->

