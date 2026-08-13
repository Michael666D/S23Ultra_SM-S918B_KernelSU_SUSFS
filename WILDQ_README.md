# WildQ-KPM scaffold v0.1 — SM-S918B / dm3q / Kalama

This overlay is designed for a fork of:

- `WildKernels/Samsung_KernelSU_SUSFS`
- audited base commit: `87a2cca5c6a4ac468446f3513119f95431dbee4a`

It does **not** modify Wild's original workflows. It adds a separate experimental workflow:

`.github/workflows/wildq-sm918b.yml`

## Milestones

- **W1** — pinned Samsung source + SukiSU only (`CONFIG_KSU_SUSFS=n`, `CONFIG_KPM=n`).
- **W2** — W1 + Wild's SUSFS kernel-side integration.
- **W3** — W2 + `CONFIG_KPM` source-side API + one Suki KernelPatch post-build injection.

No NoMount, ZeroMount, BBG, BBRv3, NTsync, Droidspaces or optimization pack is added in W1-W3. Those come only after W3 boots and KPM is verified.

## Why this shape

The known-good Wild build and the known-good qlenlen KPM build both boot on the SM-S918B, but they differ in kernel version/toolchain/root stack. W1-W3 keep the Wild Samsung 5.15/Clang-14/Full-LTO/CFI baseline and change the root stack incrementally.

The qlenlen KPM binary contains the Suki string:

`v4.1.3-b1d534bc@builtin`

so this scaffold pins SukiSU to:

`b1d534bc41941b2c818d7a1a1dac341e4aabfc2d`

## Double-KernelPatch guard

W3 deliberately distinguishes:

1. **Suki source-side KPM API** — expected **before** post-build patching.
2. **KernelPatch core** — must be absent before post-build patching.

Pre-patch:
- `KernelPatch Version` = 0
- `KernelPatch Config` = 0
- `sukisu_handle_kpm` >= 1
- `SUKISU_KPM_LOAD` >= 1

Post-patch:
- `KernelPatch Version` = 1
- `KernelPatch Config` = 1
- Suki KPM API still present

If KernelPatch is already present before the patch step, the build aborts instead of patching twice.

## Canonical Image

Wild's original `ak3zip-prep` searches heuristically for an Image and copies it before exporting the path. WildQ instead:

`Bazel build -> locate canonical Image -> validate -> KPM (W3 only) -> stage same canonical Image -> ZIP`

This prevents patching Image A and accidentally packaging Image B.

## Important limitation in v0.1

W2/W3 initially reuse Wild's audited `susfs-patches` action from the `87a2cca` base. That action fetches Simonpunk/Pershoot branches dynamically. The workflow records the exact resulting SUSFS HEAD/history in the diagnostics artifact.

Once the first successful W2/W3 run is available, those exact SUSFS commits should be frozen in v0.2. Do **not** call v0.1 perfectly reproducible with respect to SUSFS supplemental commits.

## Use

1. Fork `WildKernels/Samsung_KernelSU_SUSFS`.
2. Create a branch from commit `87a2cca5c6a4ac468446f3513119f95431dbee4a`.
3. Copy this overlay into that branch preserving paths.
4. Commit and push.
5. In Actions run **WildQ SM-S918B W1-W3** with `W1`.
6. Review diagnostics before considering any flash.
7. Only after W1 is understood, run W2; then W3.

This package itself does not flash the phone.

## First-flash rule

Before flashing any experimental ZIP keep:
- the known-good Wild ZIP,
- the known-good qlenlen KPM ZIP,
- original/known-good boot material,
- Odin firmware/recovery path appropriate for the installed firmware.

A compilation success is not a boot-success claim.

## v0.1 safety corrections

- W1 explicitly disables `CONFIG_KSU_SUSFS`. In the pinned Suki revision this option defaults to `y`, so leaving it implicit would contaminate W1 or cause missing-SUSFS compile errors.
- The workflow aborts before compilation if any unresolved `.rej` file remains after patch application.
