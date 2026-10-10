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

### 6. GameGuard black-screen crash on launch (Linux/Proton)
**Symptom:** GameGuard splash appears, then the game hangs on a black screen and exits.
Every attempt leaves a fresh `NxStorage_<date>_<time>_helldivers2.txt` in the game root
containing the line:
```
Can't get volume for mount point 'Z:\home\'.
```
and a new `dumps/dump-<date>-<time>-*-zero-41.dmp`.
**Cause:** GameGuard (nProtect) runs a storage/volume check at init and cannot resolve
the Wine `Z:` drive (`Z:` → `/` in the Proton prefix). This is a Proton/Wine-side
regression in resolving the `Z:\home` mount point, not a game or a hardware bug.
**Fix:** Force the game to use **Proton Hotfix** (or **Proton Experimental**) — these
builds carry the Wine fix for the `Z:` mount resolution. Do not run this title under a
custom/older GE-Proton build.
```
Steam → HELLDIVERS 2 → Properties → Compatibility → Force the use of a specific
Steam Play compatibility tool → Proton Hotfix
```
**Verify:** after relaunch, no new `NxStorage_*.txt` is written and the game passes the
GameGuard splash into the main menu.

Source: Steam Community HELLDIVERS 2 support thread, "Stopped working on Linux"
(https://steamcommunity.com/app/553850/discussions/1/833872096657427188/) — same error
text and the Proton Hotfix/Experimental fix; corroborated by the CachyOS forum report of
the black screen past GameGuard under Proton 10.

Full evidence, dump signature, and re-verification steps:
[CRASH_SIGNATURES.md](CRASH_SIGNATURES.md) · [tools/](tools/README.md)

## General

- Reinstall the game if crashes persist (last resort)
- Update GPU drivers to latest stable
- Close background applications that use GPU (browser, streaming software)
- Check CPU temps — high temps cause crashes during combat

### 7.0.2 "Devoid of Liberty" crash fixes (server-side, patch 25 Aug 2026) — confirmed
Arrowhead fixed these at patch level. No community patch required:

1. Crash while browsing the Vehicle Customization menu
2. Crash in Dynamic Resolution Scaling
3. Crashes during Message of the Day

Source: SteamDB patchnotes 24826606, https://steamdb.info/patchnotes/24826606/

### Terminal / superwide-window crash hotfix (server-side)
A Steam hotfix targets crashes when using intercoms/terminals and on superwide (e.g. 32:9)
windowed setups. This is a server-side fix; no client config change is required. Confirmed
on the Steam app hub & PC support thread (https://steamcommunity.com/app/553850/discussions/1/).
