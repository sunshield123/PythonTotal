It implements total order broadcast Protocol.

It implements fixed sequencer BB(broadcast-broadcast).


Algorithm implemented

---------start-----------------
Sender:
   procedure to_broadcast(m)
   send (m) to sequencer

Sequencer:
Init
   seqnum = 0
   when receive(m)
       sn(m) := seqnum
       send(m, sn(m)) to all
       seqnum: = seqnum + 1

Destination (code of process pi):
    next_deliver(pi) := 0
    pending(pi) := ()
    when receive(m, seqnum)
        pending(pi) := pending(pi) U ({m, seqnum})
        while (m', seqnum') belongs to pending(pi) and seqnum'== next_deliver(pi) do
            deliver(m')
            next_deliver(pi) :=  next_deliver(pi) + 1

------------end-----------------

This package implements total order broadcast protocol. Implementation of sequencer is in sequencer.py,
and all other node process implementation is in process.py

How to run total_order_broadcast

import this package in pycharm
run total_order_broadcast.py

How to test total_order broadcast
run test_total_order_broadcast.py, It creates files of process names and
where you can check message and its sequence number

How to change messages and message order
In test_total_order_broadcast.py change message_data data as you wish

How to check duplicate message scenario coming from same process
assign client this duplicate_client in test_total_order_broadcast




