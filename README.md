<p style="text-align: center">
  <a href="https://arxiv.org/abs/2506.02896">
    <img src="docs/imgs/logo.jpg" width="50%" alt="FlySearch" />
  </a>
</p>

---

# FlySearch: Exploring how vision-language models explore

A benchmark for evaluating vision-language models in simulated 3D, outdoor, photorealistic environments. Easy for humans, hard for state-of-the-art VLMs / MLLMs.

### [Leaderboard & Docs](https://flysearch.pardyl.com/) | [Paper](https://arxiv.org/abs/2506.02896)

## Abstract 

The real world is messy and unstructured. Uncovering critical information often requires active, goal-driven exploration. It remains to be seen whether Vision-Language Models (VLMs), which recently emerged as a popular zero-shot tool in many difficult tasks, can operate effectively in such conditions. In this paper, we answer this question by introducing FlySearch, a 3D, outdoor, photorealistic environment for searching and navigating to objects in complex scenes. We define three sets of scenarios with varying difficulty and observe that state-of-the-art VLMs cannot reliably solve even the simplest exploration tasks, with the gap to human performance increasing as the tasks get harder. We identify a set of central causes, ranging from vision hallucination, through context misunderstanding, to task planning failures, and we show that some of them can be addressed by finetuning. We publicly release the benchmark, scenarios, and the underlying codebase.


## Dependencies

### Hardware

We recommend using a machine with at least 32GB of RAM and a modern CPU (e.g. AMD Ryzen 7 5800X3D or Intel i7 13700K). A ray-tracing capable GPU is required to run the Unreal Engine 5 (UE5) binaries. We've tested the benchmark on NVIDIA RTX 4060 and 4080 GPUs, as well NVIDIA A100. Vulkan drivers need to be installed for the GPU to work with UE5. Make sure you have at least 60GB free storage space (preferable SSD or RAM-cached HDD).

### Operating system

We've verified that the benchmark works on Ubuntu 22.04, Archlinux (2025), and Rocky Linux 9.6, but it should work on any modern Linux distribution.

Unreal Engine 5 supports Windows and MacOS as well, but we haven't tested the benchmark on these operating systems, nor provide compiled binaries for them. You will need to compile the UE5 environments yourself if you want to run the benchmark on Windows or MacOS.

### Python environment 

We suggest you use Python 3.12 and then install dependencies using uv (https://docs.astral.sh/uv/) - it will automatically install all requirements when first running FlySearch.

### `.env` file 

Before proceeding, you need to create a `.env` file in the root directory of this repository. We've provided a template for it in the file `.env-example`. In other words, you should run:

```bash 
cp .env-example .env
```

You will need to edit the `.env` file so that it contains your local variables (e.g. API keys and URLs).

### Benchmark binaries

FlySearch will automatically download Unreal Engine binaries on Linux. We do not provide pre-compiled simulator for other platforms, so you will need to build it yourself (see documentation).


## Running FlySearch

You can run FlySearch using 
```
uv run flysearch.py --model-backend <name of model backend> --model-name <model name string> benchmark <scenario template set>
```
Scenario sets are located in the run_templates directory

See `uv run flyserach.py --help` for a list of all options.

More details in the documentation.

## Result analysis

To read how to analyse logs from FlySearch, please see the documentation.


## Notes

### UE5 binary crashes 

The UE5 binary can sometimes spontaneously crash, usually when generating new scenarios. The code is designed to handle this (we've modified UnrealCV's code to do so), but in case it happens you just need to restart the script with appropriately set `continue_from_idx` flag. Furthermore, in case where your code was terminated by `UnrealDiedException` please open an issue here with a stack trace (or email us with it).

## License and legal

Our benchmark code is released under the MIT License.

FlySearch uses Unreal® Engine. Unreal® is a trademark or registered trademark of Epic Games, Inc. in the United States of America and elsewhere. See Unreal Engine EULA for more information [https://www.unrealengine.com/en-US/eula/unreal](https://www.unrealengine.com/en-US/eula/unreal).


## Citation
If you use FlySearch in your research, please cite the following paper:

```
@misc{pardyl2025flysearch,
  title={FlySearch: Exploring how vision-language models explore},
  author={Adam Pardyl and Dominik Matuszek and Mateusz Przebieracz and Marek Cygan and Bartosz Zieliński and Maciej Wołczyk},
  year={2025},
  eprint={2506.02896},
  archivePrefix={arXiv},
  primaryClass={cs.CV},
  url={https://arxiv.org/abs/2506.02896}, 
}
```
