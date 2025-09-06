import os
import pathlib
import subprocess

from datetime import datetime
from time import sleep
from typing import IO, Optional, Sequence, Union
import logging


logger = logging.getLogger(__name__)


class UnrealGuardian:
    """Lifecycle manager for the standalone Unreal simulation process.

    - Spawns the Unreal binary with sensible defaults for headless rendering.
    - Streams stdout/stderr to a timestamped logfile under a configurable directory.
    - Provides reset semantics and liveness checks.
    """

    def __init__(
        self,
        unreal_binary_path: Union[str, pathlib.Path],
        startup_wait_seconds: int = 120,
        extra_args: Optional[Sequence[str]] = None,
        log_dir_env_var: str = "UNREAL_LOG_PATH",
    ) -> None:
        self.process: Optional[subprocess.Popen[str]] = None
        self.unreal_binary_path = pathlib.Path(unreal_binary_path)
        self.startup_wait_seconds = int(startup_wait_seconds)
        self.extra_args = list(extra_args) if extra_args is not None else []

        if not self.unreal_binary_path.is_file():
            raise FileNotFoundError(f"Unreal binary not found: {self.unreal_binary_path}")

        self.logfile: IO[str] = self._create_logfile(log_dir_env_var)
        self._start_unreal()

    def _create_logfile(self, log_dir_env_var: str) -> IO[str]:
        base_file_name = datetime.now().strftime("%Y-%m-%d-%H:%M:%S-FlySearchUnreal.log")

        env_dir = os.environ.get(log_dir_env_var)
        if env_dir and env_dir.strip():
            base_path = pathlib.Path(env_dir.strip())
        else:
            # Default to project root
            base_path = pathlib.Path(__file__).parent.parent / "unreal_logs"

        base_path.mkdir(exist_ok=True, parents=True)
        return open(base_path / base_file_name, "w")

    def _start_unreal(self) -> None:
        logger.info("Guardian is starting Unreal process.")
        args = [
            str(self.unreal_binary_path),
            "-RenderOffscreen",
            "-nosound",
            *self.extra_args,
        ]

        self.process = subprocess.Popen(
            args,
            stdout=self.logfile,
            stderr=subprocess.STDOUT,
        )

        # Give the process time to initialize and start the UnrealCV server.
        sleep(self.startup_wait_seconds)

    def _terminate_process(self) -> None:
        if self.process is None:
            return
        if self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
            finally:
                self.process = None
        else:
            self.process = None

    def reset(self) -> None:
        logger.info("Guardian is resetting Unreal process.")
        self._terminate_process()
        self._start_unreal()

    def stop(self) -> None:
        """Gracefully stop the Unreal process."""
        logger.info("Guardian is stopping Unreal process.")
        self._terminate_process()

    def close(self) -> None:
        """Stop the process and close the logfile handle."""
        self.stop()
        try:
            if not self.logfile.closed:
                self.logfile.close()
        except Exception as ex:
            logger.error(f"Error closing logfile: {ex}")

    @property
    def is_alive(self) -> bool:
        return self.process is not None and self.process.poll() is None
