import json
import os
import jsonpickle
import font


class Config:
    def __init__(self):
        self.user_name = "User"
        self.script_dir = ""
        self.command_font = font.Font("Consolas", 12)


def saveConfig(config):
    if not os.path.exists(os.path.expanduser("~") + "\\.cosmos"):
        os.makedirs(os.path.expanduser("~") + "\\.cosmos")
    with open(os.path.expanduser("~") + "\\.cosmos\\config.json", "w") as f:
        json.dump(jsonpickle.encode(config), f)


def loadConfig():
    if not os.path.isfile(os.path.expanduser("~") + "\\.cosmos\\config.json"):
        config = Config()
        saveConfig(config)
        return config
    else:
        with open(os.path.expanduser("~") + "\\.cosmos\\config.json", "r") as f:
            return jsonpickle.decode(json.load(f))
