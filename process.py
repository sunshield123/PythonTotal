"""
Module which has all the node processes
"""
import json
import socket
import threading
from multiprocessing import Queue
from message_detail import Message

from config import BROADCAST, PROCESSES


class Process(threading.Thread):
    """
    Process node
    """

    def __init__(self, process_name, ip, port):
        """
        Init
        Args:
            process_name: process name
            ip: ip
            port: port
        """
        threading.Thread.__init__(self)

        self.shutdown_flag = threading.Event()
        self.process_name = process_name
        self.ip = ip
        self.port = port
        self.sock = None
        self.lock = threading.Lock()
        self.buffer_size = 1024

    def run(self):
        """
        Runs process

        """
        print('Thread #%s started' % self.ident)
        # Create socket which listens
        self.sock = socket.socket(family=socket.AF_INET,
                                  type=socket.SOCK_DGRAM)

        print("thread bound at")
        print((self.ip, int(self.port)))
        self.sock.bind((self.ip, int(self.port)))
        print("Process name: {}".format(self.process_name))


        # put message as per sequence id priority
        priority_queue = Queue.PriorityQueue()

        # Delivered messages order
        delivered = []
        # next deliverable counter
        next_deliverable = 0
        while not self.shutdown_flag.is_set():
            data = self.sock.recvfrom(self.buffer_size)
            self.lock.acquire()
            message = data[0]
            data = json.loads(message)
            message = data["message"]
            sender = data["sender"]
            sequencer_sender = data.get("sequencer_sender", None)
            # check if message came from client, broadcast
            # message to each process
            if sender == "client":
                priority_queue.put(Message(message, sender))
                print("broad cast message")
                self.broadcast_message(data)

            # if sender is one of the other process,
            # put data into buffer and wait for sequencer,
            # to get the sequence id
            elif sender in PROCESSES:
                priority_queue.put(Message(message, sender))

            # If sender is sequencer, you got sequence id for the message
            if sequencer_sender:
                priority_queue.put(Message(message,
                                           sender,
                                           data["message_id"],
                                           sequencer_sender))

                # Pop out data from priority queue as per sequence number
                while not priority_queue.empty():
                    queue_data = priority_queue.get()
                    if queue_data.message_id != next_deliverable:
                        priority_queue.put(queue_data)
                        break
                    else:
                        next_deliverable = next_deliverable + 1
                        delivered.append(queue_data)

            while not priority_queue.empty():
                queue_data = priority_queue.get()
                if queue_data.message_id != next_deliverable:
                    priority_queue.put(queue_data)
                    break
                else:
                    next_deliverable = next_deliverable + 1
                    delivered.append(queue_data)

            # Write data into file in an order as process to deliver it
            with open(self.process_name, "w") as f:
                for message in delivered:
                    f.write("message: " + message.message + " --- " + "sequence_num: " + str(message.message_id) + "\n")
            self.lock.release()

        print('Thread #%s stopped' % self.ident)

    def broadcast_message(self, data):
        """
        Broad cast messages, sequencer and other processes
        Args:
            data: data

        """

        for client in BROADCAST:
            data["sender"] = self.process_name
            bytes_to_send = str.encode(json.dumps(data))
            if (self.ip, self.port) != client:
                self.sock.sendto(bytes_to_send, client)
