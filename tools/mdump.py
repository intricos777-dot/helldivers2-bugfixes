#!/usr/bin/env python3
"""Minimal Windows minidump reader: header, streams, exception, modules, sysinfo."""
import struct
import sys

MDMP = 0x504D444D
T_EXCEPTION, T_MODULE, T_SYSTINFO, T_THREAD = 6, 4, 7, 3


def read(path):
    data = open(path, "rb").read()
    sig, ver, nstreams, dir_rva, _, ts, flags = struct.unpack_from("<IIIIIii", data, 0)
    print(f"file   : {path}")
    print(f"sig    : 0x{sig:08x}  ver: 0x{ver:08x}  streams: {nstreams}  flags: 0x{flags:08x}")
    if sig != MDMP:
        print("NOT a minidump"); return
    streams = {}
    for i in range(nstreams):
        t, size, rva = struct.unpack_from("<III", data, dir_rva + i * 12)
        streams[t] = (rva, size)

    if T_SYSTINFO in streams:
        rva, _ = streams[T_SYSTINFO]
        arch, level, rev, ncpu, ptype, maj, minor, build, plat = struct.unpack_from("<HHHBBIIII", data, rva)
        arch_s = {0:"x86",5:"ARM",6:"IA64",9:"x64",12:"ARM64"}.get(arch, f"0x{arch:x}")
        print(f"system : {arch_s} level {level} rev 0x{rev:x}  cpus={ncpu}  win{maj}.{minor}.{build}")

    modules = []
    if T_MODULE in streams:
        rva, size = streams[T_MODULE]
        count = struct.unpack_from("<I", data, rva)[0]
        off = rva + 4
        for _ in range(count):
            base, siz, _, _, name_rva, *_ = struct.unpack_from("<QIIII", data, off)
            nlen = struct.unpack_from("<I", data, name_rva)[0]
            name = data[name_rva + 4: name_rva + 4 + nlen * 2].decode("utf-16-le", "replace")
            modules.append((base, siz, name))
            off += 108
        print(f"modules: {len(modules)}")

    def module_for(addr):
        for base, siz, name in modules:
            if base <= addr < base + siz:
                return name
        return "???"

    if T_EXCEPTION in streams:
        rva, _ = streams[T_EXCEPTION]
        code, flags_, rec, addr, _nparams = struct.unpack_from("<IIQQI", data, rva)
        print(f"exc 0x{code:08x} flags=0x{flags_:x} addr=0x{addr:016x}")
        if addr:
            print(f"     faulting module: {module_for(addr)}")
            for base, siz, name in modules:
                if base <= addr < base + siz:
                    print(f"     offset 0x{addr-base:x} in {name}")
                    break
        ctx_rva = rva + 160  # x64: ExceptionRecord(152) + ThreadId(4) + pad(4)
        try:
            ctx = struct.unpack_from("<II", data, ctx_rva)
            rip = struct.unpack_from("<Q", data, ctx_rva + 0x110)[0]
            rsp = struct.unpack_from("<Q", data, ctx_rva + 0x98)[0]
            print(f"     RIP=0x{rip:016x} RSP=0x{rsp:016x}")
            mods = [m for m in modules if m[0] <= rip < m[0] + m[1]]
            if mods:
                base, _, name = mods[0]
                print(f"     executing module: {name} (off 0x{rip - base:x})")
            else:
                print(f"     executing module: ??? (unmapped)")
        except Exception as e:
            print(f"     (context parse: {e})")
    else:
        print("no exception stream")


    # threads w/ first frames
    if T_THREAD in streams:
        rva, size = streams[T_THREAD]
        count = struct.unpack_from("<I", data, rva)[0]
        print(f"threads: {count}")
    for base, siz, name in sorted(modules, key=lambda m: -m[1])[:12]:
        print(f"  mod 0x{base:016x} {siz:>8x}  {name}")

for p in sys.argv[1:]:
    print("=" * 78)
    read(p)