import os
import platform
import subprocess
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.shell.runner import run_and_read_line


class BinExecutableFlagSetter(SetupStepInterface):
    def __init__(
        self,
        conda_executable_path: str,
        venv_dir: str,
        logger: Logger,
    ):
        self._conda_executable_path = conda_executable_path
        self._venv_dir = venv_dir
        self._logger = logger

    def get_description(self):
        return "Set executable flag to pyspark/bin files"

    def run(self):
        command = f"{self._conda_executable_path} run -p {self._venv_dir} pip show databricks-connect | grep Location:"
        pyspark_location = run_and_read_line(command, shell=True)
        site_packages_dir = pyspark_location[10:]

        pyspark_bin_dir = site_packages_dir + "/pyspark/bin"  # remove "Location: "

        if not os.path.isdir(pyspark_bin_dir):
            raise Exception(f"pyspark bin dir does not exist: {pyspark_bin_dir}")

        self._logger.info(f"Setting executable permissions to {pyspark_bin_dir}")

        subprocess.check_call(["chmod", "-R", "+x", pyspark_bin_dir])

    def should_be_run(self) -> bool:
        return platform.system() != "Windows"
