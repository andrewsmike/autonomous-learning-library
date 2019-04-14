# /Users/cpnota/repos/autonomous-learning-library/all/approximation/value/action/torch.py
import torch
from torch import nn
from torch.optim import Adam
from all.layers import Flatten
from all.agents import REINFORCE
from all.approximation import ValueNetwork
from all.experiments import DummyWriter
from all.policies import SoftmaxPolicy


def fc_value(env):
    return nn.Sequential(
        Flatten(),
        nn.Linear(env.state_space.shape[0], 256),
        nn.ReLU(),
        nn.Linear(256, 1)
    )


def fc_policy(env):
    return nn.Sequential(
        Flatten(),
        nn.Linear(env.state_space.shape[0], 256),
        nn.ReLU(),
        nn.Linear(256, env.action_space.n)
    )


def reinforce(
        lr_v=1e-3,
        lr_pi=1e-3,
        device=torch.device('cpu')
):
    def _reinforce(env, writer=DummyWriter()):
        value_model = fc_value(env).to(device)
        value_optimizer = Adam(value_model.parameters(), lr=lr_v)
        v = ValueNetwork(value_model, value_optimizer, writer=writer)
        policy_model = fc_policy(env).to(device)
        policy_optimizer = Adam(policy_model.parameters(), lr=lr_pi)
        policy = SoftmaxPolicy(
            policy_model,
            policy_optimizer,
            env.action_space.n,
            writer=writer
        )
        return REINFORCE(v, policy)
    return _reinforce


__all__ = ["reinforce"]