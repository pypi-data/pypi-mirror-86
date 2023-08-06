from gym.spaces import Discrete, Box
import numpy as np
import warnings
import magent
from pettingzoo import AECEnv
import math
from pettingzoo.magent.render import Renderer
from pettingzoo.utils import agent_selector
from .magent_env import magent_parallel_env, make_env
from pettingzoo.utils._parallel_env import _parallel_env_wrapper
from pettingzoo.utils.to_parallel import parallel_wrapper_fn
from gym.utils import EzPickle


map_size = 45
max_cycles_default = 300
minimap_mode = False


def parallel_env(max_cycles=max_cycles_default):
    return _parallel_env(map_size, max_cycles)


def raw_env(max_cycles=max_cycles_default):
    return _parallel_env_wrapper(_parallel_env(map_size, max_cycles))


env = make_env(raw_env)


def get_config(map_size):
    gw = magent.gridworld
    cfg = gw.Config()

    cfg.set({"map_width": map_size, "map_height": map_size})
    cfg.set({"embedding_size": 10})
    cfg.set({"minimap_mode": minimap_mode})

    options = {
        'width': 1, 'length': 1, 'hp': 5, 'speed': 1,
        'view_range': gw.CircleRange(1), 'attack_range': gw.CircleRange(0),
        'step_recover': 0.2,
        'kill_supply': 8, 'dead_penalty': -1.,
    }

    deer = cfg.register_agent_type(
        "deer",
        options)

    options = {
        'width': 1, 'length': 1, 'hp': 10, 'speed': 1,
        'view_range': gw.CircleRange(4), 'attack_range': gw.CircleRange(1),
        'damage': 1, 'step_recover': -0.2
    }
    tiger = cfg.register_agent_type(
        "tiger",
        options)

    deer_group = cfg.add_group(deer)
    tiger_group = cfg.add_group(tiger)

    a = gw.AgentSymbol(tiger_group, index='any')
    b = gw.AgentSymbol(tiger_group, index='any')
    c = gw.AgentSymbol(deer_group, index='any')

    # tigers get reward when they attack a deer simultaneously
    e1 = gw.Event(a, 'attack', c)
    e2 = gw.Event(b, 'attack', c)
    cfg.add_reward_rule(e1 & e2, receiver=[a, b], value=[1, 1])

    return cfg


class _parallel_env(magent_parallel_env, EzPickle):
    def __init__(self, map_size, max_cycles):
        EzPickle.__init__(self, map_size, max_cycles)
        env = magent.GridWorld(get_config(map_size), map_size=map_size)

        handles = env.get_handles()
        reward_range = [-1, 2]

        names = ["deer", "tiger"]
        super().__init__(env, handles, names, map_size, max_cycles, reward_range, minimap_mode)

    def generate_map(self):
        env, map_size = self.env, self.map_size
        handles = env.get_handles()

        env.add_walls(method="random", n=map_size * map_size * 0.04)
        env.add_agents(handles[0], method="random", n=map_size * map_size * 0.05)
        env.add_agents(handles[1], method="random", n=map_size * map_size * 0.01)
