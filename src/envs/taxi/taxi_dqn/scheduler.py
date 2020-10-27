from mesa.time import BaseScheduler

from taxi_dqn.agents import TaxiAgent, PassengerAgent, LocationAgent

class RLActivation(BaseScheduler):
    """ 
    A scheduler which activates each agent once per step, in random order,
    """

    def __init__(self, model, rl_agent) -> None:
         super().__init__(model)
         self.rl_agent = rl_agent


    def step(self) -> None:
        """ 
        Executes the step of all agents, one at a time, in random order.
        """
        action = self.rl_agent.forward(self.model.env.s)
        observation, rewards, done, info = self.model.env.step(action)

        self.model.env.s = observation
        print(observation, rewards, done, info)
        
        if done:
            self.rl_agent.forward(observation)
            self.rl_agent.backward(0., terminal=False)
       
        taxi_x, taxi_y, pass_index, dest_index = self.model.env.decode(self.model.env.s)

        for agent in self.agent_buffer(shuffled=True):
            if type(agent) is TaxiAgent:
                agent.step((taxi_x, taxi_y))
            elif type(agent) is PassengerAgent:
                coords = (taxi_x, taxi_y) if pass_index == 4 else self.model.locations[pass_index]
                agent.step(coords)
                
        self.steps += 1
        self.time += 1
