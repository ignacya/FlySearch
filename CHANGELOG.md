# Change Log
All notable changes to this project will be documented in this file.

## v1.1.0
- Update prompts for GPT-5: contrary to previous models, GPT-5 attempts to
return multiple actions in one response (not a repeated output, but intentional
behaviour consisted with reasoning output), a line was added to prompt to
explicitly forbid this, should not affect other LLMs.
- Verified support for GPT-5, Claude 4.5, and Gemini 2.5.
- New benchmark template execution code, now works with partial sessions with
missing episodes.
- Template naming consistency (remove _r0 suffix).

## v1.0.0
- NeurIPS camera ready version.
- CLI re-written in Typer.
- Replaced conda with uv package manager
- Auto-download unreal engine binaries
- Overall project refactor and cleanup

## v0.0.1
- First fully-functional version