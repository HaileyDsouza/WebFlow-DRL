import pandas as pd
import matplotlib.pyplot as plt
import os

LOG_DIR = "logs"

def plot_graphs(csv_path):
    if not os.path.exists(csv_path):
        print(f" File not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    print(f"Loaded data from {csv_path}")

    #  Learning Curve: Reward vs Episode
    plt.figure(figsize=(8,5))
    plt.plot(df["episode"], df["total_reward"], marker='o', color='teal')
    plt.title("Learning Curve: Reward vs. Episode")
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(LOG_DIR, "reward_vs_timesteps.png"))
    plt.close()
    print("Saved: reward_vs_timesteps.png")

    #  Score Distribution
    plt.figure(figsize=(8,5))
    plt.hist(df["total_reward"], bins=10, color='orange', edgecolor='black', alpha=0.8)
    plt.title("Score Distribution: Rewards Across Episodes")
    plt.xlabel("Total Reward")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(LOG_DIR, "score_distribution.png"))
    plt.close()
    print(" Saved: score_distribution.png")

    #  Success Rate 
    plt.figure(figsize=(8,5))
    plt.plot(df["episode"], df["login_success"], label="Login Success", color='green', marker='o')
    plt.plot(df["episode"], df["visited_contact"], label="Contact Page Visit", color='purple', marker='x')
    plt.title("Success Rate: Episodes Completing Key Steps")
    plt.xlabel("Episode")
    plt.ylabel("Success (1 = yes, 0 = no)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(LOG_DIR, "success_rate.png"))
    plt.close()
    print(" Saved: success_rate.png")

if __name__ == "__main__":
    csv_path = os.path.join(LOG_DIR, "ppo_formfiller_eval.csv")
    plot_graphs(csv_path)
