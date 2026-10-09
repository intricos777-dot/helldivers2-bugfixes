# Crash Signatures

Community-verified crash patterns for Helldivers 2 on Linux (Proton), with the
evidence trail so the same signature can be recognised on other machines.

## Signature: NVRM `NV_ERR_NO_MEMORY` GPU system-memory crash

Originally verified: **2026-10-09**, Garuda Linux, Proton prefix
**GE-Proton10-34** (@ Steam appid 553850).

### Symptoms

- Game launches, loads every subsystem, then dies ~60–90 s in.
- Two identical crash dumps, a few seconds apart (re-launch → same crash).
- Kernel log shows NVIDIA driver OOM **on the same second as each crash**:

  ```
  nvidia_uvm: ... Out of memory [NV_ERR_NO_MEMORY] (0x51) from
      _memdescAllocInternal /system_mem.c ...
  nvidia ... uvm_...
  ```

- This is **GPU system memory (GTT)**: it is CPU-RAM-backed, so allocation
  fails when the whole machine is under physical-RAM pressure, even when the
  GPU has free VRAM.

### Dump signature (minidump parser output)

```
system : x64 ... cpus=12  win10.0.19045
modules: 83
exc 0x000002ac flags=0x0 addr=0x0000000000000000
threads: 27
```

- `exc 0x2AC` with `addr 0` and `RIP 0` = **engine-generated** handled crash
  (Arrowhead's writer stamps its own code), not a raw segfault.
- All subsystems loaded before death: `helldivers2.exe`, `data/game/game.dll`,
  `bin/libxess.dll` (XeSS), `bin/amd_fidelityfx_upscaler_dx12.dll` (FSR),
  `bin/plugins/wwise_pluginw64_release.dll` (audio), `bin/GameGuard/npsc64.des`
  (anti-cheat), `bin/PartyWin.dll`.
- Windows build string `10.0.19045` is normal (Proton reports Win10).

### Fixes / mitigations

1. **Give the OS enough pageable memory** (the direct cause):
   - ensure a swap/zram backing store exists so the kernel never starves a GTT
     allocation. On the validating machine: 32 GB swapfile + 7+ GB zram.
2. Reboot after enabling swap so the bad-pressure window is gone; re-test with
   `journalctl -k -b | grep -c NVRM` — expect 0 on a healthy run.
3. On NVIDIA: make sure the dGPU is used for rendering (PRIME offload):
   ```
   __NV_PRIME_RENDER_OFFLOAD=1 __VK_LAYER_NV_optimus=NVIDIA_only
   __GLX_VENDOR_LIBRARY_NAME=nvidia
   ```
4. Low-VRAM (4 GB) cards: disable **Dynamic Resolution**, keep the upscaler
   (XeSS/FSR) enabled — an upscaler reduces, not increases, memory pressure.
5. Keep driver up to date (`nvidia-open-dkms 615.78.08` was current on the
   validating machine).

### Known misdiagnoses

- "Reinstall the game" does not help (dumps prove it is memory allocation,
  not broken files).
- "Verify game integrity" does not help for the same reason.

## How to verify again

```
# 1) check kernel OOM lines vs crash timestamps
journalctl -k -b | grep -E "NVRM|nvrm.*Out of memory"

# 2) parse the game dump (see tools/)
python3 tools/mdump.py ".../crash_data/reports/<id>.dmp"
```