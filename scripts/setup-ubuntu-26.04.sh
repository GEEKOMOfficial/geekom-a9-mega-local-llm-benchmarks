#!/usr/bin/env bash
set -euo pipefail

# Prepares a native Ubuntu 26.04 A9 Mega host for the recorded ROCm 10.0.0 setup.
# AMD specifies the Ubuntu inbox kernel driver for supported Ryzen APUs.
ROCM_INSTALLER_URL='https://repo.radeon.com/rocm/installer/rocm-runfile-installer/rocm-rel-10.0/rocm-installer-10.0.0-4.run'
INSTALL_ROCM=1
if [[ ${1:-} == --skip-rocm ]]; then INSTALL_ROCM=0
elif [[ $# -ne 0 ]]; then echo "Usage: $0 [--skip-rocm]" >&2; exit 2
fi

source /etc/os-release
[[ ${ID:-} == ubuntu && ${VERSION_ID:-} == 26.04 ]] || {
  echo 'This script requires native Ubuntu 26.04.' >&2; exit 1;
}
[[ $(uname -m) == x86_64 ]] || { echo 'x86_64 is required.' >&2; exit 1; }
if grep -qi microsoft /proc/version; then
  echo 'Use a native Ubuntu installation for the recorded A9 Mega setup, not WSL.' >&2; exit 1
fi

sudo apt-get update
sudo apt-get install -y build-essential ca-certificates cmake curl git python3 python3-venv pciutils tar

repo_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
python3 -m venv "$repo_dir/.venv"
"$repo_dir/.venv/bin/python" -m pip install --upgrade 'huggingface_hub[hf_xet]>=0.34,<2'

echo 'Detected display adapters:'
lspci | grep -Ei 'VGA|Display|3D' || true

if (( INSTALL_ROCM )); then
  if { [[ -f /opt/rocm/.info/version ]] && grep -q '^10\.0\.0' /opt/rocm/.info/version; } || \
     { [[ -f /opt/rocm/core-10.0.0/.info/version ]] && grep -q '^10\.0\.0' /opt/rocm/core-10.0.0/.info/version; }; then
    echo 'ROCm 10.0 appears installed; skipping installer.'
  else
    installer_dir=$(mktemp -d)
    trap 'rm -rf "$installer_dir"' EXIT
    installer="$installer_dir/rocm-installer-10.0.0-4.run"
    echo "Downloading AMD ROCm 10.0.0 installer: $ROCM_INSTALLER_URL"
    curl --fail --location --retry 5 --output "$installer" "$ROCM_INSTALLER_URL"
    installer_version=$(bash "$installer" version)
    echo "$installer_version"
    [[ $installer_version == *10.0.0* ]] || { echo 'Unexpected ROCm installer version.' >&2; exit 1; }
    # The APU uses Ubuntu's inbox kernel driver; do not replace it with amdgpu DKMS.
    (cd "$installer_dir" && bash "$installer" deps=install compo=core-sdk rocm gpu-access=user)
    echo 'Log out and back in for GPU group access; reboot if the installer requests it.'
  fi
fi

if command -v rocminfo >/dev/null 2>&1; then
  rocminfo | grep -m1 -E 'gfx1151|gfx1150' || echo 'Check rocminfo: expected a supported Radeon 8060S GPU.'
fi
echo 'Ubuntu preparation complete. Run download-models.py and download-llama-cpp.py next.'
