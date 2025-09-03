# Running the benchmark

## API keys

To use closed-source VLMs, you need to have an API key. To configure them, set appropriate variables in the
`.env` file.

## Running FlySearch

We present examples on how to run FlySearch benchmark in the `examples` directory.

- `mimic.sh` contains 3 examples of how to run different models on FS-1, FS-Anomaly-1 and FS-2.
- `create_new.sh` contains 3 examples of how to sample new scenarios from distribution of scenarios used in FS-1, FS-Anomaly-1 and FS-2. 
If you just want to test a model on our benchmark, we recommend using `mimic.sh`.


### Direct `drone.py` script usage

`drone.py` script is the entrypoint to run the benchmark. It has several configurable parameters. We explain them in the `tutorials/00-script.md` file.

### Models 

FlySearch supports testing several models. To test them, you can use on of our examples (discussed in the `Examples` section) and change the `model` parameter appropriately:
* OpenAI models. To use it, prefix your model argument with `oai-` and then use OpenAI's model name (e.g. `oai-gpt-4o`).
* Gemini family models (e.g. gemini-2.0-flash. To use it, set `model` flag to `gemini-2.0-flash`). Note that we use Gemini models using compatibility mode with OpenAI format -- as of now, this unfortunately tends to fail with Gemini 2.5 Pro. Pull requests fixing that issue are welcome.
* Anthropic models. To use it, prefix the model name with `anthropic-`, e.g. `anthropic-claude-3-5-sonnet-20241022`.
* Any models behind a VLLM API. If model name does not match any of the above, it is assumed to be a VLLM model. OpenAI protocol is used to communicate with the model. For example, to use Gemma3-27b hosted on [DeepInfra](https://deepinfra.com/), you need to configure `.env` file with `VLLM_ADDRESS = 'https://api.deepinfra.com/v1/openai'`, `VLLM_KEY` matching your DeepInfra API key, and set `model` to `google/gemma-3-27b-it`.

### Direct use of our environment (without code for benchmarking)

Our environment is based on Unreal Engine 5, and we provide a Gymnasium-like interface to it. It can be used directly without the rest of the code in this repository. See `tutorials/01-environment.md` for examples. 

## Result analysis

To read how to analyse logs from FlySearch, please see the `tutorials/02-result-analysis.md` file.

## Contributing support for unsupported models

See `tutorials/03-conversation.md`.

## Supporting new classes and assets 

See `tutorials/04-custom-assets.md`.

## Custom agents

See `tutorials/05-custom-agents.md`.

## Notes

### UE5 binary crashes 

The UE5 binary can sometimes spontaneously crash. The code is designed to handle this (we've modified UnrealCV's code to do so), but in case it happens you just need to restart the script with appropriately set `continue_from` flag. Furthermore, in case where your code was terminated by `UnrealDiedException` please open an issue here with a stack trace (or email us with it).