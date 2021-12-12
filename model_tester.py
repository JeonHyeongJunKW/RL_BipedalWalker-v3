from Critic_and_Actor import Actor,Actor_best
import gym
import numpy as np
import torch
def t(x):
    x = np.array(x) if not isinstance(x, np.ndarray) else x
    return torch.from_numpy(x).float()

def model_tester(mode_name,type,state_dim=24,n_actions=4):
  if type =="best":
    test_model = Actor_best(state_dim,n_actions)
  elif type =="origin":
    test_model = Actor(state_dim,n_actions)
  test_model.load_state_dict('./model_weight/'+mode_name)
  test_model.eval()
  env = gym.make('BipedalWalker-v3')
  state = env.reset()
  for i in range(300):
    env.render()
    dists = test_model(t(state))
    actions = dists.sample().detach().data.numpy()
    actions_clipped = np.clip(actions, env.action_space.low.min(), env.action_space.high.max())
    next_state, _, done, _ = env.step(actions_clipped)
    state = next_state
    if done :
      break