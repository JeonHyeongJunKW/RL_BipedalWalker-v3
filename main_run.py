from learning import A2CLearner
from Critic_and_Actor import Critic, Actor
import gym
env = gym.make('BipedalWalker-v3')
state_dim = env.observation_space.shape[0]
n_actions = env.action_space.shape[0]

actor = Actor(state_dim, n_actions)
critic = Critic(state_dim)

learner = A2CLearner(actor, critic)
learner.A2C_env_run(env)

#학습다돌리고 10번정도 확인하기
for j in range(10):
  learner.view(env)