from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from ..trading.engine import TradingEngine

class RLAgent:
    def __init__(self, env, model_path: str = "agent.zip"):
        self.env = env
        self.model_path = model_path
        self.model = PPO("MlpPolicy", self.env, verbose=0)

    def train(self, timesteps: int = 1000):
        self.model.learn(total_timesteps=timesteps)
        self.model.save(self.model_path)

    def load(self):
        self.model = PPO.load(self.model_path, env=self.env)

    def act(self, obs):
        action, _ = self.model.predict(obs)
        return action
