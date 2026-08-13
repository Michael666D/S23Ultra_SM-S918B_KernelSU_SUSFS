# Known limitations / unresolved evidence

1. Exact qlenlen KernelPatch/KPIMG commit is not yet proven.
2. W3 uses SukiSU_patch commit `547ae94...` as a pinned candidate patcher, not as a claim that it is byte-identical to qlenlen's patcher.
3. W2/W3 SUSFS supplemental commits are still selected by Wild's original 87a2cca SUSFS action. The workflow logs the resulting commit so it can be frozen after the first run.
4. `kernel_patches` pin `f569cc9...` is a W0-era candidate. Confirm against Build #657 diagnostics if available.
5. External GitHub Actions `endersonmenezes/free-disk-space@v3`, `thejerrybao/setup-swap-space@v1`, `actions/checkout@v5`, and `actions/upload-artifact@v6` are version tags, not immutable SHAs. Freeze these after the first successful CI run.
6. Firmware AP/BL/CP/CSC/security-patch identity remains a pre-flash requirement.
7. No claim is made that W3 boots until it has actually completed boot and hardware validation.
