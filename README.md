# Go-Back-N Reliable Transport Protocol Simulation

## Overview
This project simulates a **Go-Back-N reliable transport protocol** over an **unreliable network** using Python.  

In real-world networks, packets can be **lost, corrupted, or arrive out of order**. The Go-Back-N protocol ensures **reliable and in-order delivery** of packets by using:

- **Sequence Numbers:** Track each packet’s order.  
- **Checksums:** Detect corrupted packets.  
- **Acknowledgments (ACKs):** Confirm receipt of packets.  
- **Timeouts & Retransmissions:** Resend unacknowledged packets.  
- **Sliding Window:** Control the number of packets sent without waiting for ACKs, improving efficiency.

## Features
- Simulates **packet loss and corruption** with configurable probabilities  
- Uses **sliding window protocol** for efficient packet transmission  
- Displays **real-time console output** showing: packet sends, losses, corruptions, ACKs, and retransmissions  
- Reconstructs the **original message** at the receiver

## How it Works
- Sender divides the message into packets of `CHUNK_SIZE` characters.  
- Sender transmits packets within the sliding window (`WINDOW_SIZE`).  
- Packets may be lost or corrupted based on `PACKET_LOSS_PROB` and `PACKET_CORRUPT_PROB`.  
- Receiver verifies each packet:  
   - Sends ACK if correct and in order  
   - Discards packet if corrupted or out of order and resends last ACK  
- Sender retransmits packets on **timeout** if ACKs are not received.  
- Process continues until all packets are successfully delivered.  
- Receiver reconstructs the original message.

## Requirements
- Python 3.x
- No external libraries required

## Configuration
You can modify these parameters in `go_back_n.py`:

```python
PACKET_LOSS_PROB = 0.2       # Probability of packet loss
PACKET_CORRUPT_PROB = 0.1    # Probability of packet corruption
WINDOW_SIZE = 4               # Sliding window size
CHUNK_SIZE = 3                # Characters per packet
TIMEOUT = 3                   # Retransmission timeout in seconds
SLEEP_TIME = 0.2              # Delay between steps for console readability
```

## Usage

- Run the Python simulation:
```bash
python go_back_n.py
```
- Enter any message when prompted.
- Observe the console output for packet transmissions, losses, ACKs, and retransmissions.

## Example Output
*Full console output demonstrating packet transmission, loss, corruption, ACKs, and message reconstruction:*
```
Enter the message to send: Reliable Transmission Simulation

Go-Back-N Reliable Transmission Simulation

Message to send: 'Reliable Transmission Simulation'
Total packets: 11

[SENDER] Sending packet 0: 'Rel' [checksum=35]
[SENDER] Sending packet 1: 'iab' [checksum=44]
[SENDER] Sending packet 2: 'le ' [checksum=241]
[SENDER] Sending packet 3: 'Tra' [checksum=39]
[RECEIVER] Packet 0 received correctly. Sending ACK 0.
[RECEIVER] Packet 1 received correctly. Sending ACK 1.
[RECEIVER] Packet 2 received correctly. Sending ACK 2.
[RECEIVER] Packet 3 received correctly. Sending ACK 3.
[SENDER] Sending packet 4: 'nsm' [checksum=78]
[SENDER] Sending packet 5: 'iss' [checksum=79]
[SENDER] Sending packet 6: 'ion' [checksum=70]
[SENDER] Sending packet 7: ' Si' [checksum=220]
[RECEIVER] Packet 4 received correctly. Sending ACK 4.
[RECEIVER] Packet 5 received correctly. Sending ACK 5.
[RECEIVER] Packet 6 received correctly. Sending ACK 6.
[RECEIVER] Packet 7 received correctly. Sending ACK 7.
[SENDER] Sending packet 8: 'mul' [checksum=78]
[SENDER] Sending packet 9: 'ati' [checksum=62]
[SENDER] Sending packet 10: 'on' [checksum=221]
[RECEIVER] Packet 8 received correctly. Sending ACK 8.
[RECEIVER] Packet 9 corrupted. Discarded.
[RECEIVER] Packet 10 out of order. Expected 9. Discarded.
[RECEIVER] Resending ACK 8.
[RECEIVER] Packet 9 received correctly. Sending ACK 9.
[RECEIVER] Packet 10 received correctly. Sending ACK 10.

Transmission Complete
All packets transmitted and acknowledged successfully!
[RECEIVER] Reconstructed message: 'Reliable Transmission Simulation'
```

## Future Improvements
- Implement Selective Repeat protocol for more efficient retransmissions
- Add GUI visualization of packet transmission
- Extend to real network sockets for actual UDP/TCP transmission
- Log transmission statistics for analysis
