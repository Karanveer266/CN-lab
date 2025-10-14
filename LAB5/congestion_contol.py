import matplotlib.pyplot as plt
import random

def tcp_congestion_control(
    rounds=30,
    init_cwnd=1,
    ssthresh=12,
    loss_prob=0.18,
    seed=7
):
    random.seed(seed)
    cwnd_history = []
    cwnd = init_cwnd
    threshold = ssthresh
    state = "slow start"

    print(f"{'Round':<6} {'cwnd':<6} {'ssthresh':<9} {'Phase':<18} {'Loss'}")
    print("-" * 50)

    for r in range(1, rounds + 1):
        loss = random.random() < loss_prob
        cwnd_history.append(cwnd)

        # Print summary for this round
        print(f"{r:<6} {cwnd:<6} {threshold:<9} {state:<18} {'Yes' if loss else 'No'}")

        if loss:
            # Multiplicative decrease
            threshold = max(cwnd // 2, 1)
            cwnd = init_cwnd
            state = "slow start"
            print(f"  Loss detected! ssthresh set to {threshold}, cwnd reset to {cwnd} (Slow Start resumes)")
        elif state == "slow start":
            cwnd *= 2
            if cwnd >= threshold:
                cwnd = threshold
                state = "congestion avoidance"
                print(f"  cwnd reached ssthresh ({threshold}), switching to Congestion Avoidance")
        elif state == "congestion avoidance":
            cwnd += 1

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(cwnd_history, marker='o', color='blue')
    plt.title("TCP Congestion Window (cwnd) Evolution")
    plt.xlabel("Transmission Round")
    plt.ylabel("cwnd (segments)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("cwnd plot.png")
    plt.show()

if __name__ == "__main__":
    tcp_congestion_control(
        rounds=30,
        init_cwnd=1,
        ssthresh=12,
        loss_prob=0.18,
        seed=3,
    )
