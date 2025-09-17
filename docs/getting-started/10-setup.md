# Setup

## Requirements

Requirements for running the benchmark are described below. Note that these are only requirements for running the benchmark; if you want to rebuild the environments, you may need additional dependencies for Unreal Engine 5 development.

This does not include requirements for running local LLMs, as these depend on the model you want to run. 

### Hardware

* CPU: any modern x64 CPU (e.g. AMD Ryzen 7 5800X3D or Intel i7 13700K)
* RAM: at least 32GB of RAM (64GB recommended).
* GPU: ray-tracing capable GPU is required (tested on NVIDIA RTX 4060 and 4080 GPUs, as well NVIDIA A100). Vulkan drivers need to be installed for the GPU to work with UE5.
* Storage: At least 60GB of free storage. SSD strongly recommended.

### Operating system

We've verified that the benchmark works on Ubuntu 22.04, Archlinux (2025), and Rocky Linux 9.6, but it should work on any modern Linux distribution.

Unreal Engine 5 supports Windows and macOS as well, but we haven't tested the benchmark on these operating systems, nor provide compiled binaries for them. You will need to compile the UE5 environments yourself if you want to run the benchmark on Windows or macOS.

## Python environment 

We suggest you use Python 3.12 and then install dependencies using [uv](https://docs.astral.sh/uv/getting-started/installation/). Pyproject and uv lock files are provided. Just run `uv sync` in the main directory. For additional capabilities run `uv sync --all-extras`

## Config `.env` file 

Before proceeding, you need to create a `.env` file in the root directory of this repository. We've provided a template for it in the file `.env-example`. In other words, you should run:

```bash 
cp .env-example .env
```

You will need to edit the `.env` file so that it contains your local variables (such as paths to binaries, fonts, etc.). We will describe the variables you need to set below.

### Model keys and URLs

To evaluate models using FlySearch, you will need to provide API keys (`OPEN_AI_KEY`, `GEMINI_AI_KEY`, `ANTHROPIC_AI_KEY`, `VLLM_KEY`) and URLs (`VLLM_ADDRESS`) where applicable. You can get these keys by signing up on the respective platforms. If you are using a local LLM, you may not need any keys.

### Optional settings

#### Benchmark binaries

Binaries will be automatically downloaded from https://doi.org/10.5281/zenodo.15428224 to `SIMULATOR_PATH` (defaults to `project_root/simulator`). If you want to change this location, set the `SIMULATOR_PATH` variable in the `.env` file to your desired location.

Alternatively, you can download the binaries yourself from the above or build them yourself (see build documentation). In this case, you will need to set the following variables in the `.env` file:

* set the `CITY_BINARY_PATH` to `your_location/CitySample/Binaries/Linux/CitySample`
* set the `FOREST_BINARY_PATH` to `your_location/ElectricDreamsEnv/Binaries/Linux/ElectricDreamsSample`

You can also verify manually that these work on your computer by
running `./CitySample/Binaries/Linux/CitySample` or
`./ElectricDreamsEnv/Binaries/Linux/ElectricDreamsSample`. These commands should start the UE5
environment in interactive mode and show it on your screen. Note, that objects will not be spawned until you run the benchmark code or run low level command yourself, you can exit the simulator with Alt-F4.

#### Debug logs
The path where logs from engine should be stored are set with `UNREAL_LOG_PATH` (defaults to root of repo).

#### City locations

The file `locations_city.csv` is provided with this repository and automatically detected. You can override it by setting the `LOCATIONS_CITY_PATH` variable in the `.env` file. This file is important for running city scenarios, as it contains permissible safe locations for objects to be spawned.

#### Fonts

The benchmark needs a font to overlay images from the engine with a navigation scaffold. It will attempt to auto-detect the location of `NotoSerif-Bold.ttf` font. You may need to override the location with the `FONT_LOCATION` variable in the `.env` file to the location of a font file in your filesystem if auto-detection fails.
