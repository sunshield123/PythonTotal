"""
Config file
"""

# Sequencer configuration
SEQUENCER = {"name": "sequencer", "address": ("192.168.0.14", 20055)}

# Node process client configuration
CLIENTS = (
           {"name": "process_2", "address": ("192.168.0.14", 20057)},
           {"name": "process_3", "address": ("192.168.56.1", 10058)})

# Broadcast message configuration for 2 process
BROADCAST = (("192.168.0.14", 20055),("192.168.0.14", 20057), ("192.168.56.1", 10058))

# Node process list names
PROCESSES = ("process_2", "process_3")