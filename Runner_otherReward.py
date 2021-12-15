from math import gamma
import numpy as np
import torch
import gym
from torch import nn
from torch.nn import functional as F

def GetReward(reward, next_state):
  data = next_state[14:24]
  applied_reward = (min(data.tolist()))/10
  return reward+applied_reward

def t(x):
    x = np.array(x) if not isinstance(x, np.ndarray) else x
    return torch.from_numpy(x).float().cuda() 

class Runner_otherReward():
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



  def run(self, max_steps, actor, writer,memory=None):
    if not memory :memory = []
    for i in range(max_steps):
      if self.done : self.reset()

      dists = actor(t(self.state))
      actions = dists.sample().detach().cpu().data.numpy()
      actions_clipped = np.clip(actions, self.env.action_space.low.min(), self.env.action_space.high.max())
      next_state, reward, self.done, info = self.env.step(actions_clipped)
      memory.append((actions, GetReward(reward,next_state), self.state, next_state, self.done))
      self.state = next_state
      self.steps += 1
      self.episode_reward += reward#GetReward(reward,next_state)
      if self.done:
        self.episode_rewards.append(self.episode_reward)
        if len(self.episode_rewards) % 10 == 0:
            # print("episode:", len(self.episode_rewards), ", episode reward:", self.episode_reward)
            writer.add_scalar("Episode Reward/train", self.episode_reward,len(self.episode_rewards))
    return memory
