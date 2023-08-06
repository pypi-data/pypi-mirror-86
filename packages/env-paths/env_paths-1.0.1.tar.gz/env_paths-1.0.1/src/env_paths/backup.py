import os
import platform

home_dir = os.path.expanduser("~")
os_name = platform.system()


def env(name: str):
    return os.getenv(name)


def macos(name: str):
    """
    docstring
    """
    return os.path.join(home_dir, "Library", "Caches", name)


def windows(name: str):
    appData = env("APPDATA") or os.path.join(home_dir, "AppData", "Roaming")
    localAppData = env("LOCALAPPDATA") or os.path.join(home_dir, "AppData", "Local")
    return os.path.join(localAppData, name, "Cache")


def linux(name: str):
    username = os.path.basename(home_dir)
    return os.path.join(env("XDG_CACHE_HOME") or os.path.join(home_dir, ".cache"), name)


def cache_dir(name: str):
    """
    docstring
    """
    if os_name == "Darwin":
        return macos(name)
    elif os_name == "Windows":
        return windows(name)


def env_paths(naem: str):
    """
    docstring
    """
    pass