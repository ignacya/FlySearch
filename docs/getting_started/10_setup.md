# Setup

## Requirements

Requirements for running the benchmark are described below. Note that these are only requirements for running the benchmark; if you want to rebuild the environments, you may need additional dependencies for Unreal Engine 5 development.

This does not include requirements for running local LLMs, as these depend on the model you want to run. 

### Hardware

We recommend using a machine with at least 32GB of RAM and a modern CPU (e.g. AMD Ryzen 7 5800X3D or Intel i7 13700K). A ray-tracing capable GPU is required to run the Unreal Engine 5 (UE5) binaries. We've tested the benchmark on NVIDIA RTX 4060 and 4080 GPUs, as well NVIDIA A100. Vulkan drivers need to be installed for the GPU to work with UE5.

### Operating system

We've verified that the benchmark works on Ubuntu 22.04, Archlinux (2025), and Rocky Linux 9.6, but it should work on any modern Linux distribution.

Unreal Engine 5 supports Windows and MacOS as well, but we haven't tested the benchmark on these operating systems, nor provide compiled binaries for them. You will need to compile the UE5 environments yourself if you want to run the benchmark on Windows or MacOS.

## Python environment 

We suggest you use Python 3.12 and then install dependencies using uv - pyproject and uv.lock files provided. Just use `uv run <script name>`.

## Config `.env` file 

Before proceeding, you need to create a `.env` file in the root directory of this repository. We've provided a template for it in the file `.env-example`. In other words, you should run:

```bash 
cp .env-example .env
```

You will need to edit the `.env` file so that it contains your local variables (such as paths to binaries, fonts, etc.). We will describe the variables you need to set below.

### Benchmark binaries

Binaries cam be downloaded from https://doi.org/10.5281/zenodo.15428224.

`city.tar.gz` contains the city environment and
`forest.tar.gz` contains the forest environment. Extract them and then modify the `.env` file by:

* setting the `CITY_BINARY_PATH` to `/your_location/simulator/CitySample/Binaries/Linux/CitySample`
* setting the `FOREST_BINARY_PATH` to `your_location/simulator-dreamsenv/Linux/ElectricDreamsEnv/Binaries/Linux/ElectricDreamsSample`
* setting path where logs from binaries themselves should be stored (`UNREAL_LOG_PATH`) to `"/path_to_repo/FlySearch/unreal_logs"` (or wherever else you want -- the directory will be created automatically, defaults to project root if not set)

You can also verify manually that these work on your computer by
running `./simulator/CitySample/Binaries/Linux/CitySample` or
`./simulator-dreamsenv/Linux/ElectricDreamsEnv/Binaries/Linux/ElectricDreamsSample`. These commands should start the UE5
environment in interactive mode and show it on your screen. Note, that objects will not be spawned until you run the benchmark code or run low level command yourself.

### City locations

The file `locations_city.csv` is provided with this repository. Set the `LOCATIONS_CITY_PATH` variable in the `.env` file to location of this file in your filesystem; this file is important for running city scenarios, as it contains permissible safe locations for objects to be spawned.

### Fonts

The benchmark needs a font to overlay images from the engine with a navigation scaffold. Set the `FONT_LOCATION` variable in the `.env` file to the location of a font file in your filesystem. The default one is `/usr/share/fonts/google-noto/NotoSerif-Bold.ttf`, which may or may not be present on your machine.
