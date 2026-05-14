#!/usr/bin/env python3
"""Split a binary file into base64 chunks and reconstruct it."""
import argparse, base64, hashlib, json, math, os, sys

CHUNK_SIZE = 500_000  # bytes per chunk (~667KB base64)


def split(src: str, out_dir: str, chunk_size: int = CHUNK_SIZE) -> None:
    os.makedirs(out_dir, exist_ok=True)
    with open(src, "rb") as f:
        data = f.read()

    total = len(data)
    n_chunks = math.ceil(total / chunk_size)
    sha256 = hashlib.sha256(data).hexdigest()

    manifest = {
        "filename": os.path.basename(src),
        "size": total,
        "sha256": sha256,
        "chunk_size": chunk_size,
        "n_chunks": n_chunks,
        "chunks": [],
    }

    for i in range(n_chunks):
        chunk = data[i * chunk_size : (i + 1) * chunk_size]
        b64 = base64.b64encode(chunk).decode()
        name = f"chunk_{i:04d}.b64"
        path = os.path.join(out_dir, name)
        with open(path, "w") as f:
            f.write(b64)
        manifest["chunks"].append({"index": i, "file": name, "size": len(chunk)})
        print(f"  wrote {name} ({len(chunk):,} bytes → {len(b64):,} b64 chars)")

    manifest_path = os.path.join(out_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nSplit {total:,} bytes into {n_chunks} chunks → {out_dir}/")
    print(f"SHA-256: {sha256}")


def join(chunk_dir: str, out_path: str) -> None:
    manifest_path = os.path.join(chunk_dir, "manifest.json")
    with open(manifest_path) as f:
        manifest = json.load(f)

    parts = []
    for chunk in sorted(manifest["chunks"], key=lambda c: c["index"]):
        path = os.path.join(chunk_dir, chunk["file"])
        with open(path) as f:
            b64 = f.read().strip()
        parts.append(base64.b64decode(b64))
        print(f"  read {chunk['file']} ({chunk['size']:,} bytes)")

    data = b"".join(parts)
    sha256 = hashlib.sha256(data).hexdigest()

    if sha256 != manifest["sha256"]:
        print(f"ERROR: SHA-256 mismatch!\n  expected: {manifest['sha256']}\n  got:      {sha256}", file=sys.stderr)
        sys.exit(1)

    with open(out_path, "wb") as f:
        f.write(data)

    print(f"\nReconstructed {len(data):,} bytes → {out_path}")
    print(f"SHA-256 verified: {sha256}")


def main():
    parser = argparse.ArgumentParser(description="Chunk/dechunk binary files via base64")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("split", help="Split file into chunks")
    sp.add_argument("src", help="Source file")
    sp.add_argument("out_dir", help="Output directory for chunks")
    sp.add_argument("--chunk-size", type=int, default=CHUNK_SIZE,
                    help=f"Bytes per chunk (default {CHUNK_SIZE:,})")

    jp = sub.add_parser("join", help="Reconstruct file from chunks")
    jp.add_argument("chunk_dir", help="Directory containing chunks and manifest.json")
    jp.add_argument("out_path", help="Output file path")

    args = parser.parse_args()
    if args.cmd == "split":
        split(args.src, args.out_dir, args.chunk_size)
    else:
        join(args.chunk_dir, args.out_path)


if __name__ == "__main__":
    main()
