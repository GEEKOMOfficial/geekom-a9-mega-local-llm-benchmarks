# QA Handoff Template

Complete one copy of this template for each clean installation run.

## 1. Test identity

- Test date:
- Tester:
- Test run: Run 1 / Run 2
- Overall result: Pass / Pass with limitations / Fail

## 2. Hardware and operating environment

- GEEKOM product and exact SKU:
- CPU:
- GPU:
- NPU:
- Installed memory:
- Allocated graphics memory, if configured:
- SSD model and capacity:
- Windows edition and build:
- BIOS version:
- Graphics driver version:
- NPU driver version:
- Power mode/profile:
- Ambient temperature:
- Background applications closed before testing:

## 3. Software and model versions

- Inference framework and version:
- Browser interface and version:
- Primary model repository URL:
- Model revision/commit:
- Model file and quantization:
- Model file size:
- Model license:
- Secondary model, if tested:

## 4. Installation record

- Clean environment confirmed: Yes / No
- Installation start time:
- Ready-to-chat time:
- Total installation time:
- Manual steps not covered by the script:
- Internet connection required for:
- Errors encountered:
- Relevant log filenames:

## 5. Functional verification

- Local browser UI opens successfully: Yes / No
- Ten fixed prompts completed: Yes / No
- Responses completed without interruption: Yes / No
- Service works after Windows restart: Yes / No
- Installed model works after internet is disconnected: Yes / No / Partially
- Stop procedure works: Yes / No
- Uninstall procedure works: Yes / No

Attach the fixed prompts and unedited model responses. Do not report answer quality without preserving the original prompts, settings, and outputs.

## 6. Performance record

- Cold model load time:
- Warm model load time:
- Time to first token:
- Generation speed:
- Idle memory usage:
- Peak memory usage:
- CPU utilization:
- GPU utilization:
- NPU utilization:
- Maximum observed temperature:
- 30-minute stability result:
- Measurement tool and version:

## 7. Evidence checklist

- [ ] System information screenshot
- [ ] Software version screenshots
- [ ] Installation screenshots
- [ ] Browser UI screenshot
- [ ] Performance measurement screenshots
- [ ] Full demonstration recording
- [ ] Installation and runtime logs
- [ ] Error screenshots and logs

Remove user names, serial numbers, internal network addresses, tokens, passwords, API keys, and other sensitive information before sharing the package.

## 8. Issues and limitations

For each issue, record:

1. Exact symptom or error message
2. Steps to reproduce
3. Affected version
4. Suspected cause
5. Workaround or fix
6. Whether the fix was retested

## 9. QA conclusion

- Recommended for public release: Yes / No / After fixes
- Blocking issues:
- Non-blocking limitations:
- Steps in the guide that need clarification:

