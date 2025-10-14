import random
import time

def stop_and_wait(num_frames=5, loss_prob=0.3, timeout=1.0, ack_loss_prob=0.0, seed=42):

    seq = 0                 # sender's current frame sequence bit (0/1)
    expected_seq = 0        # receiver's expected sequence bit (0/1)
    total_sent = 0
    total_retx = 0
    delivered = 0

    for i in range(num_frames):
        acked = False
        while not acked:
            # Sender transmits current frame i
            print(f"Sending Frame {i} (seq {seq})")
            total_sent += 1

            if random.random() < loss_prob:
                time.sleep(timeout)
                print(f"Frame {i} lost, timeout, retransmitting ...")
                total_retx += 1
                # Retransmit same frame
                continue

            # Receiver side
            if seq == expected_seq:
                # First time seeing this seq: accept and deliver
                print(f"Receiver: accepted Frame {i} (seq {seq})")
                delivered += 1
                ack_bit = seq            # ACK carries the received bit
                expected_seq ^= 1        # expect the other bit next
            else:
                # Duplicate: do not deliver, just ACK the received bit
                print(f"Receiver: duplicate Frame {i} (seq {seq}), discarding")
                ack_bit = seq           

            if random.random() < ack_loss_prob:
                time.sleep(timeout)
                print(f"ACK {ack_bit} for Frame {i} lost, timeout, retransmitting ...")
                total_retx += 1
                continue

            # Sender receives ACK
            if ack_bit == seq:
                print(f"ACK {ack_bit} received")
                seq ^= 1      # advance to next bit
                acked = True
            else:
                time.sleep(timeout)
                print(f"Out-of-sync ACK {ack_bit} ignored, retransmitting ...")
                total_retx += 1

    print(f"\nSummary: sent={total_sent}, retransmissions={total_retx}, delivered={delivered}")


stop_and_wait(6,0.3,1.0,0.0,20)

