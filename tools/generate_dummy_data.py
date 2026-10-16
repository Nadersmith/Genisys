# Generates dummy binary file of specified size for packaging (use to reach 100MB)
import os
import argparse

def gen(path, size_mb):
    total = size_mb * 1024 * 1024
    with open(path, "wb") as f:
        chunk = b"\x00" * 1024 * 1024
        for i in range(size_mb):
            f.write(chunk)
    print(f"Wrote {path} ({size_mb} MB)")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="samples/dummy.bin")
    p.add_argument("--mb", type=int, default=120)
    args = p.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    gen(args.out, args.mb)
