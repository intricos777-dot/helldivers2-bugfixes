# Minidump reader (community crash-analysis tool)

Minimal dependency-free Python reader for the Windows minidumps Helldivers 2
drops when it crashes. Extracts:

- header / system info
- exception code, address, thread context RIP/RSP
- loaded module list (so you can map fault addresses to game/DLLs)

## Usage

```
python3 tools/mdump.py path/to/dump-*.dmp
```

## Where the game writes dumps

Under the Proton prefix:

```
.../steamapps/compatdata/553850/pfx/drive_c/users/steamuser/AppData/Roaming/
    Arrowhead/Helldivers2/crash_data/reports/*.dmp      ← full dumps
    Arrowhead/Helldivers2/dumps/*.dmp                   ← game-writer dumps
    Arrowhead/Helldivers2/crash_data/metadata           ← ids the game uploads
```

`metadata` tells you the crash ids already sent to Arrowhead:
- `localId` / `uuid` and one line per dump file.

## Reading a result

- `exc 0x........` — the exception code. Windows codes you care about:
  - `0xC0000005` access violation
  - `0xC00000FD` stack overflow
  - `0x887A00..` DXGI error codes (device removed / out of video memory)
  - `0x8007000E` DirectX "not enough memory"
- `RIP / RSP` — instruction + stack pointer of the crashing thread's context.
- Module names show whether the process died in the engine (`game.dll`),
  an upscaler (`libxess.dll`, `amd_fidelityfx_upscaler_dx12.dll`), audio
  (`wwise_pluginw64_release.dll`), anti-cheat (`GameGuard/npsc64.des`), etc.

See [CRASH_SIGNATURES.md](../CRASH_SIGNATURES.md) for the signatures recorded
so far.