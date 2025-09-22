import os
import sys
from pathlib import Path
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

sys.path.insert(0, '../')

# Use Agg backend for headless rendering and import pyplot/visualiser at module load
import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt
from analysis.run import Run
from analysis.run_analyser import RunAnalyser
from analysis.run_visualiser import RunVisualiser


def create_app(log_dir: Path) -> FastAPI:
    app = FastAPI(title="FlySearch Log Preview API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    base_dir = log_dir.resolve()

    def secure_join(relative_path: str) -> Path:
        candidate = (base_dir / relative_path).resolve()
        # Protect against path traversal and symlinks outside of base_dir
        if os.path.commonpath([str(base_dir), str(candidate)]) != str(base_dir):
            raise HTTPException(status_code=403, detail="Access outside of LOG_DIR is forbidden")
        return candidate

    @app.get("/", response_class=JSONResponse)
    async def root():
        return {"message": "OK", "log_dir": str(base_dir)}

    @app.get("/runs", response_class=JSONResponse)
    async def list_runs() -> List[str]:
        try:
            runs = [p.name for p in base_dir.iterdir() if p.is_dir()]
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="LOG_DIR not found")
        return sorted(runs)

    @app.get("/runs/{run}/episodes", response_class=JSONResponse)
    async def list_episodes(run: str) -> List[str]:
        run_dir = secure_join(run)
        if not run_dir.exists() or not run_dir.is_dir():
            raise HTTPException(status_code=404, detail="Run not found")
        episodes = [p.name for p in run_dir.iterdir() if p.is_dir()]
        return sorted(episodes)

    @app.get("/file/{rel_path:path}")
    async def get_file(rel_path: str):
        try:
            full_path = secure_join(rel_path)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid path")

        if not full_path.exists() or not full_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(str(full_path))

    @app.get("/runs/{run}/file/{rel_path:path}")
    async def get_file_in_run(run: str, rel_path: str):
        try:
            full_path = secure_join(str(Path(run) / rel_path))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid path")

        if not full_path.exists() or not full_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(str(full_path))

    @app.get("/runs/{run}/episodes/{episode}/success", response_class=JSONResponse)
    async def episode_success(run: str, episode: str):
        episode_dir = secure_join(str(Path(run) / episode))
        if not episode_dir.exists() or not episode_dir.is_dir():
            raise HTTPException(status_code=404, detail="Episode not found")
        analyser = RunAnalyser(Run(episode_dir))
        success = analyser.success_criterion_satisfied(threshold=10, check_claimed=True)
        return success

    @app.get("/runs/{run}/episodes/{episode}/preview.png")
    async def episode_preview(run: str, episode: str):
        episode_dir = secure_join(str(Path(run) / episode))
        if not episode_dir.exists() or not episode_dir.is_dir():
            raise HTTPException(status_code=404, detail="Episode not found")

        run_obj = Run(episode_dir)
        visualiser = RunVisualiser(run_obj)

        fig = plt.figure(figsize=(8, 6), dpi=150)
        ax = fig.add_subplot(projection='3d')
        visualiser.plot(ax)

        import io
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return StreamingResponse(buf, media_type='image/png')

    return app


def _default_logs_dir() -> Path:
    env_dir = os.environ.get("LOG_DIR")
    if env_dir:
        return Path(env_dir)
    repo_default = Path(__file__).resolve().parent.parent / "all_logs"
    return repo_default


# When imported by `uvicorn web.log_preview_backend:app`, fall back to env/default dir
app = create_app(_default_logs_dir())

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="FlySearch Log Preview API server")
    parser.add_argument("--log-dir", type=str, default=str(_default_logs_dir()),
                        help="Base directory containing log episodes")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    selected_dir = Path(args.log_dir).resolve()
    uvicorn.run(create_app(selected_dir), host=args.host, port=args.port, reload=args.reload)
