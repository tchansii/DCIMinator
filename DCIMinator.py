import os
import shutil
import argparse
from PIL import Image
import pyheif
from tqdm import tqdm
import subprocess
from yaspin import yaspin

def convert_heic_to_jpg(heic_path, output_path):
    heif_file = pyheif.read(heic_path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    jpg_path = os.path.splitext(output_path)[0] + '.jpg'
    image.save(jpg_path, "JPEG")

def convert_mov_to_mp4(mov_path, output_path, verbose=False):
    command = [
        "ffmpeg",
        "-i", mov_path,
        "-vcodec", "libx264",
        "-acodec", "aac",
        "-y",
        output_path
    ]

    file_name = os.path.basename(mov_path)

    if verbose:
        tqdm.write(f"🎞️  Converting {file_name} to MP4 (verbose)...")
        subprocess.run(command)
    else:
        with open(os.devnull, 'w') as devnull:
            with yaspin(text=f"🎞️  Converting {file_name}", color="cyan", timer=True) as spinner:
                result = subprocess.run(command, stdout=devnull, stderr=devnull)
                if result.returncode == 0:
                    spinner.ok("✅")
                else:
                    spinner.fail("💥")
                    raise subprocess.CalledProcessError(result.returncode, command)


def import_photos(source_dir, target_dir, keep_heic=False, include_videos=False, keep_mov=False, verbose_ffmpeg=False):
    os.makedirs(target_dir, exist_ok=True)

    file_list = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_list.append(os.path.join(root, file))

    for source_file in tqdm(file_list, desc="Processing files"):
        ext = os.path.splitext(source_file)[1].lower()
        file_name = os.path.basename(source_file)

        # Normalize .jpg/.jpeg to lowercase
        if ext in ['.jpg', '.jpeg']:
            normalized_file_name = file_name.lower()
            target_file = os.path.join(target_dir, normalized_file_name)
        else:
            target_file = os.path.join(target_dir, file_name)

        try:
            if ext in ['.jpg', '.jpeg']:
                shutil.copy2(source_file, target_file)

            elif ext == '.heic':
                if keep_heic:
                    shutil.copy2(source_file, target_file)
                else:
                    convert_heic_to_jpg(source_file, target_file)

            elif ext == '.mov' and include_videos:
                    if keep_mov:
                        shutil.copy2(source_file, target_file)
                    else:
                        mp4_target = os.path.splitext(target_file)[0] + '.mp4'
                        convert_mov_to_mp4(source_file, mp4_target, verbose=verbose_ffmpeg)

        except Exception as e:
            print(f"\n⚠️ Failed to process {file_name}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DCIMinator: Import iPhone photos with options.")
    parser.add_argument("source_dir", help="Source directory (e.g. mounted DCIM folder)")
    parser.add_argument("target_dir", help="Target directory to store all images")

    parser.add_argument("--keep-heic", action="store_true", help="Don't convert HEIC files to JPG")
    parser.add_argument("--include-videos", action="store_true", help="Include .MOV videos in import")
    parser.add_argument("--keep-mov", action="store_true", help="Keep .MOV videos as-is (only applies if --include-videos is set)")
    parser.add_argument("--verbose-ffmpeg", action="store_true", help="Show full ffmpeg output (default is silent)")

    args = parser.parse_args()

    if args.keep_mov and not args.include_videos:
        print("⚠️  Warning: --keep-mov has no effect unless --include-videos is also set.")
        print("    If you want to import .MOV files, use --include-videos too.\n")

    if args.verbose_ffmpeg and not args.include_videos:
        print("⚠️  Warning: --verbose-ffmpeg has no effect unless --include-videos is also set.")
        print("    If you want to convert .MOV files with ffmpeg, use --include-videos too.\n")


    import_photos(
        args.source_dir,
        args.target_dir,
        keep_heic=args.keep_heic,
        include_videos=args.include_videos,
        keep_mov=args.keep_mov,
        verbose_ffmpeg=args.verbose_ffmpeg,
    )
