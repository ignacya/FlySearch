#!/usr/bin/env python3
import argparse
import json
import os
import shutil
from pathlib import Path
from PIL import Image

# Headless rendering for matplotlib
import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt

# Ensure analysis import works when run from project root or web/
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from analysis.run import Run
from analysis.run_visualiser import RunVisualiser


def generate_preview(episode_dir: Path, out_file: Path) -> None:
    run = Run(episode_dir)
    visualiser = RunVisualiser(run)
    fig = plt.figure(figsize=(8, 6), dpi=150)
    ax = fig.add_subplot(projection='3d')
    visualiser.plot(ax)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_file, format='jpg', bbox_inches='tight')
    plt.close(fig)


def copy_file_if_exists(src: Path, dst: Path) -> bool:
    if src.exists() and src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return True
    return False


def convert_png_to_jpg(src: Path, dst: Path) -> bool:
    """Convert a PNG image to JPEG while copying.

    If the PNG has an alpha channel, composite onto a white background.
    Returns True on success, False otherwise.
    """
    if not src.exists() or not src.is_file():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        with Image.open(src) as img:
            # Handle transparency by compositing onto white background
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                rgba = img.convert("RGBA")
                background = Image.new("RGB", rgba.size, (255, 255, 255))
                background.paste(rgba, mask=rgba.split()[-1])
                img_to_save = background
            else:
                img_to_save = img.convert("RGB")
            img_to_save.save(dst, format="JPEG", quality=90, optimize=True)
        return True
    except Exception as e:
        print(f"[WARN] Failed to convert {src} to JPEG: {e}")
        return False


def export_episode(run_dir: Path, episode_name: str, out_dir: Path) -> None:
    episode_dir = run_dir / episode_name
    target_dir = out_dir / run_dir.name / episode_name
    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy scenario params
    copy_file_if_exists(episode_dir / 'scenario_params.json', target_dir / 'scenario_params.json')

    # Prefer conversation.json, fallback to simple_conversation.json
    if not copy_file_if_exists(episode_dir / 'conversation.json', target_dir / 'conversation.json'):
        copy_file_if_exists(episode_dir / 'simple_conversation.json', target_dir / 'conversation.json')

    # Convert and copy all PNGs as JPGs (images like 0.png -> 0.jpg)
    for item in os.listdir(episode_dir):
        if item.lower().endswith('.png'):
            src_png = episode_dir / item
            dst_jpg = target_dir / f"{Path(item).stem}.jpg"
            convert_png_to_jpg(src_png, dst_jpg)

    # Generate preview.jpg
    try:
        generate_preview(episode_dir, target_dir / 'preview.jpg')
    except Exception as e:
        print(f"[WARN] Failed to generate preview for {episode_dir}: {e}")


def build_index(log_dir: Path) -> dict:
    index = {"runs": []}
    for run_name in sorted([d.name for d in log_dir.iterdir() if d.is_dir()]):
        run_dir = log_dir / run_name
        episodes = sorted([d.name for d in run_dir.iterdir() if d.is_dir()])
        index["runs"].append({"name": run_name, "episodes": episodes})
    return index


def main():
    parser = argparse.ArgumentParser(description='Export static data for the web client')
    parser.add_argument('--log-dir', type=str, required=True, help='Base LOG_DIR containing runs with episodes')
    parser.add_argument('--out-dir', type=str, default=str(PROJECT_ROOT / 'web' / 'client' / 'public' / 'data'),
                        help='Output directory for exported static data (served under /data)')
    parser.add_argument('--clean', action='store_true', help='Remove existing out-dir before export')
    args = parser.parse_args()

    log_dir = Path(args.log_dir).resolve()
    out_dir = Path(args.out_dir).resolve()

    if args.clean:
        shutil.rmtree(out_dir, ignore_errors=True)

    out_dir.mkdir(parents=True, exist_ok=True)

    # Build index
    index = build_index(log_dir)

    # Export each episode
    for run in index["runs"]:
        run_dir = log_dir / run["name"]
        for episode in run["episodes"]:
            export_episode(run_dir, episode, out_dir)

    # Write index.json
    with open(out_dir / 'index.json', 'w') as f:
        json.dump(index, f, indent=2)

    print(f"Export complete. Static data written to: {out_dir}")


if __name__ == '__main__':
    main()
