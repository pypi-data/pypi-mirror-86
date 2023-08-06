import os
from pathlib import Path
from contextlib import contextmanager
import shutil
import json
import yaml

def load_json(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data

def json_dump(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)

def parent_dir(path):
    return Path(os.path.dirname(Path(path).resolve()))

def load_yaml(file):
    with open(file, "r") as f:
        data = yaml.safe_load(f)
    return data

def dump_yaml(file, data):
    with open(file, "w") as f:
        yaml.dump(data, f, default_flow_style=False)

def path_from_env(var):
    value = os.environ.get(var)
    if value is None:
        return
    return Path(value).resolve()

def file_from_env(var):
    value = path_from_env(var)
    if value and value.is_file():
        return value
    return

def dir_from_env(var):
    value = path_from_env(var)
    if value and value.is_dir():
        return value
    return

def recursive_copy(source, dest):
    shutil.copytree(source, dest, symlinks=True)


def expandpath(path):
    return Path(os.path.expanduser(os.path.expandvars(path)))


@contextmanager
def temp_environ():
    # Backup environ
    environ = dict(os.environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(environ)