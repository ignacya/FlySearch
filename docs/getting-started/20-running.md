# Running the benchmark

## Setup
If you haven't done so already, please follow the instructions in the [Setup](../getting-started/10-setup.md) section.

## Running FlySearch

You can run FlySearch using 
```
uv run flysearch.py --model-backend <name of model backend> --model-name <model name string> benchmark <scenario template set>
```
Scenario sets are located in the run_templates directory

See `uv run flyserach.py --help` for a list of all options.

### Models 

FlySearch supports testing several model backends. Set the `--model-backend` and `--model-name` parameters appropriately:
* OpenAI models - `--model backend=openai`.
* Gemini family models (e.g. gemini-2.0-flash) - `--model-backend gemini`. Note that we use Gemini models using compatibility mode with OpenAI format -- as of now, this unfortunately tends to fail with Gemini 2.5 Pro. Pull requests fixing that issue are welcome.
* Anthropic models - `--model-backend antropic`.
* Any models behind a OpenAI/VLLM API - `--model-backend vllm`. OpenAI protocol is used to communicate with the model. For example, to use Gemma3-27b hosted on [DeepInfra](https://deepinfra.com/), you need to configure `.env` file with `VLLM_ADDRESS = 'https://api.deepinfra.com/v1/openai'`, `VLLM_KEY` matching your DeepInfra API key, and set `--model-name` to `google/gemma-3-27b-it`.

## Result analysis

FlySearch prints out basic statistics to the console, but more detailed logs are stored in JSON format in the `logs` directory.
To read how to analyse logs from FlySearch, please see the [result-analysis](../user-guide/20-result-analysis.md).

## Adding support for new models

Out of the box, FlySearch supports any OpenAI API compliant model. If you need to use other API standards, you can implement a new conversation class - see [conversation](../user-guide/10-conversation.md).

## Custom agents

If you want to implement a new agent behaviour (for example, one that uses multiple models), you can do so by implementing a new agent class.
See [custom-agents](../user-guide/30-custom-agents.md).

## Supporting new classes, assets and environments

See [internals](../internals/30-custom-environments.md) documentation.

## Direct use of our environment (without code for benchmarking)

Our environment is based on Unreal Engine 5, and we provide a Gymnasium-like interface to it. It can be used directly without the rest of the code in this repository. See [environment](../internals/10-environment.md) for examples.

## Notes

### UE5 binary crashes 

The UE5 binary can sometimes spontaneously crash. The code is designed to handle this (we've modified UnrealCV's code to do so), but in case it happens you just need to restart the script with appropriately set `continue_from` flag. Furthermore, in case where your code was terminated by `UnrealDiedException` please open an issue here with a stack trace (or email us with it).