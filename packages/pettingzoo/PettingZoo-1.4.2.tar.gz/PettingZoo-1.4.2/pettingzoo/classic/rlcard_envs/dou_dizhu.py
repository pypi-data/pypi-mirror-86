from pettingzoo import AECEnv
from pettingzoo.utils.agent_selector import agent_selector
from gym import spaces
import rlcard
import random
import numpy as np
from pettingzoo.utils import wrappers
from .rlcard_base import RLCardBase


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.CaptureStdoutWrapper(env)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    pass_move = 308
    env = wrappers.NanNoOpWrapper(env, pass_move, "passing turn with action number {}".format(pass_move))
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class raw_env(RLCardBase):

    metadata = {'render.modes': ['human']}

    def __init__(self, opponents_hand_visible=False):
        self._opponents_hand_visible = opponents_hand_visible
        self.agents = ['landlord_0', 'peasant_0', 'peasant_1']
        num_planes = 6 if self._opponents_hand_visible else 4
        super().__init__("doudizhu", 3, (num_planes, 5, 15))

    def _scale_rewards(self, reward):
        # Maps 1 to 1 and 0 to -1
        return 2 * reward - 1

    def observe(self, agent):
        obs = self.env.get_state(self._name_to_int(agent))
        if self._opponents_hand_visible:
            return obs['obs'].astype(self._dtype)
        else:
            return obs['obs'][[0, 2, 3, 4], :, :].astype(self._dtype)

    def render(self, mode='human'):
        for player in self.possible_agents:
            state = self.env.game.get_state(self._name_to_int(player))
            print("\n===== {}'s Hand =====".format(player))
            print(state['current_hand'])
        print('\n=========== Last 3 Actions ===========')
        for action in state['trace'][:-4:-1]:
            print('{}: {}'.format(self._int_to_name(action[0]), action[1]))
        print('\n')
