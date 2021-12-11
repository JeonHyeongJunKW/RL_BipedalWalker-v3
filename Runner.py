from math import gamma
import numpy as np
import torch
import gym
from torch import nn
from torch.nn import functional as F
from Reward import GetReward
def t(x):
    x = np.array(x) if not isinstance(x, np.ndarray) else x
    return torch.from_numpy(x).float()

class Runner():
  def __init__(self, env):
    self.env = env
    self.state = None
    self.done = True
    self.steps =0
    self.episode_reward = 0
    self.episode_rewards = []
  
  def reset(self):
    self.episode_reward = 0
    self.done = False
    self.state = self.env.reset()
    self.steps = 0



  def run(self, max_steps, actor , memory=None):
    if not memory :memory = []
    for i in range(max_steps):
      if self.done : self.reset()

      dists = actor(t(self.state))
      actions = dists.sample().detach().data.numpy()
      actions_clipped = np.clip(actions, self.env.action_space.low.min(), self.env.action_space.high.max())
      next_state, reward, self.done, info = self.env.step(actions_clipped)
      memory.append((actions, GetReward(reward), self.state, next_state, self.done))
      self.state = next_state
      self.steps += 1
      self.episode_reward += GetReward(reward)
      if self.done:
        self.episode_rewards.append(self.episode_reward)
        if len(self.episode_rewards) % 10 == 0:
            print("episode:", len(self.episode_rewards), ", episode reward:", self.episode_reward)
            print(self.steps)
    return memory
