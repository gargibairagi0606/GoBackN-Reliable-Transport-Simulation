import random
import time

PACKET_LOSS_PROB = 0.2      
PACKET_CORRUPT_PROB = 0.1    
TIMEOUT = 3                
WINDOW_SIZE = 4
CHUNK_SIZE = 3
SLEEP_TIME = 0.2

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

class Sender:
    def __init__(self, message, receiver):
        self.packets = [message[i:i + CHUNK_SIZE] for i in range(0, len(message), CHUNK_SIZE)]
        self.receiver = receiver
        self.total = len(self.packets)
        self.base = 0
        self.next_seq = 0
        self.acks = [False] * self.total
        self.start_time = None

    def send(self):
        print("\n=== Go-Back-N Reliable Transmission Simulation ===\n")
        print(f"Message to send: '{''.join(self.packets)}'")
        print(f"Total packets: {self.total}\n")

        while self.base < self.total:
            while self.next_seq < self.base + WINDOW_SIZE and self.next_seq < self.total:
                data = self.packets[self.next_seq]
                pkt_checksum = checksum(data)
                if not self.start_time:
                    self.start_time = time.time()
                print(f"[SENDER] Sending packet {self.next_seq}: '{data}' [checksum={pkt_checksum}]")
                self.next_seq += 1

            for i in range(self.base, self.next_seq):
                if not self.acks[i]:
                    if is_lost():
                        print(f"   [NETWORK] Packet {i} lost.")
                        continue
                    ack = self.receiver.receive(i, self.packets[i], checksum(self.packets[i]))
                    if ack is not None:
                        self.acks[ack] = True

            while self.base < self.total and self.acks[self.base]:
                self.base += 1
                self.start_time = time.time()

            if self.start_time and time.time() - self.start_time > TIMEOUT:
                print(f"\n🔁 [TIMEOUT] No ACK for packet {self.base}. Retransmitting from {self.base}...\n")
                for i in range(self.base, min(self.base + WINDOW_SIZE, self.total)):
                    if not self.acks[i]:
                        print(f"🔁 [SENDER] Retransmitting packet {i}: '{self.packets[i]}' [checksum={checksum(self.packets[i])}]")
                self.next_seq = self.base
                self.start_time = time.time()

            time.sleep(SLEEP_TIME)

        print("\n=== Transmission Complete ===")
        print("All packets transmitted and acknowledged successfully!")
        print(f"[RECEIVER] Reconstructed message: '{self.receiver.reconstruct_message()}'")

if __name__ == "__main__":
    user_message = input("Enter the message to send: ")
    receiver = Receiver()
    sender = Sender(user_message, receiver)
    sender.send()
