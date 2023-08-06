import os
import platform
import tempfile

homedir = os.path.expanduser("~")
tmpdir = tempfile.gettempdir()
os_name = platform.system()
join = os.path.join


def env(name: str):
    return os.getenv(name)


def assign(target: dict, *args):
    for arg in args:
        target.update(arg)
    return target


def macos(name: str) -> dict:
    library = join(homedir, "Library")
    return {
        "data": join(library, "Application Support", name),
        "config": join(library, "Preferences", name),
        "cache": join(library, "Cache", name),
        "log": join(library, "Log", name),
        "temp": join(tmpdir, name),
    }


def windows(name: str) -> dict:
    appdata = env("APPDATA") or join(homedir, "AppData", "Roaming")
    local_appdata = env("LOCALAPPDATA") or join(homedir, "AppData", "Local")
    return {
        "data": join(local_appdata, name, "Data"),
        "config": join(appdata, name, "Config"),
        "cache": join(local_appdata, name, "Cache"),
        "log": join(local_appdata, name, "Log"),
        "temp": join(tmpdir, name),
    }


def linux(name: str) -> dict:
    username = os.path.basename(homedir)
    return {
        "data": join(env("XDG_DATA_HOME") or join(homedir, ".local", "share"), name),
        "config": join(env("XDG_CONFIG_HOME") or join(homedir, ".config"), name),
        "cache": join(env("XDG_CACHE_HOME") or join(homedir, ".cache"), name),
        "log": join(env("XDG_STATE_HOME") or join(homedir, ".local", "state"), name),
        "temp": join(tmpdir, username, name),
    }


def env_paths(name: str, options: dict = {}) -> dict:
    if type(name) != str:
        raise TypeError(f"Expected string, got {type(name)}")
    options = assign({"suffix": "python"}, options)
    if options.get("suffix"):
        name += f"-{options.get('suffix')}"
    if platform.system() == "Darwin":
        return macos(name)
    if platform.system() == "Windows":
        return windows(name)
    return linux(name)


__all__ = ["env_paths"]
