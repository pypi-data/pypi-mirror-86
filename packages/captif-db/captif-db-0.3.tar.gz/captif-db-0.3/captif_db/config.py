from pathlib import Path
from configparser import ConfigParser

from captif_db.constants import CONFIG_FILENAME

CONFIG_FILE = Path.home().joinpath(CONFIG_FILENAME)


def config():
    """
    The config file must contain the following database connection details. Place this in
    the home directory with filename `.captif-db.ini`.

    [GENERAL]
    USERNAME = ****
    PASSWORD = ****
    URL = ****
    PORT = ****
    CONNECTION_STRING = ****  (e.g. mysql+pymysql://)
    DATABASE = ****  (e.g. captif)

    """

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


def database_connection_str(database=None):
    url, port, username, password, database_, connection_str = get_database_params()
    if not database:
        database = database_
    return f"{connection_str}{username}:{password}@{url}:{port}/{database}"


class ConfigError(Exception):
    pass
