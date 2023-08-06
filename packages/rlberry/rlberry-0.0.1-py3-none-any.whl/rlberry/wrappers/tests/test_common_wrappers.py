import numpy as np
import pytest
import rlberry.seeding as seeding

from rlberry.envs.classic_control import MountainCar
from rlberry.envs.finite import FiniteMDP
from rlberry.wrappers.discretize_state import DiscretizeStateWrapper
from rlberry.wrappers.rescale_reward import RescaleRewardWrapper
from rlberry.wrappers.autoreset import AutoResetWrapper


@pytest.mark.parametrize("n_bins", list(range(1, 10)))
def test_discretizer(n_bins):
    env = DiscretizeStateWrapper(MountainCar(), n_bins)
    assert env.observation_space.n == n_bins * n_bins

    for _ in range(2):
        state = env.reset()
        for _ in range(50):
            assert env.observation_space.contains(state)
            action = env.action_space.sample()
            next_s, _, _, _ = env.step(action)
            state = next_s

    for _ in range(100):
        state = env.observation_space.sample()
        action = env.action_space.sample()
        next_s, _, _, _ = env.sample(state, action)
        assert env.observation_space.contains(next_s)

    assert env.unwrapped.name == "MountainCar"


def test_rescale_reward():
    # tolerance
    tol = 1e-14

    rng = seeding.get_rng()

    for _ in range(10):
        # generate random MDP
        S, A = 5, 2
        R = rng.uniform(0.0, 1.0, (S, A))
        P = rng.uniform(0.0, 1.0, (S, A, S))
        for ss in range(S):
            for aa in range(A):
                P[ss, aa, :] /= P[ss, aa, :].sum()
        env = FiniteMDP(R, P)

        # test
        wrapped = RescaleRewardWrapper(env, (-10, 10))
        _ = wrapped.reset()
        for _ in range(100):
            _, reward, _, _ = wrapped.sample(
                wrapped.observation_space.sample(),
                wrapped.action_space.sample())
            assert reward <= 10+tol and reward >= -10-tol

        _ = wrapped.reset()
        for _ in range(100):
            _, reward, _, _ = wrapped.step(wrapped.action_space.sample())
            assert reward <= 10+tol and reward >= -10-tol


@pytest.mark.parametrize("rmin, rmax", [(0, 1), (-1, 1), (-5, 5), (-5, 15)])
def test_rescale_reward_2(rmin, rmax):
    # tolerance
    tol = 1e-15

    # dummy MDP
    S, A = 5, 2
    R = np.ones((S, A))
    P = np.ones((S, A, S))
    for ss in range(S):
        for aa in range(A):
            P[ss, aa, :] /= P[ss, aa, :].sum()
    env = FiniteMDP(R, P)

    # test bounded case
    env.reward_range = (-100, 50)
    wrapped = RescaleRewardWrapper(env, (rmin, rmax))
    xx = np.linspace(-100, 50, num=100)
    for x in xx:
        y = wrapped._rescale(x)
        assert y >= rmin-tol and y <= rmax+tol

    # test unbounded above
    env.reward_range = (-1.0, np.inf)
    wrapped = RescaleRewardWrapper(env, (rmin, rmax))
    xx = np.linspace(-1, 1e2, num=100)
    for x in xx:
        y = wrapped._rescale(x)
        assert y >= rmin-tol and y <= rmax+tol

    # test unbounded below
    env.reward_range = (-np.inf, 1.0)
    wrapped = RescaleRewardWrapper(env, (rmin, rmax))
    xx = np.linspace(-1e2, 1, num=100)
    for x in xx:
        y = wrapped._rescale(x)
        assert y >= rmin-tol and y <= rmax+tol

    # test unbounded
    env.reward_range = (-np.inf, np.inf)
    wrapped = RescaleRewardWrapper(env, (rmin, rmax))
    xx = np.linspace(-1e2, 1e2, num=200)
    for x in xx:
        y = wrapped._rescale(x)
        assert y >= rmin-tol and y <= rmax+tol


@pytest.mark.parametrize("horizon", list(range(1, 10)))
def test_autoreset(horizon):

    # dummy MDP
    S, A = 5, 2
    R = np.ones((S, A))
    P = np.ones((S, A, S))
    for ss in range(S):
        for aa in range(A):
            P[ss, aa, :] /= P[ss, aa, :].sum()
    # initial state = 3
    env = FiniteMDP(R, P, initial_state_distribution=3)
    env = AutoResetWrapper(env, horizon)

    env.reset()
    for tt in range(5*horizon+1):
        action = env.action_space.sample()
        next_s, reward, done, info = env.step(action)
        if (tt+1) % horizon == 0:
            assert next_s == 3
