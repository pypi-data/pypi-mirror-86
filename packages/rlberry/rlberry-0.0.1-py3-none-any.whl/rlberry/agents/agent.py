from abc import ABC, abstractmethod
from copy import deepcopy


class Agent(ABC):
    """
    Basic interface for agents.

    Input environment is (deep)copied and reseeded.

    Notes
    ------
        Classes that implement this class should send **kwargs to
        Agent.__init__()


    Attributes
    ----------
    name : string
        agent identifier
    fit_info : tuple
        tuple of strings containing the keys in the dictionary
        returned by fit()
    env : rlberry.envs.interface.model.Model
        environment on which to train the agent


    Methods
    --------
    fit(**kwargs), abstract
        train the agent, returns dictionary with training info,
        whose keys are strings
    policy(observation, **kwargs), abstract
        returns the action to be taken given an observation
    reset()
        puts the agent in default setup (optional)
    sample_parameters(), optional
        returns dictionary with sampled hyperparameters.
    save(), optional
        save agent
    load(), optional
        load agent, returns an instance of the agent
    """

    name = ""
    fit_info = ()

    def __init__(self, env, copy_env=True,
                 reseed_env=True, **kwargs):
        """
        Parameters
        ----------
        env : Model
            Environment used to fit the agent.
        copy_env : bool
            If true, makes a deep copy of the environment.
        reseed_env : bool
            If true, reseeds the environment.
        """
        if copy_env:
            self.env = deepcopy(env)
        else:
            self.env = env
        if reseed_env:
            self.env.reseed()

    @abstractmethod
    def fit(self, **kwargs):
        """Train the agent using the provided environment."""
        pass

    @abstractmethod
    def policy(self, observation, **kwargs):
        """Returns an action, given an observation."""
        pass

    def reset(self, **kwargs):
        """Put the agent in default setup."""
        pass

    def save(self, **kwargs):
        """Save agent object."""
        raise NotImplementedError("agent.save() not implemented.")

    def load(self, **kwargs):
        """Load agent object."""
        raise NotImplementedError("agent.load() not implemented.")

    @classmethod
    def sample_parameters(cls, trial):
        """
        Sample hyperparameters for hyperparam optimization using
        Optuna (https://optuna.org/)

        Note: only the kwargs sent to __init__ are optimized. Make sure to
        include in the Agent constructor all "optimizable" parameters.

        Parameters
        ----------
        trial: optuna.trial
        """
        raise NotImplementedError("agent.sample_parameters() not implemented.")
