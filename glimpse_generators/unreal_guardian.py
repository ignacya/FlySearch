import subprocess
import pathlib
import os

from time import sleep
from typing import Optional
from datetime import datetime

class UnrealGuardian:
    def __init__(self, unreal_binary_path: pathlib.Path):
        self.process: Optional[subprocess.Popen] = None
        self.unreal_binary_path = unreal_binary_path
        self.logfile = self._create_logfile()
        self._start_unreal()

    def _create_logfile(self):
        base_file_name = datetime.now().strftime("%Y-%m-%d-%H:%M:%S-FlySearchUnrealLog")
        base_path = pathlib.Path(os.environ.get("UNREAL_LOG_PATH"))
        if not base_path:
            project_root = pathlib.Path(__file__).parent.parent
            base_path = project_root
        base_path.mkdir(exist_ok=True, parents=True)

        logfile = open(base_path / base_file_name, "w")

        return logfile


    def _start_unreal(self):
        self.process = subprocess.Popen(
            [str(self.unreal_binary_path), "-RenderOffscreen",  "-nosound"],
            stdout=self.logfile,
            stderr=subprocess.STDOUT,
        )

        sleep(120)

    def reset(self):
        self.process.kill()
        print("Unreal Guardian: Terminated Unreal process.")
        self._start_unreal()

    @property
    def is_alive(self):
        return self.process.poll() is None
