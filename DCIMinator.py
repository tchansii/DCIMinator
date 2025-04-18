import os
import shutil
import argparse
from PIL import Image
import pyheif
from tqdm import tqdm

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

def import_photos(source_dir, target_dir):
    os.makedirs(target_dir, exist_ok=True)

    # Collect all files first to track progress
    file_list = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_list.append(os.path.join(root, file))

    for source_file in tqdm(file_list, desc="Processing files"):
        ext = os.path.splitext(source_file)[1].lower()
        file_name = os.path.basename(source_file)

        # Normalize extensions: convert all .JPG/.JPEG to .jpg
        if ext in ['.jpg', '.jpeg']:
            normalized_file_name = file_name.lower()
            target_file = os.path.join(target_dir, normalized_file_name)
        else:
            target_file = os.path.join(target_dir, file_name)

        try:
            if ext in ['.jpg', '.jpeg', '.png']:
                shutil.copy2(source_file, target_file)
            elif ext == '.heic':
                convert_heic_to_jpg(source_file, target_file)
        except Exception as e:
            print(f"\n⚠️ Failed to process {file_name}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import iPhone photos and convert HEIC to JPG.")
    parser.add_argument("source_dir", help="Source directory (e.g. mounted DCIM folder)")
    parser.add_argument("target_dir", help="Target directory to store all images")

    args = parser.parse_args()

    import_photos(args.source_dir, args.target_dir)
