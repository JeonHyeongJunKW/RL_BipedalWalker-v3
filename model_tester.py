from Critic_and_Actor import Actor,Actor_best
import gym
import numpy as np
import torch
def t(x):
    x = np.array(x) if not isinstance(x, np.ndarray) else x
    return torch.from_numpy(x).float()

def model_tester(mode_name,type,std,state_dim=24,n_actions=4):
  if type =="best":
    test_model = Actor_best(state_dim,n_actions,0.4)
  elif type =="origin":
    test_model = Actor(state_dim,n_actions)
  model_name = './model_weight/'+mode_name
  print(model_name)
  test_model.load_state_dict(torch.load(model_name))
  test_model.eval()
  env = gym.make('BipedalWalker-v3')
  state = env.reset()
  for j in range(10):
    state = env.reset()
    re_sum =0
    while True:
      env.render()
      dists = test_model(t(state))
      actions = dists.sample().detach().cpu().data.numpy()
      actions_clipped = np.clip(actions, env.action_space.low.min(), env.action_space.high.max())
      next_state, reward, done, _ = env.step(actions_clipped)
      re_sum +=reward
      # print("done? ", done)
      print("실시간 보상 : ",reward, "보상 합 : ",re_sum)
      state = next_state
      if done :
        break
  env.close()