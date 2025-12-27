# Go-Back-N Reliable Transport Protocol Simulation

## Overview
This project simulates a **Go-Back-N reliable transport protocol** over an **unreliable network** using Python.  

In real-world networks, packets can be **lost, corrupted, or arrive out of order**. The Go-Back-N protocol ensures **reliable and in-order delivery** of packets by using:

- **Sequence Numbers:** Track each packet’s order.  
- **Checksums:** Detect corrupted packets.  
- **Acknowledgments (ACKs):** Confirm receipt of packets.  
- **Timeouts & Retransmissions:** Resend unacknowledged packets.  
- **Sliding Window:** Control the number of packets sent without waiting for ACKs, improving efficiency.

This project is **console-based** and designed for educational purposes to demonstrate how reliable transport works over unreliable channels.


## Features
- **Configurable network unreliability:**  
  - `PACKET_LOSS_PROB` – probability of packet loss.  
  - `PACKET_CORRUPT_PROB` – probability of packet corruption.  
- **Adjustable transmission parameters:**  
  - `WINDOW_SIZE` – size of the sliding window.  
  - `CHUNK_SIZE` – number of characters per packet.  
- **Real-time simulation output** showing:  
  - Packet sending  
  - Packet loss  
  - Packet corruption  
  - ACKs sent by the receiver  
  - Retransmissions triggered by timeout  
- **Message reconstruction** at the receiver side.


## How the Simulation Works

1. **Sender divides the message into packets** of `CHUNK_SIZE` characters each.  
2. **Sender transmits packets** according to the sliding window size (`WINDOW_SIZE`).  
3. **Network may randomly lose or corrupt packets**, simulated by `PACKET_LOSS_PROB` and `PACKET_CORRUPT_PROB`.  
4. **Receiver verifies each packet**:  
   - If packet is **correct and in order**, it sends an ACK.  
   - If packet is **corrupted or out of order**, it is discarded, and the receiver resends the last ACK.  
5. **Timeout mechanism:**  
   - If the sender does not receive an ACK for the oldest unacknowledged packet within `TIMEOUT` seconds, it **retransmits all unacknowledged packets** in the window (Go-Back-N behavior).  
6. **Process continues** until all packets are successfully transmitted and acknowledged.  
7. **Final reconstructed message** is displayed at the receiver.


## Example Output


