from .main import *


def data_dir(name: str, options: dict = {}) -> str:
    return env_paths(name, options)["data"]


def config_dir(name: str, options: dict = {}) -> str:
    return env_paths(name, options)["config"]


def cache_dir(name: str, options: dict = {}) -> str:
    return env_paths(name, options)["cache"]


def log_dir(name: str, options: dict = {}) -> str:
    return env_paths(name, options)["log"]


def temp_dir(name: str, options: dict = {}) -> str:
    return env_paths(name, options)["temp"]
