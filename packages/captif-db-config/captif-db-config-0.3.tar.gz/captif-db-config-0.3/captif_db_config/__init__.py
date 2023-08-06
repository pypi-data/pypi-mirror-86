__version__ = "0.3"

from pathlib import Path
from configparser import ConfigParser


CONFIG_FILENAME = ".captif-db.ini"
CONFIG_FILE = Path.home().joinpath(CONFIG_FILENAME)


def config():
    config_ = ConfigParser()
    config_.read(CONFIG_FILE)
    return config_


def get_config_param(parameter, raise_exception=True):
    value = config().get("GENERAL", parameter, fallback="")

    if value:
        return value

    if raise_exception:
        raise ConfigError(f"'{parameter}' not defined in the config file")

    return None


def get_database_params():
    return (
        get_config_param("url"),
        get_config_param("port"),
        get_config_param("username"),
        get_config_param("password"),
        get_config_param("database"),
        get_config_param("connection_string"),
    )


def database_connection_str(database):
    url = get_config_param("url")
    port = get_config_param("port")
    connection_str = get_config_param("connection_string")

    username = get_config_param("username")
    password = get_config_param("password")

    return f"{connection_str}{username}:{password}@{url}:{port}/{database}"


class ConfigError(Exception):
    pass
