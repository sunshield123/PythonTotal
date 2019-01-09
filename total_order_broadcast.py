"""
This module initializes the nodes and sequencer
"""
import signal
from sequencer import Sequencer
from config import CLIENTS, SEQUENCER
from process import Process


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    """
    If anyone presses CTL-C, it raises exception on
    closes the processes
    Args:
        signum: signal number
        frame: None

    """
    raise ServiceExit


def init_sequencer():
    """
    Set sequencer process
    Returns:
        thread id
    """
    seq_thread = Sequencer(SEQUENCER["name"],
                           SEQUENCER["address"][0],
                           SEQUENCER["address"][1])
    return seq_thread


def init_nodes(threads):
    """
    Sets all processes
    Args:
        threads: thread list list

    Returns:
        threads list
    """
    for client in CLIENTS:
        threads.append(Process(client["name"],
                         client["address"][0],
                         client["address"][1]))
    return threads


def main():
    """
    It Initialises sequencer and other nodes
    Returns:

    """
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    thread_list = list()
    thread_list.append(init_sequencer())
    init_nodes(thread_list)
    return thread_list


if __name__ == "__main__":
    thread_list = []
    try:
        thread_list = main()
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
    except ServiceExit:
        for thread in thread_list:
            thread.shutdown_flag.set()
        for thread in thread_list:
            thread.join()
