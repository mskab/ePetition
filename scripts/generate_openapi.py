#! /usr/bin/python
import importlib
import os
import sys

import yaml
from fastapi.openapi.utils import get_openapi


workspace = os.environ.get("GITHUB_WORKSPACE")
sys.path.append(workspace)

try:
    mod = importlib.import_module("api.main")
except Exception as e:
    raise ModuleNotFoundError(
        f"Error importing api/main.py file."
        f"Error: {e}"
    )

app = getattr(mod, "app")

specs = get_openapi(
    title=app.title if app.title else None,
    version=app.version if app.version else None,
    openapi_version=app.openapi_version if app.openapi_version else None,
    description=app.description if app.description else None,
    routes=app.routes if app.routes else None,
)

with open("openapi.yml", "w") as f:
    yaml.dump(specs, f)