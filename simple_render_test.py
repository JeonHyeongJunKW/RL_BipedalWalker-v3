import gym
env = gym.make('BipedalWalker-v3')

goal_steps =500
while True:
  obs = env.reset()
  for i in range(goal_steps):
    env.render()
    env.step(env.action_space.sample()) #
