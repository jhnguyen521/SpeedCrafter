try:
    from malmo import MalmoPython
except:
    import MalmoPython

import sys
import time
import json
import matplotlib.pyplot as plt
import numpy as np

import gym, ray
from gym.spaces import Discrete, Box
from ray.rllib.agents import sac

class SpeedCrafter(gym.Env):
    def __init__(self, env_config):
        # Static Parameters
        self.agent_start = [-192.5, 68.5, 182.5]

        self.size = 15
        self.obs_size = 5
        self.max_episode_steps = 100
        self.log_frequency = 10
        self.action_dict = {
            0: 'jumpmove 1',  # jump forward
            1: 'turn 1',  # Turn 90 degrees to the right
            2: 'turn -1',  # Turn 90 degrees to the left
            3: 'look 1',  # look down 45 degrees
            4: 'look -1',  # look up 45 degrees
            5: 'attack 1'
        }

        # RLlib Parameters
        self.action_space = Discrete(len(self.action_dict))
        self.observation_space = Box(0, 1, shape=(np.prod([self.obs_size, self.obs_size, self.obs_size]), ), dtype=np.int32)

        # Malmo Parameters
        self.agent_host = MalmoPython.AgentHost()
        try:
            self.agent_host.parse(sys.argv)
        except RuntimeError as e:
            print('ERROR:', e)
            print(self.agent_host.getUsage())
            exit(1)

        # SpeedCrafter Parameters
        self.resources = {'log': 2} # # resource: # needed TODO: UPDATE BASED ON TARGET ITEM
        self.pitch = 0
        self.pos = [-192.5, 68.5, 182.5]
        self.target_item = ''
        self.inventory = dict()

        self.target_pos = None
        self.last_dist = float('inf')
        self.dist = float('inf')

        self.obs = None
        self.episode_step = 0
        self.episode_return = 0
        self.returns = []
        self.steps = []

    def reset(self) -> np.array:
        """
        Resets the env for next episode

        :return:
        <np.array> flattened initial observation
        """

        # Reset Malmo
        world_state = self.init_malmo()

        # Reset Variables
        self.returns.append(self.episode_return)
        current_step = self.steps[-1] if len(self.steps) > 0 else 0
        self.steps.append(current_step + self.episode_step)
        self.episode_return = 0
        self.episode_step = 0

        self.resources = {'log': 2} # # resource: # needed TODO: UPDATE BASED ON TARGET ITEM
        self.pitch = 0
        self.pos = [-192.5, 68.5, 182.5]
        self.inventory = dict()
        self.target_pos = None
        self.last_dist = float('inf')
        self.dist = float('inf')

        # Log
        if len(self.returns) > self.log_frequency and \
            len(self.returns) % self.log_frequency == 0:
                self.log_returns()

        # Get Observation
        self.obs = self.get_observation(world_state)

        return self.obs.flatten()

    def step(self, action):
        """
                Take an action in the environment and return the results.

                Args
                    action: <int> index of the action to take

                Returns
                    observation: <np.array> flattened array of obseravtion
                    reward: <int> reward from taking action
                    done: <bool> indicates terminal state
                    info: <dict> dictionary of extra information
                """

        # Get Action
        command = self.action_dict[action]
        # allow_break_action = (self.obs[1, int(self.obs_size / 2) - 1, int(self.obs_size / 2)] == 1 and self.pitch == 45) \
        #                      or (self.obs[2, int(self.obs_size / 2) - 1, int(self.obs_size / 2)] == 1 and self.pitch == 0) \
        #                      or (self.obs[3, int(self.obs_size / 2) - 1, int(self.obs_size / 2)] == 1 and self.pitch == -45)
        #
        #
        # if allow_break_action:
        #     print(self.obs[0])
        #     print(self.obs[1])
        #     print(self.obs[2])
        #     self.agent_host.sendCommand('attack 1')
        #     time.sleep(.1)
        #     self.episode_step += 1
        if (command == 'look 1' and self.pitch == 45) or (command == 'look -1' and self.pitch == -45):
            # Don't send action
            print('Not sending action')
            pass
        else:
            self.agent_host.sendCommand(command)
            time.sleep(.1)
            self.episode_step += 1



        # Get Done
        done = False
        crafted_item = False
        enough_resources = self.enough_resources()
        if self.episode_step >= self.max_episode_steps or enough_resources: # TODO: FIX BUG WITH: Error starting mission: A mission is already running.
            done = True
            if enough_resources:
                crafted_item = True
            time.sleep(0.5)

            # Gt Observation
        world_state = self.agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:", error.text)
        self.obs = self.get_observation(world_state)

        # Get Reward
        reward = 0
        for r in world_state.rewards:
            reward += r.getValue()

        # Reward according to distance
        if self.dist < self.last_dist:
            reward += 1
        elif self.dist > self.last_dist:
            reward -= 1

        if crafted_item:
            print('Collected enough resources to craft item')
            reward += 1000

        self.episode_return += reward


        return self.obs.flatten(), reward, done, dict()

    def get_mission_xml(self):
        return '''<?xml version="1.0" encoding="UTF-8" ?>
                    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <About>
                            <Summary>Crafter Agent</Summary>
                        </About>

                        <ServerSection>
                            <ServerInitialConditions>
                                <Time>
                                    <StartTime>8000</StartTime>
                                    <AllowPassageOfTime>false</AllowPassageOfTime>
                                </Time>
                                <Weather>clear</Weather>
                            </ServerInitialConditions>
                            <ServerHandlers>
                                <DefaultWorldGenerator seed="996181341395652" forceReset="true"/>
                                <DrawingDecorator>''' + \
               "<DrawCuboid x1='{}' x2='{}' y1='0' y2='100' z1='{}' z2='{}' type='air'/>".format(
                   int(self.agent_start[0] - self.size), int(self.agent_start[0] - self.size - 10), int(self.agent_start[2] - self.size - 10),
                   int(self.agent_start[2] + self.size + 10)) + \
               "<DrawCuboid x1='{}' x2='{}' y1='0' y2='100' z1='{}' z2='{}' type='air'/>".format(
                   int(self.agent_start[0] + self.size), int(self.agent_start[0] + self.size + 10), int(self.agent_start[2] - self.size - 10),
                   int(self.agent_start[2] + self.size + 10)) + \
               "<DrawCuboid x1='{}' x2='{}' y1='0' y2='100' z1='{}' z2='{}' type='air'/>".format(
                   int(self.agent_start[0] - self.size - 10), int(self.agent_start[0] + self.size + 10), int(self.agent_start[2] - self.size),
                   int(self.agent_start[2] - self.size - 10)) + \
               "<DrawCuboid x1='{}' x2='{}' y1='0' y2='100' z1='{}' z2='{}' type='air'/>".format(
                   int(self.agent_start[0] - self.size - 10), int(self.agent_start[0] + self.size + 10), int(self.agent_start[2] + self.size),
                   int(self.agent_start[2] + self.size + 10)) + \
               '''
               </DrawingDecorator>
               <ServerQuitWhenAnyAgentFinishes />
           </ServerHandlers>
       </ServerSection>

       <AgentSection mode="Survival">
           <Name>Crafter</Name>
           <AgentStart>''' + \
               "<Placement x='{}' y='{}' z='{}'/>".format(self.agent_start[0], self.agent_start[1], self.agent_start[2]) + \
               '''
           </AgentStart>
                <AgentHandlers>
                    <DiscreteMovementCommands/>
                    <SimpleCraftCommands/>
                    <ObservationFromFullStats/>
                    <ObservationFromHotBar/>
                    <ObservationFromGrid>
                    <Grid name="floorAll">
                            <min x="-''' + str(int(self.obs_size / 2)) + '''" y="-''' + str(int(self.obs_size / 2)) + '''" z="-''' + str(int(self.obs_size / 2)) + '''"/>
                            <max x="''' + str(int(self.obs_size / 2)) + '''" y="''' + str(int(self.obs_size / 2)) + '''" z="''' + str(int(self.obs_size / 2)) + '''"/>
                    </Grid>
                    </ObservationFromGrid>
                    <RewardForCollectingItem>
                        <Item type="log" reward="100"/>
                        <Item type="dirt" reward="-1"/>
                    </RewardForCollectingItem> 
                    <RewardForSendingCommand reward="-1"/>
                    <AgentQuitFromReachingCommandQuota total="'''+str(self.max_episode_steps)+'''" />
                </AgentHandlers>            
        </AgentSection>
    </Mission>'''

    def init_malmo(self):
        """
        Initialize new malmo mission
        """
        my_mission = MalmoPython.MissionSpec(self.get_mission_xml(), True)
        my_mission_record = MalmoPython.MissionRecordSpec()
        my_mission.setViewpoint(1)

        max_retries = 3
        my_clients = MalmoPython.ClientPool()
        my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000)) # add Minecraft machines here as available

        for retry in range(max_retries):
            try:
                self.agent_host.startMission(my_mission, my_clients, my_mission_record, 0, 'SpeedCrafter')
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:", e)
                    exit(1)
                else:
                    time.sleep(2)

        world_state = self.agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                print("\nError:", error.text)

        return world_state

    def calc_dist(self, p1, p2):
        return np.sqrt(np.sum((np.array(p1)-np.array(p2))**2, axis=0))

    def calc_pos_from_obs(self, obs_coord):
        p = [int(self.pos[0] - (int(self.obs_size/2)-obs_coord[0])),
             int(self.pos[1] - (int(self.obs_size/2)-obs_coord[1])),
             int(self.pos[2] - (int(self.obs_size/2)-obs_coord[2]))]
        d = self.calc_dist(self.pos, p)
        return p,d

    def enough_resources(self):
        for r in self.resources:
            if r not in self.inventory:
                return False
            else:
                if self.inventory[r] < self.resources[r]:
                    return False
        return True


    def get_observation(self, world_state):
        """
                Use the agent observation API to get a 5 x 5 x 5 grid around the agent.
                The agent is in the center square facing up.

                Args
                    world_state: <object> current agent world state

                Returns
                    observation: <np.array>
                """
        obs = np.zeros((self.obs_size, self.obs_size, self.obs_size))

        while world_state.is_mission_running:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            if len(world_state.errors) > 0:
                raise AssertionError('Could not load grid.')

            if world_state.number_of_observations_since_last_state > 0:
                # First we get the json from the observation API
                msg = world_state.observations[-1].text
                observations = json.loads(msg)

                # Update position
                self.pos = [observations['XPos'], observations['YPos'], observations['ZPos']]
                if self.target_pos:
                    self.last_dist = self.dist
                    self.dist = self.calc_dist(self.pos, self.target_pos)

                grid = observations['floorAll']
                grid_binary = [1 if x in self.resources else 0 for x in grid] #TODO: Update this

                obs = np.reshape(grid_binary, (self.obs_size, self.obs_size, self.obs_size))

                # Find closest resource
                coords = np.argwhere(obs == 1)
                if coords.size > 0 and self.target_pos is None:
                    min_dist = float('inf')
                    curr_coord = None
                    print("No target resource, checking if found a potential one.")
                    for c in coords:
                        p,d = self.calc_pos_from_obs(c)
                        if d < min_dist:
                            curr_coord,min_dist = p,d
                    self.target_pos = curr_coord
                    self.dist = min_dist
                    print(f"Current Pos: {self.pos}")
                    print(f"Found a resources at {self.target_pos} and distance of {min_dist}")

                # Update pitch of agent
                self.pitch = observations['Pitch']

                # Rotate observation with orientation of agent
                yaw = observations['Yaw']
                if yaw == 270:
                    obs = np.rot90(obs, k=1, axes=(1, 2))
                elif yaw == 0:
                    obs = np.rot90(obs, k=2, axes=(1, 2))
                elif yaw == 90:
                    obs = np.rot90(obs, k=3, axes=(1, 2))

                # Update inventory
                temp = dict()
                for i in range(9):
                    item = observations[f'Hotbar_{i}_item']
                    size = observations[f'Hotbar_{i}_size']
                    if size == 0:
                        break
                    else:
                        temp[item] = size
                if temp != self.inventory:
                    self.inventory = temp

                break

        return obs

    def log_returns(self):
        """
        Log the current returns as a graph and text file

        Args:
            steps (list): list of global steps after each episode
            returns (list): list of total return of each episode
        """
        box = np.ones(self.log_frequency) / self.log_frequency
        returns_smooth = np.convolve(self.returns, box, mode='same')
        plt.clf()
        plt.plot(self.steps, returns_smooth)
        plt.title('SpeedCrafter')
        plt.ylabel('Return')
        plt.xlabel('Steps')
        plt.savefig('returns.png')

        with open('returns.txt', 'w') as f:
            for step, value in zip(self.steps, self.returns):
                f.write("{}\t{}\n".format(step, value))


if __name__ == '__main__':
    ray.init()
    trainer = sac.SACTrainer(env=SpeedCrafter, config={
        'env_config': {},           # No environment parameters to configure
        'framework': 'torch',       # Use pyotrch instead of tensorflow
        'num_gpus': 1,              # use GPU
        'num_workers': 0
    })

    while True:
        print(trainer.train())