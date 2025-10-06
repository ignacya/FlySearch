---
hide:
  - toc
---
# `flyserach.py` parameters

## Base options

```
 Usage: flysearch.py [OPTIONS] COMMAND [ARGS]...                                                                         
                                                                                                                         
 FlySearch benchmark                                                                                                     
                                                                                                                         
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --model-backend            [vllm|openai|anthropic|gemini]              The backend of the model to use [required]  │
│ *  --model-name               TEXT                                        The name of the model to use (passed to the │
│                                                                           model backend)                              │
│                                                                           [required]                                  │
│    --run-name                 TEXT                                        The name of the benchmark run (default to   │
│                                                                           date and time)                              │
│    --results-directory        PATH                                        The directory to store the experiment       │
│                                                                           results                                     │
│                                                                           [default: all_logs]                         │
│    --agent                    [simple_llm|description_llm|generalist_one  The type of agent to use (use default for   │
│                               |detection_driven_description_llm|detectio  oryginal FlySearch)                         │
│                               n_cheater_factory|parsing_error]            [default: simple_llm]                       │
│    --skip-sanity-check                                                    Whether to skip running a sanity check      │
│                                                                           before the benchmark (not recommended)      │
│    --number-of-runs           INTEGER                                     The number of runs to perform               │
│                                                                           [default: 300]                              │
│    --continue-from-idx        INTEGER                                     The index of the scenario to continue       │
│                                                                           running from (e.g. if execution was         │
│                                                                           interrupted)                                │
│                                                                           [default: 0]                                │
│    --log-level                [CRITICAL|ERROR|WARNING|INFO|DEBUG]         The level of logging to use [default: INFO] │
│    --help                                                                 Show this message and exit.                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ benchmark          Run a predefined benchmark set.                                                                    │
│ random-scenarios   Run FlySearch with random scenario generation.                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## benchmark command

Runs the predefined benchmark set, e.g. FS-1 or FS-2. Default scenario sets are located in the `run_templates`
directory. You can also create your own scenario sets from logs of any experiment, just copy the `scenario_params.json`
files and directory structure.

```                                                                                                                    
 Usage: flysearch.py benchmark [OPTIONS] SCENARIO_DIRECTORY                                                              
                                                                                                                         
 Run a predefined benchmark set.                                                                                         
                                                                                                                         
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    scenario_directory      PATH  The directory containing the scenarios to run the benchmark on [required]          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## random-scenarios command

Runs FlySearch with random scenario generation. You can specify the number of scenario profile and difficulty levels to use.
You can create new difficulty levels in `rl/evaluation/configs/difficulty_levels.py`.

```
 Usage: flysearch.py random-scenarios [OPTIONS] SCENARIO_TYPE:{city|forest|city_anomaly|forest_anomaly}
                                      DIFFICULTY:{fs1|fs2}                                                               
                                                                                                                         
 Run FlySearch with random scenario generation.                                                                          
                                                                                                                         
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    scenario_type      SCENARIO_TYPE:{city|forest|city_anomaly|fores  The type of scenario to generate [required]    │
│                         t_anomaly}                                                                                    │
│ *    difficulty         DIFFICULTY:{fs1|fs2}                           The difficulty of the scenario [required]      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```