import gym
env = gym.make('BipedalWalker-v3')
goal_steps =500

for episode in range(10):#훈련수가 10번인건가 
  obs = env.reset()
  while True:
    
    for i in range(goal_steps):
      env.render()
      action = env.action_space.sample()
      next_state, reward, done, info = env.step(action)
      if done :#넘어져버림 
        break
