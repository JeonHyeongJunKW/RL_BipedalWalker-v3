from math import gamma
import numpy as np
import torch

from torch import nn
from torch.nn import functional as F
from Runner import Runner
from Runner_otherReward2 import Runner_otherReward2
from Critic_and_Actor import Critic, Actor
# helper function to convert numpy arrays to tensors
def t(x):
    x = np.array(x) if not isinstance(x, np.ndarray) else x
    return torch.from_numpy(x).float().cuda() 

def process_memory(memory, gamma=0.99):
    actions = []
    states = []
    next_states = []
    rewards = []
    dones = []

    for action, reward, state, next_state, done in memory:
        actions.append(action)
        rewards.append(reward)
        states.append(state)
        next_states.append(next_state)
        dones.append(done)
    actions = t(actions)
    states = t(states)
    next_states = t(next_states)
    rewards = t(rewards).view(-1, 1)
    dones = t(dones).view(-1, 1)
    return actions, rewards, states, next_states, dones

def clip_grad_norm_(module, max_grad_norm):
    nn.utils.clip_grad_norm_([p for g in module.param_groups for p in g["params"]], max_grad_norm)

class A2CLearner():
  def __init__(self,actor,critic,gamma =0.9, actor_lr=4e-4,critic_lr=4e-3, max_grad_norm =0.5):
    self.gamma = gamma
    self.actor = actor
    self.critic = critic

    self.max_grad_norm = max_grad_norm
    self.actor_optim = torch.optim.Adam(self.actor.parameters(), lr=actor_lr)
    self.critic_optim = torch.optim.Adam(self.critic.parameters(),lr=critic_lr)

  def learn(self,memory,writer, step_i):
    actions, rewards, states, next_states, dones = process_memory(memory,self.gamma)
    
    
    td_target = rewards +self.gamma*self.critic(next_states)*(1-dones)
    
      # print(next_states.shape)

    value = self.critic(states)
    adventage = td_target-value

    norm_dists = self.actor(states)
    logs_probs = norm_dists.log_prob(actions)#특정 행동에 대한 로그확률값을 가져옵니다.
    
    ##actor
    actor_loss = (-logs_probs*adventage.detach()).mean()
    self.actor_optim.zero_grad()
    actor_loss.backward()
    clip_grad_norm_(self.actor_optim,self.max_grad_norm)
    self.actor_optim.step()
    writer.add_scalar("actor_loss", actor_loss.item(), step_i)


    ##critic
    critic_loss = F.mse_loss(td_target,value)
    self.critic_optim.zero_grad()
    critic_loss.backward()
    clip_grad_norm_(self.critic_optim, self.max_grad_norm)
    self.critic_optim.step()
    writer.add_scalar("critic_loss", critic_loss.item(), step_i)

  def A2C_env_run(self,env, max_episode, writer, memory_s,save_folder):
    #환경, 학습 횟수, 시각화도구 

    runner = Runner(env)

    step_on_memory = memory_s
    episodes =max_episode
    episode_length =300
    total_steps = (episode_length*episodes)//step_on_memory
    print("전체 스텝수 : ",total_steps)
    ten = total_steps//30
    for i in range(total_steps):
      memory = runner.run(step_on_memory,self.actor,writer)
      if i%ten ==0:
        torch.save(self.actor.state_dict(),"./model_weight/"+save_folder+"/"+str(i)+" actor.pth")
        torch.save(self.critic.state_dict(),"./model_weight/"+save_folder+"/"+str(i)+" critic.pth")
      self.learn(memory,writer,i)
  
  def view(self,env):
    state = env.reset()
    for i in range(300):
      env.render()
      dists = self.actor(t(state))
      actions = dists.sample().detach().cpu().data.numpy()
      actions_clipped = np.clip(actions, env.action_space.low.min(), env.action_space.high.max())
      next_state, _, done, info = env.step(actions_clipped)
      state = next_state
      if done :
        break



class A2CLearner2():
  def __init__(self,actor,critic,gamma =0.9, actor_lr=4e-4,critic_lr=4e-3, max_grad_norm =0.5):
    self.gamma = gamma
    self.actor = actor
    self.critic = critic

    self.max_grad_norm = max_grad_norm
    self.actor_optim = torch.optim.Adam(self.actor.parameters(), lr=actor_lr)
    self.critic_optim = torch.optim.Adam(self.critic.parameters(),lr=critic_lr)

  def learn(self,memory,writer, step_i):
    actions, rewards, states, next_states, dones = process_memory(memory,self.gamma)
    
    
    td_target = rewards +self.gamma*self.critic(next_states)*(1-dones)
    
      # print(next_states.shape)

    value = self.critic(states)
    adventage = td_target-value

    norm_dists = self.actor(states)
    logs_probs = norm_dists.log_prob(actions)#특정 행동에 대한 로그확률값을 가져옵니다.
    
    ##actor
    actor_loss = (-logs_probs*adventage.detach()).mean()
    self.actor_optim.zero_grad()
    actor_loss.backward()
    clip_grad_norm_(self.actor_optim,self.max_grad_norm)
    self.actor_optim.step()
    writer.add_scalar("actor_loss", actor_loss.item(), step_i)


    ##critic
    critic_loss = F.mse_loss(td_target,value)
    self.critic_optim.zero_grad()
    critic_loss.backward()
    clip_grad_norm_(self.critic_optim, self.max_grad_norm)
    self.critic_optim.step()
    writer.add_scalar("critic_loss", critic_loss.item(), step_i)

  def A2C_env_run(self,env, max_episode, writer, memory_s,save_folder):
    #환경, 학습 횟수, 시각화도구 

    runner = Runner_otherReward(env)

    step_on_memory = memory_s
    episodes =max_episode
    episode_length =300
    total_steps = (episode_length*episodes)//step_on_memory
    print("전체 스텝수 : ",total_steps)
    ten = total_steps//30
    for i in range(total_steps):
      memory = runner.run(step_on_memory,self.actor,writer)
      if i%ten ==0:
        torch.save(self.actor.state_dict(),"./model_weight/"+save_folder+"/"+str(i)+" actor.pth")
        torch.save(self.critic.state_dict(),"./model_weight/"+save_folder+"/"+str(i)+" critic.pth")
      self.learn(memory,writer,i)
  
  def view(self,env):
    state = env.reset()
    for i in range(300):
      env.render()
      dists = self.actor(t(state))
      actions = dists.sample().detach().cpu().data.numpy()
      actions_clipped = np.clip(actions, env.action_space.low.min(), env.action_space.high.max())
      next_state, _, done, info = env.step(actions_clipped)
      state = next_state
      if done :
        break
  

class A2CLearner3():
  def __init__(self,actor,critic,gamma =0.9, actor_lr=4e-4,critic_lr=4e-3, max_grad_norm =0.5):
    self.gamma = gamma
    self.actor = actor
    self.critic = critic

    self.max_grad_norm = max_grad_norm
    self.actor_optim = torch.optim.Adam(self.actor.parameters(), lr=actor_lr)
    self.critic_optim = torch.optim.Adam(self.critic.parameters(),lr=critic_lr)

  def learn(self,memory,writer, step_i):
    actions, rewards, states, next_states, dones = process_memory(memory,self.gamma)
    
    
    td_target = rewards +self.gamma*self.critic(next_states)*(1-dones)
    
      # print(next_states.shape)

    value = self.critic(states)
    adventage = td_target-value

    norm_dists = self.actor(states)
    logs_probs = norm_dists.log_prob(actions)#특정 행동에 대한 로그확률값을 가져옵니다.
    
    ##actor
    actor_loss = (-logs_probs*adventage.detach()).mean()
    self.actor_optim.zero_grad()
    actor_loss.backward()
    clip_grad_norm_(self.actor_optim,self.max_grad_norm)
    self.actor_optim.step()
    writer.add_scalar("actor_loss", actor_loss.item(), step_i)


    ##critic
    critic_loss = F.mse_loss(td_target,value)
    self.critic_optim.zero_grad()
    critic_loss.backward()
    clip_grad_norm_(self.critic_optim, self.max_grad_norm)
    self.critic_optim.step()
    writer.add_scalar("critic_loss", critic_loss.item(), step_i)

  def A2C_env_run(self,env, max_episode, writer, memory_s,save_folder):
    #환경, 학습 횟수, 시각화도구 

    runner = Runner_otherReward2(env)

    step_on_memory = memory_s
    episodes =max_episode
    episode_length =300
    total_steps = (episode_length*episodes)//step_on_memory
    print("전체 스텝수 : ",total_steps)
    ten = total_steps//30
    for i in range(total_steps):
      memory = runner.run(step_on_memory,self.actor,writer)
      if i%ten ==0:
        torch.save(self.actor.state_dict(),"./model_weight/"+save_folder+"/"+str(i)+" actor.pth")
        torch.save(self.critic.state_dict(),"./model_weight/"+save_folder+"/"+str(i)+" critic.pth")
      self.learn(memory,writer,i)
  
  def view(self,env):
    state = env.reset()
    for i in range(300):
      env.render()
      dists = self.actor(t(state))
      actions = dists.sample().detach().cpu().data.numpy()
      actions_clipped = np.clip(actions, env.action_space.low.min(), env.action_space.high.max())
      next_state, _, done, info = env.step(actions_clipped)
      state = next_state
      if done :
        break