# pylint: disable=too-many-instance-attributes

"""
    Global Config variable is defined here
"""

import json

class GlobalConfig:
    """
        Contains global variable
    """
    __conf = {
        "databases" : {},
        "window_size" : 0,
        "treshold" : 0,
    }

    @staticmethod
    def config(name):
        """
            get contant named 'name'
        """
        return GlobalConfig.__conf[name]

    @staticmethod
    def set(name, value):
        """
            set contant named 'name' with value
        """
        GlobalConfig.__conf[name] = value

def init_config(path_to_config):
    """
        read params.json and set constats
    """
    with open(path_to_config, encoding='UTF-8') as file:
        params_list = json.load(file)

    GlobalConfig.set("databases", params_list["databases"])

    sig_params = params_list["signal params"]
    GlobalConfig.set("window_size", sig_params["window_size"])

    run_params = params_list["run params"]
    GlobalConfig.set("treshold", run_params["treshold"])
