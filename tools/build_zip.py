import zipfile
import os
import argparse

def build(src_dir, out_zip):
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src_dir):
            for f in files:
                path = os.path.join(root, f)
                arc = os.path.relpath(path, src_dir)
                z.write(path, arc)
    print(f"Built {out_zip} ({os.path.getsize(out_zip)//1024//1024} MB)")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--src", default=".")
    p.add_argument("--out", default="genisys_linux_studio.zip")
    args = p.parse_args()
    build(args.src, args.out)
