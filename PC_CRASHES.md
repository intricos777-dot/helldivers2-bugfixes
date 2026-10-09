# PC Crash Fixes

## Verified Fixes

### 1. Dynamic Resolution
**Symptom:** Instant crash on launch or during gameplay.
**Fix:** Disable Dynamic Resolution in graphics settings.
```
Settings → Graphics → Dynamic Resolution → OFF
```

### 2. E-cores in BIOS
**Symptom:** Crashes, stutter, freezing on Intel hybrid CPUs.
**Fix:** Re-enable Efficiency Cores (E-cores) in BIOS.
```
BIOS → CPU Configuration → E-cores → Enabled
```
Note: Some users had previously disabled E-cores for compatibility with another game.

### 3. Permissions/Access
**Symptom:** Crashes after update, especially on first launch.
**Fix:** Right-click game in Steam → Properties → Local Files → Verify integrity.
Then ensure the game has read/write permissions to its install directory.

### 4. Re-apply permissions every update
**Symptom:** Crashes return after each patch.
**Fix:** After every update, re-verify game files and re-apply any permission overrides.

### 5. NVIDIA driver "Out of memory" crash ~60–90 s after launch (Linux/Proton)
**Symptom:** Game loads fully, then dies once or twice a minute in; `journalctl -k`
shows `nvidia_uvm ... Out of memory [NV_ERR_NO_MEMORY]` on the same second as each crash.
**Cause:** GPU system-memory (GTT) allocation failure under physical-RAM pressure —
not VRAM, not broken files. Dumps show the engine's own handled crash (`exc 0x2AC`).
**Fix:**
1. Add a swap/zram backing store; reboot; verify next boot with
   `journalctl -k -b | grep -c NVRM` (expect 0).
2. Enforce dGPU rendering on NVIDIA hybrid systems (PRIME offload), see
   [CRASH_SIGNATURES.md](CRASH_SIGNATURES.md).
3. On low-VRAM (4 GB) cards, disable Dynamic Resolution and keep XeSS/FSR on.
4. Keep the driver updated.

Full evidence, dump signature, and re-verification steps:
[CRASH_SIGNATURES.md](CRASH_SIGNATURES.md) · [tools/](tools/README.md)

## General

- Reinstall the game if crashes persist (last resort)
- Update GPU drivers to latest stable
- Close background applications that use GPU (browser, streaming software)
- Check CPU temps — high temps cause crashes during combat
