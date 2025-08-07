import yaml
import os

#variable names in local_settings.yaml
var1 = "banks_base_path"


def load_local_settings(local_settings_path="local_settings.yaml"):
    """
    Loads and parses the local_settings.yaml file.

    Args:
        local_settings_path (str): Path to the local settings YAML file.

    Returns:
        dict: Parsed local settings as a Python dictionary.
    """
    if not os.path.exists(local_settings_path):
        raise FileNotFoundError(f"Required file '{local_settings_path}' not found. Please create it and add your base_path.")
    with open(local_settings_path, "r", encoding="utf-8") as f:
        try:
            local_settings = yaml.safe_load(f)
            banks_base_path = local_settings[var1]
        except yaml.YAMLError as e:
            raise RuntimeError(f"Error parsing '{local_settings_path}': {e}")
        except KeyError:
            raise KeyError(f"'{var1}' not found in '{local_settings_path}'.")
    return local_settings

def _load_config(config_path="banks_config.yaml"):
    """
    Loads and parses the YAML configuration file.

    Args:
        config_path (str): Path to the YAML config file.

    Returns:
        dict: Parsed configuration as a Python dictionary.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file '{config_path}' not found.")
    with open(config_path, "r", encoding="utf-8") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise RuntimeError(f"Error parsing '{config_path}': {e}")
    return config
