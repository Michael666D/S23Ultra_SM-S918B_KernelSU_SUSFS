# Applying the overlay

Target starting point:
`WildKernels/Samsung_KernelSU_SUSFS@87a2cca5c6a4ac468446f3513119f95431dbee4a`

Copy the contents of this directory into the root of a branch based on that commit.

The overlay adds only:
- `.github/workflows/wildq-sm918b.yml`
- `.github/actions/wildq-*`
- `scripts/wildq_scan_image.py`
- manifests/docs

It intentionally leaves Wild's original workflows/actions untouched, because the experimental workflow reuses several audited local actions from the W0 commit.

Recommended Git history:
- `wildq/w0-audited-base`
- `wildq/w1-suki`
- `wildq/w2-suki-susfs`
- `wildq/w3-suki-susfs-kpm`

The current overlay allows W1/W2/W3 from one workflow input, but tags/commits should still be created for successful milestones.
