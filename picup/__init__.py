"""
Time:     2023/3/6 14:25
Author:   忆千峰
Version:  V 0.1
File:     __init__.py
Email:    yiqf2022@126.com
"""
import os.path

import yaml

base_path = os.path.abspath(".")
config_path = os.path.normpath(f"{base_path}/config")


def get_config() -> dict:
    config_file = f"{config_path}/config.yaml"
    yaml_data = {}

    try:
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                yaml_data = yaml.safe_load(f)
                if not yaml_data: yaml_data = {}
    except Exception as e:
        pass

    data = to_properties(yaml_data)

    default_value = {
        "resource.path": "resource",
        "useragent.filename": "fake_useragent_0.1.11.json",
        "account.filename": "account.yaml",
        "account.username.encrypt": False,
        "account.password.encrypt": False
    }
    for key, value in default_value.items():
        if data.get(key) is None: data[key] = value
    return data


def to_properties(tree: dict) -> dict:
    data = {}
    for key, value in tree.items():
        if isinstance(value, dict):
            for sub_key, sub_value in to_properties(value).items():
                data[f"{key}.{sub_key}"] = sub_value
        else:
            data[key] = value
    return data


config_data = get_config()
resource_path = os.path.normpath(f"{base_path}/{config_data['resource.path']}")
fonts_path = os.path.normpath(f"{resource_path}/fonts")
secret_key_path = os.path.normpath(f"{resource_path}/secret_key")
tinypng_path = os.path.normpath(f"{resource_path}/tinypng")
