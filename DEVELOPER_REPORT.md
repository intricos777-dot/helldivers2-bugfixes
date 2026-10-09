# Developer Report — HD2 crash on NVIDIA (GPU system-memory OOM) under Proton

> Copy-paste ready for Arrowhead support (https://arrowhead.zendesk.com) or the
> public issue tracker. Field placeholders are marked `[REPLACE]`.
>
> Not affiliated with Arrowhead. No copyrighted assets included in this repo.

## Summary

Helldivers 2 (Steam appid 553850) under Proton crashes ~60–90 s after launch.
The crash coincides, to the second, with NVIDIA kernel-driver OOM allocating
**GPU system memory (GTT, CPU-RAM-backed)** under physical-RAM pressure. Two
consecutive launches produced two identical dumps. The crash feed was already
uploaded automatically (ids below).

## Environment

- OS: Garuda Linux (Arch), kernel `7.2.9-zen1-1-zen`
- Driver: `nvidia-open-dkms 615.78.08` (open kernel modules)
- GPU: NVIDIA GeForce [REPLACE model] 4 GB VRAM
- Proton prefix: `GE-Proton10-34` (Steam compatibility tool)
- RAM: [REPLACE total] GB physical
- Game build: `[REPLACE]` (see `crash_data/metadata` version fields)

## Repro

1. Launch HD2 from Steam (Proton).
2. Load into the ship.
3. Crash within ~60–90 s (two attempts, same result).

## Evidence

Crash ids (uploaded by the game's crash feed):

```
localId: 15123643
uuid   : 17e4dfe5-8c44-44b3-90fc-606973637034
dumps  : e754c302-bbbd-42e1-bbd4-dd1750dbcda4.dmp   (15:32:02)
         67378ef1-f085-48e0-97b3-bfa5e81dc12f.dmp   (15:32:42)
```

Kernel log (each ``Out of memory`` lands on the same second as a dump):

```
15:32:04 nvidia_uvm: ... Out of memory [NV_ERR_NO_MEMORY] (0x51)
         from _memdescAllocInternal, system_mem.c ...
15:32:43 nvidia_uvm: ... Out of memory [NV_ERR_NO_MEMORY] (0x51) ...
```

Minidump signature (see tools/mdump.py):

```
system : x64 ... cpus=12 win10.0.19045
modules: 83
exc 0x000002ac flags=0x0 addr=0x0000000000000000
threads: 27
```

- `exc 0x2AC`, `addr 0`, `RIP 0` → engine-generated handled crash (custom writer).
- Loaded modules at death include `helldivers2.exe`, `data/game/game.dll`,
  `bin/libxess.dll` (XeSS), `bin/amd_fidelityfx_upscaler_dx12.dll` (FSR),
  `bin/plugins/wwise_pluginw64_release.dll`, `bin/GameGuard/npsc64.des`,
  `bin/PartyWin.dll`.

## Likely cause (our view)

D3D12/texture streaming request for GPU system memory (GTT) fails with
`NV_ERR_NO_MEMORY` because the allocation is backed by physical RAM and the
machine was under pressure. The handshake that follows (engine sees a failed
allocation) ends in the handled crash that produced both dumps. Adding a
large swap backing store and rebooting eliminated the failure on the
reporting machine — consistent with a RAM-pressure trigger rather than a
game-code defect.

## Request

- Confirm from these ids whether the failure is a lost device / failed
  GTT allocation on the render or streaming thread.
- Consider succeeding the GTT allocation gracefully (retry / lower the
  streaming budget) when `cudaMallocManaged`-style system-memory fails.

## Thanks

Happy to re-run with debug builds or GStreamer/`NV_DEBUG` logs if your team
wants more.