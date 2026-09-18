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

## General

- Reinstall the game if crashes persist (last resort)
- Update GPU drivers to latest stable
- Close background applications that use GPU (browser, streaming software)
- Check CPU temps — high temps cause crashes during combat
