import gymnasium as gym
from gymnasium import spaces
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import time

class WebFlowEnv(gym.Env):
    def __init__(self, mode="form_filler", headless=True):
        super().__init__()
        self.mode = mode  # "form_filler" or "explorer"
        self.action_space = spaces.Discrete(4)  # 0: type username, 1: type password, 2: submit, 3: visit contact page
        self.observation_space = spaces.Box(low=0, high=1, shape=(3,), dtype=np.float32)
        self.max_steps = 20
        self.step_count = 0

        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        # keep headless optional
        if headless:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.driver.get("http://127.0.0.1:5000/login")
        time.sleep(2) 
        self.step_count = 0
        self.username_done = False
        self.password_done = False
        self.login_success = False
        self.visited_contact = False
        self.start_time = time.time()
        return np.zeros(3, dtype=np.float32), {}

    def step(self, action):
        reward = 0
        done = False
        info = {}
        self.step_count += 1

        try:
            if action == 0:
                # Wait until the username field appears
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                user = self.driver.find_element(By.NAME, "username")
                user.clear()
                user.send_keys("admin")
                self.username_done = True
                reward += 0.2

            elif action == 1:
                # Wait for password input
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "password"))
                )
                pwd = self.driver.find_element(By.NAME, "password")
                pwd.clear()
                pwd.send_keys("123")
                self.password_done = True
                reward += 0.2

            elif action == 2:
                # Try clicking login button
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "button"))
                )
                self.driver.find_element(By.TAG_NAME, "button").click()
                time.sleep(0.3)
                if "Dashboard" in self.driver.title:
                    reward += 5
                    self.login_success = True
                    done = True
                else:
                    reward -= 0.5

            elif action == 3:
                self.driver.get("http://127.0.0.1:5000/contact")
                self.visited_contact = True
                reward += 0.5

        except Exception as e:
            print("Error:", e)
            reward -= 0.1

        if self.mode == "explorer" and self.visited_contact:
            reward += 0.3

        if self.step_count >= self.max_steps:
            done = True

        obs = np.array([
            1 if self.username_done else 0,
            1 if self.password_done else 0,
            1 if self.login_success else 0
        ], dtype=np.float32)

        info = {
            "steps": self.step_count,
            "visited_contact": self.visited_contact,
            "login_success": self.login_success,
            "time_elapsed": round(time.time() - self.start_time, 2)
        }

        return obs, reward, done, False, info

    def close(self):
        self.driver.quit()
