import random
import time

PACKET_LOSS_PROB = 0.2      
PACKET_CORRUPT_PROB = 0.1    
TIMEOUT = 3                
WINDOW_SIZE = 4
CHUNK_SIZE = 3                

def checksum(data):
    return sum(ord(ch) for ch in data) % 256

def is_lost():
    return random.random() < PACKET_LOSS_PROB

def is_corrupted():
    return random.random() < PACKET_CORRUPT_PROB

class Receiver:
    def __init__(self):
        self.expected_seq = 0
        self.received_packets = []

    def receive(self, seq_num, data, pkt_checksum):
        if is_corrupted() or checksum(data) != pkt_checksum:
            print(f"   [RECEIVER] Packet {seq_num} corrupted. Discarded.")
            return None

        if seq_num == self.expected_seq:
            print(f"[RECEIVER] Packet {seq_num} received correctly. Sending ACK {seq_num}.")
            self.received_packets.append(data)
            self.expected_seq += 1
            return seq_num
        else:
            print(f"[RECEIVER] Packet {seq_num} out of order. Expected {self.expected_seq}. Discarded.")
            if self.expected_seq > 0:
                print(f"[RECEIVER] Resending ACK {self.expected_seq - 1}.")
            return None

    def reconstruct_message(self):
        return ''.join(self.received_packets)

def go_back_n_sender(message, receiver):
    packets = [message[i:i + CHUNK_SIZE] for i in range(0, len(message), CHUNK_SIZE)]
    total = len(packets)
    base = 0
    next_seq = 0
    acks = [False] * total
    start_time = None

    print("\n=== Go-Back-N Reliable Transmission Simulation ===\n")
    print(f"Message to send: '{message}'")
    print(f"Total packets: {total}\n")

    while base < total:
        while next_seq < base + WINDOW_SIZE and next_seq < total:
            data = packets[next_seq]
            pkt_checksum = checksum(data)
            if not start_time:
                start_time = time.time()
            print(f"[SENDER] Sending packet {next_seq}: '{data}' [checksum={pkt_checksum}]")
            next_seq += 1

        for i in range(base, next_seq):
            if not acks[i]:
                if is_lost():
                    print(f"   [NETWORK] Packet {i} lost.")
                    continue
                ack = receiver.receive(i, packets[i], checksum(packets[i]))
                if ack is not None:
                    acks[ack] = True

        while base < total and acks[base]:
            base += 1
            start_time = time.time()
        if start_time and time.time() - start_time > TIMEOUT:
            print(f"\n[TIMEOUT] No ACK for packet {base}. Retransmitting from {base}...\n")
            for i in range(base, min(base + WINDOW_SIZE, total)):
                if not acks[i]:
                    print(f"[SENDER] Retransmitting packet {i}: '{packets[i]}' [checksum={checksum(packets[i])}]")
            next_seq = base
            start_time = time.time()

        time.sleep(1)

    print("\n=== Transmission Complete ===")
    print("All packets transmitted and acknowledged successfully!")
    print(f"[RECEIVER] Reconstructed message: '{receiver.reconstruct_message()}'")

if __name__ == "__main__":
    user_message = input("Enter the message to send: ")
    receiver = Receiver()
    go_back_n_sender(user_message, receiver)
