import os
import platform
import tarfile
import urllib.request
from pathlib import Path

import typer
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)


def download_with_progress(url, filepath):
    with Progress(
            TextColumn("[bold blue]{task.description}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("Downloading", total=None)

        def reporthook(block_num, block_size, total_size):
            if total_size > 0:
                progress.update(task, total=total_size)
            progress.update(task, advance=block_size)

        urllib.request.urlretrieve(url, filepath, reporthook=reporthook)


def extract_tar_gz(file_path: str, output_dir: str):
    file_path = Path(file_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with Progress(
            TextColumn("[bold blue]{task.description}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task(
            f"Extracting", total=None
        )
        with tarfile.open(file_path, "r:gz") as tar:
            members = tar.getmembers()
            total_size = sum(m.size for m in members if m.isreg())
            progress.update(task, total=total_size)

            for member in members:
                tar.extract(member, output_dir)
                if member.isreg():
                    progress.update(task, advance=member.size)


def get_city_env_binary():
    return _get_unreal_binary(
        env_variable_name="CITY_BINARY_PATH",
        linux_exec_path="Linux/CitySample/Binaries/Linux/CitySample",
        linux_download_url="https://zenodo.org/records/15428224/files/City.tar.gz?download=1",
        name="City",
    )


def get_forest_env_binary():
    return _get_unreal_binary(
        env_variable_name="FOREST_BINARY_PATH",
        linux_exec_path="Linux/ElectricDreamsEnv/Binaries/Linux/ElectricDreamsSample",
        linux_download_url="https://zenodo.org/records/15428224/files/Forest.tar.gz?download=1",
        name="Forest",
    )


def _get_unreal_binary(
        env_variable_name: str, linux_exec_path: str, linux_download_url: str, name: str
):
    # Check if environment variable is defined and not empty
    env_path = os.getenv(env_variable_name)
    if env_path:
        if os.path.isfile(env_path):
            return env_path
        else:
            raise FileNotFoundError(
                f"Simulator binary not found at path specified by {env_variable_name}: {env_path}"
            )

    # Check if platform is Linux

    if platform.system() != "Linux":
        raise OSError(
            f"Automatic binary download is only supported on Linux. "
            f"Please manually set the {env_variable_name} environment variable "
            f"to point to your Unreal Engine binary."
        )

    # Get store path from SIMULATOR_PATH env variable or use default
    store_path = os.getenv("SIMULATOR_PATH")
    if not store_path:
        # Default to project_root/simulator
        project_root = Path(__file__).parent.parent
        store_path = str(project_root / "simulator")

    store_path = os.path.join(store_path, name)

    # Check if binary exists in store path
    binary_path = os.path.join(store_path, linux_exec_path)
    if os.path.isfile(binary_path):
        return binary_path

    # Binary not found, ask user if they want to download

    print(f"Unreal Engine binary not found at {binary_path}")
    print(
        "The binary is approximately 20GB in size, unpacking it will require twice that amount of space"
    )
    print(
        f"We will download it to: {store_path}, if you want to change this, set the SIMULATOR_PATH environment variable."
    )

    response = typer.confirm("Would you like to download the Unreal Engine binary?")

    if not response:
        raise FileNotFoundError(
            f"Unreal Engine binary not found and download declined. "
            f"Please set {env_variable_name} environment variable or place binary at {binary_path}"
        )

    # Create store directory if it doesn't exist
    Path(store_path).mkdir(parents=True, exist_ok=True)

    # Download and extract with progress bar
    print(f"Downloading Unreal Engine binary from {linux_download_url}...")
    tar_path = os.path.join(store_path, "temp_download.tar.gz")

    try:
        download_with_progress(linux_download_url, tar_path)

        print("Download complete. Extracting...")

        extract_tar_gz(tar_path, store_path)

        # Clean up temporary file
        os.remove(tar_path)
        print("Extraction complete.")

        # Verify the binary exists after extraction
        if os.path.isfile(binary_path):
            return binary_path
        else:
            raise FileNotFoundError(
                f"Binary not found at expected location after extraction: {binary_path}"
            )

    except Exception as e:
        # Clean up on failure
        if os.path.exists(tar_path):
            os.remove(tar_path)
        raise RuntimeError(f"Failed to download or extract Unreal Engine binary: {e}")
