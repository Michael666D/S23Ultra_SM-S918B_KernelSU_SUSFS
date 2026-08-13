#!/usr/bin/env python3
import argparse, hashlib, json, re
from pathlib import Path

MARKERS = [
    "KernelPatch Version",
    "KernelPatch Config",
    "sukisu_handle_kpm",
    "sukisu_is_kpm_control_code",
    "ksu_kpm_cmd",
    "sukisu_kpm_control",
    "sukisu_kpm_info",
    "sukisu_kpm_list",
    "sukisu_kpm_version",
    "SUKISU_KPM_LOAD",
    "SUKISU_KPM_UNLOAD",
    ".kpm.init",
    ".kpm.exit",
    "bypass_kcfi",
    "__cfi_slowpath",
    "__cfi_slowpath_diag",
    "report_cfi_failure",
    "SUSFS",
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--output")
    args = ap.parse_args()
    p = Path(args.image)
    b = p.read_bytes()
    strings = [x.decode("latin1", "ignore") for x in re.findall(rb"[\x20-\x7e]{5,}", b)]
    banner = next((s for s in strings if s.startswith("Linux version ") and len(s) > 30), None)
    builtins = [s for s in strings if "@builtin" in s and s.startswith("v")][:20]
    out = {
        "path": str(p.resolve()),
        "size": len(b),
        "sha256": hashlib.sha256(b).hexdigest(),
        "kernel_banner": banner,
        "builtin_version_strings": builtins,
        "marker_counts": {m: b.count(m.encode()) for m in MARKERS},
    }
    text = json.dumps(out, indent=2, ensure_ascii=False)
    print(text)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
