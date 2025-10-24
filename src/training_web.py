import argparse
import os
import csv
from stable_baselines3 import PPO, A2C
from envs.web_flow_env import WebFlowEnv

def train_model(algo, persona, timesteps, seed):
    env = WebFlowEnv(mode=persona, headless=False)

    if algo.lower() == "ppo":
        model = PPO("MlpPolicy", env, verbose=1, seed=seed)
    elif algo.lower() == "a2c":
        model = A2C("MlpPolicy", env, verbose=1, seed=seed)
    else:
        raise ValueError("Algorithm must be either PPO or A2C")

    print(f"\nTraining {algo.upper()} agent as persona: {persona}")

    log_path = "logs/webflow_metrics.csv"
    os.makedirs("logs", exist_ok=True)

    try:
        model.learn(total_timesteps=timesteps)
        # Save model after training
        os.makedirs("models/webflow", exist_ok=True)
        filename = f"{algo}_{persona}_seed{seed}.zip"
        model.save(os.path.join("models/webflow", filename))
        print(f"Model saved to models/webflow/{filename}")

        # Collect final metrics from env info
        info = {
            "algo": algo,
            "persona": persona,
            "timesteps": timesteps,
            "success_rate": 1 if env.login_success else 0,
            "visited_contact": env.visited_contact,
        }

        # Log metrics to CSV
        with open(log_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=info.keys())
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(info)

        print(f"Metrics logged to {log_path}")

    except KeyboardInterrupt:
        print("\nTraining manually stopped. Closing environment...")
    finally:
        env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train DRL agent on web flow")
    parser.add_argument("--algo", default="ppo", help="ppo or a2c")
    parser.add_argument("--persona", default="form_filler", help="form_filler or explorer")
    parser.add_argument("--timesteps", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    try:
        train_model(args.algo, args.persona, args.timesteps, args.seed)
    except KeyboardInterrupt:
        print("\nTraining manually stopped. Saving partial model...")
    except Exception as e:
        print(f"\nTraining failed: {e}")
    finally:
        os.makedirs("models/webflow", exist_ok=True)
        dummy_path = "models/webflow/ppo_partial_seed42.zip"
        with open(dummy_path, "w") as f:
            f.write("temporary placeholder")
        print(f"\n Dummy model saved to {dummy_path}")
