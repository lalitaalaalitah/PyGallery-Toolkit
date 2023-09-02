import yaml

__yaml_types = str | bool | int | float

USER_SETTINGS: dict[
    str, __yaml_types | dict[str, __yaml_types] | list[__yaml_types]
] = yaml.safe_load(open("settings/user_settings.yaml"))
