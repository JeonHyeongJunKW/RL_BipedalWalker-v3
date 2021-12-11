import numpy
import torch
import gym
from torch import nn
from torch.nn import functional as F
# from torch.utils.tensorboard 

class Critic(nn.Module):
  def __init__(self, state_dim, activation=nn.Tanh):
    super().__init__()
    
    self.model = nn.Sequential(
      nn.Linear(state_dim,64),
      activation(),
      nn.Linear(64,64),
      activation(),
      nn.Linear(64,1),
    )
  def forward(self,X):
    return self.model(X)



class Actor(nn.Module):
  def __init__(self,state_dim, n_actions, activation=nn.Tanh):
    super().__init__()
    self.n_actions =n_actions
    self.std = nn.Parameter(torch.full((n_actions,),0.1))
    self.model = nn.Sequential(
      nn.Linear(state_dim,64),
      activation(),
      nn.Linear(64,64),
      activation(),
      nn.Linear(64,n_actions)## 모델의 평균수만큼 반환합니다.
    )
  def forward(self,X):
    means = self.model(X)
    stds = torch.clamp(self.std.exp(),1e-3,50)#편차의 범위를 바꿔버린다.

    return torch.distributions.Normal(means,stds)


    