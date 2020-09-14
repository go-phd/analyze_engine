import json
import sys
import time


class CONF(object):
    HEALTH = "Health"
    FAULT = "Fault"
    UNKNOWN = "Unknown"

    GRANTLEY_PLATFORM = 'Grantley'
    PURLEY_PLATFORM = 'Purley'
    WHITLEY_PLATFORM = 'Whitley'
    CEDAR_IDLAND_PLATFORM = 'CedarIsland'
    UNKNOWN_PLATFORM = 'Unknown'

    INSPUR_VENDER = 'Inspur'
    INVENTEC_VENDER = 'Inventec'
    FOXCON_VENDER = 'Foxcon'
    UNKNOWN_VENDER = 'Unknown'

    DELTA_MAX_SECONDS = 300

    bin_dir = "bin"

    base_dir = "/var/log/venus/"

    # log
    log_file = "venus_engine_py.log"
    log_level = "debug"

    protected_commands = ""
    execute_timeout_seconds = 5
