import random
import time

def range_str(a, b):
        return f"{a} {b}"

def go_back_n(total_frames=10, window_size=4, loss_prob=0.2, timeout=1.0, seed=None):

    if seed is not None:
        random.seed(seed)

    base = 0                 # oldest unacknowledged frame
    next_seq = 0             # next frame to send
    N = window_size
    in_flight_status = {}    # frame -> 'ok' or 'lost' for the latest send attempt

    start_time = None

    while base < total_frames:
        # Send as many as the window allows
        frames_to_send = []
        while next_seq < base + N and next_seq < total_frames:
            frames_to_send.append(next_seq)
            next_seq += 1

        if frames_to_send:
            # Grouped send print like: "Sending frames 0 3"
            print(f"Sending frames {range_str(frames_to_send[0], frames_to_send[-1])}")
            # Mark each sent frame as lost or ok for this attempt
            for f in frames_to_send:
                in_flight_status[f] = 'lost' if random.random() < loss_prob else 'ok'
            # Start (or restart) timer for oldest unACKed if needed
            if start_time is None:
                start_time = time.time()

        # Simulate receiver cumulative ACK up to first lost in-flight frame
        # Find highest consecutive 'ok' from base
        ack_upto = base - 1
        i = base
        while i < next_seq and in_flight_status.get(i) == 'ok':
            ack_upto = i
            i += 1

        if ack_upto >= base:
            # Receiver cumulatively ACKs last in-order frame index
            print(f"ACK {ack_upto} received")
            base = ack_upto + 1
            # Slide window print
            if base < total_frames:
                win_right = min(base + N - 1, total_frames - 1)
                print(f"Window slides to {range_str(base, win_right)}")
            # Clear timer if window emptied; otherwise reset for new base
            if base == next_seq:
                start_time = None
            else:
                start_time = time.time()
            continue

        # No ACK progress; check timeout if there are outstanding frames
        if base < next_seq:
            if start_time is None:
                start_time = time.time()
            if time.time() - start_time >= timeout:
                # Timeout at 'base' implies that frame 'base' was lost (first gap)
                last = next_seq - 1
                print(f"Frame {base} lost , retransmitting frames {range_str(base, last)}")
                # Retransmit all in-flight frames from base..next_seq-1
                for f in range(base, next_seq):
                    in_flight_status[f] = 'lost' if random.random() < loss_prob else 'ok'
                # Reset timer
                start_time = time.time()
            else:
                # Small sleep to avoid busy-wait; not functionally required
                time.sleep(0.01)
        else:
            # Nothing outstanding and nothing new to send; done
            break

go_back_n(15, 4, 0.25,1.0, 20)
