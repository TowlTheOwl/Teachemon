import gymnasium as gym
import numpy as np
from sb3_contrib.ppo_mask import MaskablePPO
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker

from battleEnv import BattleGymEnv  # Replace with your actual path/module

# === Wrapper to support single-agent training against a random opponent ===
class SinglePlayerWrapper(gym.Env):
    def __init__(self, env:BattleGymEnv):
        super().__init__()
        self.env = env
        self.action_space = env.action_space
        self.observation_space = env.observation_space

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        return obs, info

    def step(self, action):
        # Get Player 1's random (but valid) action
        opponent_action = self.random_policy()
        obs, rewards, done, truncated, info = self.env.step([action, opponent_action])
        return obs, rewards[0], done, truncated, info

    def random_policy(self):
        mask = self.env.get_action_mask(1)
        valid_actions = [i for i, valid in enumerate(mask) if valid]
        return np.random.choice(valid_actions)
    
    def render(self):
        self.env.render()

    def get_action_mask(self, player=0):
        return self.env.get_action_mask(player)

# === Environment with Action Masking ===
class MaskedEnv(SinglePlayerWrapper):
    def __init__(self, env):
        super().__init__(env)

    def get_action_mask(self, player=0):
        return self.env.get_action_mask(player)

# === Create and Train the Agent ===
def mask_fn(env: gym.Env) -> np.ndarray:
    return env.get_action_mask()  # Assuming you're training Player 0

def train_agent():
    base_env = BattleGymEnv()
    env = MaskedEnv(base_env)
    env = ActionMasker(env, mask_fn)

    model = MaskablePPO(
        MaskableActorCriticPolicy,
        env,
        verbose=1,
        tensorboard_log="./ppo_teachemon_tensorboard/"
    )

    model.learn(total_timesteps=100_000)
    model.save("ppo_teachemon")

    return model, env

# === Play/Evaluate the Agent ===
def evaluate(model, env:ActionMasker, episodes=5):
    for ep in range(episodes):
        obs, info = env.reset()
        done = False
        total_reward = 0
        while not done:
            mask = env.env.get_action_mask()
            action, _ = model.predict(obs, action_masks=mask)
            obs, reward, done, truncated, info= env.step(action)
            env.env.render()
            total_reward += reward
        print(f"Episode {ep+1} reward: {total_reward}")

# === Run Training + Evaluation ===
if __name__ == "__main__":
    model, env = train_agent()
    evaluate(model, env)
