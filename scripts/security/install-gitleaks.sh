#!/bin/sh
# Verified upstream release; install only to a caller-selected local directory.
set -eu
destination=${1:?Usage: install-gitleaks.sh destination-directory}
case "$(uname -s)/$(uname -m)" in
  Darwin/arm64) platform=darwin_arm64; checksum=b40ab0ae55c505963e365f271a8d3846efbc170aa17f2607f13df610a9aeb6a5 ;;
  Linux/x86_64) platform=linux_x64; checksum=551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb ;;
  *) echo 'Unsupported platform; install verified Gitleaks 8.30.1 manually.' >&2; exit 2 ;;
esac
temporary=$(mktemp -d)
trap 'rm -rf "$temporary"' EXIT HUP INT TERM
curl --fail --silent --show-error --location --proto '=https' --tlsv1.2 \
  "https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_${platform}.tar.gz" \
  --output "$temporary/release.tar.gz"
python3 - "$temporary/release.tar.gz" "$checksum" <<'PY'
import hashlib, sys
from pathlib import Path
if hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest() != sys.argv[2]:
    sys.exit('Gitleaks checksum mismatch; installation refused')
PY
tar -xzf "$temporary/release.tar.gz" -C "$temporary" gitleaks
mkdir -p "$destination"
install -m 700 "$temporary/gitleaks" "$destination/gitleaks"
