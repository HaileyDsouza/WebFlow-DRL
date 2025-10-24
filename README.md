# WebFlow-DRL: Reinforcement Learning for Web Automation

This repository implements a **custom Gymnasium-compatible environment** simulating browser-based workflows such as login, navigation, and form submission on a sample website. Agents are trained using **PPO** and **A2C** to autonomously perform multi-step web interactions.

---

## Contributors

| Name | Role / Contribution |
|------|----------------------|
| **Hailey D’Souza** | Lead Developer |
| **Sammak Ahmed** | Developer |

---

## Project Structure

project_root/
│
├─ envs/ # Custom Selenium-based environment
│ └─ web_flow_env.py
│
├─ src/ # Training, evaluation, and graph scripts
│ ├─ training_web.py
│ ├─ eval_web.py
│ └─ graphs.py
│
├─ web_app/ # Local test web app templates
│ ├─ templates/
│ │ ├─ index.html
│ │ ├─ login.html
│ │ ├─ contact.html
│ │ ├─ navbar.html
│ │ └─ dashboard.html
│ └─ server.py
│
├─ models/webflow/ # Saved models
├─ logs/ # Evaluation results and plots
├─ configs/ # (Optional) Training configs
├─ requirements.txt
└─ README.md

---

## Setup

1. Ensure **Python 3.10+** is installed.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # on Windows
   source .venv/bin/activate  # on Mac/Linux
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Training an Agent
Use src/training_web.py to train a PPO or A2C model on the WebFlowEnv.

CLI Arguments
Argument	Description	Default
--algo	RL algorithm (ppo or a2c)	ppo
--persona	Agent persona (form_filler or explorer)	form_filler
--timesteps	Total training timesteps	8000
--seed	Random seed	42

Example Commands
Train a PPO agent for form-filling tasks:

bash
Copy code
python -m src.training_web --algo ppo --persona form_filler --timesteps 8000
Train an A2C agent for exploration tasks:

bash
Copy code
python -m src.training_web --algo a2c --persona explorer --timesteps 5000
Evaluating a Model
Evaluate a trained model and log metrics using src/eval_web.py.

CLI Arguments
Argument	Description	Default
--algo	Algorithm type (ppo or a2c)	ppo
--model_path	Path to trained model	required
--persona	Persona used for evaluation	form_filler
--episodes	Number of evaluation runs	5

Example
bash
Copy code
python -m src.eval_web --algo ppo --model_path models/webflow/ppo_formfiller_final.zip --episodes 5
If the trained model file is missing, the script automatically generates dummy evaluation data in:

bash
Copy code
logs/ppo_formfiller_eval.csv
Visualization and Metrics
Use src/graph_results.py to visualize training results and evaluation metrics.

bash
Copy code
python -m src.graph_results
Outputs
File	Description
logs/ppo_formfiller_eval.csv	Episode-level metrics
logs/reward_vs_episode.png	Reward progression plot

Environment Details
Actions
Action	Description
0	Click next / proceed
1	Fill form input
2	Submit form
3	Navigate to next page

Observations
Each observation represents a simplified web state (page progress, form completion, and navigation success indicators).

Reward Structure
Event	Reward
Successful login	+10
Correct form input	+5
Navigation to contact page	+8
Repeated failure	-2
Timeout	-5

Metrics Collected
The evaluation script logs:

Total reward per episode

Login success rate

Contact page visit success

Steps taken

Time elapsed

Example Results
Reward Curve:

<p align="center"> <img src="logs/reward_vs_episode.png" width="500"> </p>
Evaluation CSV Preview:

Episode	Total Reward	Login Success	Contact Visit	Steps	Time Elapsed
1	12.0	1	1	15	18.2
2	9.5	1	0	12	14.6

Demo Run
After setup, run:

bash
Copy code
python -m src.training_web
python -m src.eval_web
python -m src.graph_results
Expected outputs:

✅ Automated Chrome browser interaction

✅ Evaluation CSV with metrics

✅ Reward vs Episode graph in logs/

Notes & Best Practices
✅ Compatible with headless browser automation (Selenium + Gymnasium)

✅ Uses PPO and A2C algorithms from Stable-Baselines3

✅ CSV + PNG outputs for report submission

✅ Dummy model/eval fallback for reproducibility

❌ Long training times if timesteps > 5000

❌ Browser window may freeze if not headless

yaml
Copy code
