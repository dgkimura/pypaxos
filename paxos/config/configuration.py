import json


# config file
DEFAULT_CONFIG = "paxos.json"

settings = json.loads(open(DEFAULT_CONFIG, 'r').read())

# setting names
ADDRESS = settings["address"]
ADDRESS_OF_REPLICAS = settings["address_of_replicas"]

LOG_LEVEL = settings["log_level"]
LOG_DEBUG = "DEBUG"
LOG_INFO = "INFO"
