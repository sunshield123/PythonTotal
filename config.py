"""
Config file
"""

# Sequencer configuration
SEQUENCER = {"name": "sequencer", "address": ("127.0.0.1", 20001)}

# Node process client configuration
CLIENTS = ({"name": "process_1", "address": ("127.0.0.1", 20002)},
           {"name": "process_2", "address": ("127.0.0.1", 20003)},
           {"name": "process_3", "address": ("127.0.0.1", 20004)})

# Broadcast message configuration
BROADCAST = (("127.0.0.1", 20001), ("127.0.0.1", 20002), ("127.0.0.1", 20003), ("127.0.0.1", 20004))

# Node process list names
PROCESSES = ("process_1", "process_2", "process_3")