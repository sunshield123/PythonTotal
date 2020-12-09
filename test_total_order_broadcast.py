"""
Module tests total order broadcast
"""

import socket
import json
from config import BROADCAST
import random
import time
# messages
message_data = ("Hello",
                "NH...",
                "KYON")

buffer_size = 1024

# assign this variable to client to check duplicate message issue.
duplicate_client = ("127.0.0.1", 20002)

def create_client():
    data = {}
    for message in message_data:

        # select process randomly
        index = int(random.uniform(1,3))

        # randomly selected process
        client = BROADCAST[index]

        # prepare data
        data["message"] = message
        data["sender"] = "client"
        bytes_to_send = str.encode(json.dumps(data))

        # send data to process
        udp_socket_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_socket_client.sendto(bytes_to_send, client)
        print("message send by sever A: {}".format(client) + message)
        udp_socket_client.close()
        time.sleep(1)


def main():
    create_client()


if __name__ == "__main__":
    main()