import json


# config file
DEFAULT_CONFIG = "paxos.json"

settings = json.loads(open(DEFAULT_CONFIG, 'r').read())

# setting names
ADDRESS = "address"
ADDRESS_OF_REPLICAS = "address_of_replicas"

LOG_LEVEL = "log_level"
LOG_DEBUG = "DEBUG"
LOG_INFO = "INFO"
