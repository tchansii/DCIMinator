# 📸 DCIMinator

*A simple tool for taming iPhone and iPad media imports on Linux.*

So you've plugged your iPhone or iPad into your Linux machine and found yourself staring into the abyss of the `DCIM` folder. Subfolders inside subfolders, `.HEIC` files, `.MOV`s, and filenames like `IMG_9384.JPG`.

**DCIMinator** is here to help you import photos and videos in a clean and human way.

---

## 💾 What It Does

- Recursively imports photos and videos from iOS-style `DCIM` folders
- Converts `.HEIC` images to `.JPG`
- Converts `.MOV` videos to `.MP4` (unless you ask nicely not to)
- Normalizes file extensions (e.g., `.JPG` → `.jpg`)
- Shows progress bars and spinner animations so you know it’s alive
- Offers flags so you can control exactly what you want to import or convert

---

## 🛠️ Requirements

You'll need a few system libraries first. Just run:

```bash
sudo apt install libheif1 libheif-dev ffmpeg
```

Then clone this repo and set up your Python environment.

---

## 🐍 Setup (with a virtual environment)

I recommend using a virtual environment so your dependencies stay clean.

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

> You can exit the venv anytime with `deactivate`.

---

## ▶️ Usage

Once your venv is active, run the script like this:

```bash
python3 DCIMinator.py <source_dir> <target_dir> [flags]
```

For example:

```bash
python3 DCIMinator.py ~/Documents/DCIM ~/Pictures/DCIMinated --include-videos
```

---

## 🏳️ Available Flags

| Flag               | What it does                                                                 |
|--------------------|------------------------------------------------------------------------------|
| `--keep-heic`       | Keep `.HEIC` images instead of converting to `.JPG`                         |
| `--include-videos`  | Include video files in the import                                           |
| `--keep-mov`        | Keep `.MOV` format instead of converting to `.MP4` (requires `--include-videos`) |
| `--verbose-ffmpeg`  | Show full ffmpeg logs instead of using a spinner during conversion          |

⚠️ If you use `--keep-mov` **without** `--include-videos`, you’ll get a warning (and no MOVs will be copied).

---

## 🧼 Example

```bash
python3 DCIMinator.py /media/iPhone/DCIM ~/ImportedPhotos \
  --include-videos \
  --keep-heic \
  --verbose-ffmpeg
```

---

## ❤️ Philosophy

I don’t hate Apple. I just think that if we can land robots on Mars, maybe dragging your vacation pics onto your Linux desktop shouldn’t feel like spelunking in digital cave systems.

DCIMinator doesn't reinvent the wheel—it just makes the wheel roll a little smoother for folks outside the orchard.

---