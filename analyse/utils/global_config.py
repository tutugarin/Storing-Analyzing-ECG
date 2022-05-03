"""
    Global Config variable is defined here
"""

from itertools import product
import json
from pathlib import Path


class GlobalConfig:
    """
        Contains global variable
    """
    __inited : bool = False
    __conf = {
        "databases": {},
        "window_size": 0,
        "threshold": 0,
        "ngram_size": 0,
        "possible_ngrams": [],

        "est_params": {},
        "rf_params": {},
    }

    def __init__(self, path_to_config):
        """
            read params.json and set constants
        """
        if self.__inited:
            return
        self.__inited = True

        with open(path_to_config, encoding='UTF-8') as file:
            params_list = json.load(file)

        GlobalConfig.set("databases", params_list["databases"])

        sig_params = params_list["signal params"]
        GlobalConfig.set("window_size", sig_params["window_size"])
        GlobalConfig.set("max_bpm", sig_params["max_bpm"])

        run_params = params_list["run params"]
        GlobalConfig.set("threshold", run_params["threshold"])
        GlobalConfig.set("ngram_size", run_params["ngram_size"])
        possible_ngrams = list(
            map(
                lambda s: ''.join(s),
                product('ABC', repeat=GlobalConfig.get("ngram_size"))
            )
        )
        GlobalConfig.set("possible_ngrams", possible_ngrams)

        GlobalConfig.set("est_params", params_list["est params"])
        GlobalConfig.set("rf_params", params_list["random forest params"])

    @staticmethod
    def get(name):
        """
            get constant named 'name'
        """
        return GlobalConfig.__conf[name]

    @staticmethod
    def set(name, value):
        """
            set constant named 'name' with value
        """
        GlobalConfig.__conf[name] = value


script_location = Path(__file__).absolute().parent
file_location = script_location / '../config/params.json'
CONFIG = GlobalConfig(file_location)
