import os


class DatabricksConnectDetector:
    def detect(self):
        poetry_lock_path = os.getcwd() + os.sep + "poetry.lock"

        with open(poetry_lock_path, "r", encoding="utf-8") as f:
            content = f.read()

        return 'name = "databricks-connect"' in content
