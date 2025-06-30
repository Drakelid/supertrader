"""High level reinforcement learning agent wrapper."""

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from ..trading.engine import TradingEngine

class RLAgent:
    """Thin wrapper around a Stable-Baselines3 model."""

    def __init__(self, env, model_path: str = "agent.zip") -> None:
        self.env = env
        self.model_path = model_path
        self.model = PPO("MlpPolicy", self.env, verbose=0)

    def train(self, timesteps: int = 1000) -> None:
        """Train the underlying model and save it."""
        self.model.learn(total_timesteps=timesteps)
        self.model.save(self.model_path)

    def load(self) -> None:
        """Load the model from ``self.model_path``."""
        self.model = PPO.load(self.model_path, env=self.env)

    def act(self, obs):
        """Return the model's action for a given observation."""
        action, _ = self.model.predict(obs)
        return action
