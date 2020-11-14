---
layout: default
title: Status
---

## Summary
For our project, we want to give our agent a recipe or list of resources which the agent must find and collect by exploring the world around it. The agent would be placed in a normally-generated world with a given world seed. The agent would be given limited information about its immediate surroundings in the form of a three-dimensional grid and would have to explore to find additional resources. It would also need to be aware of and react to potential hazards in the area. Our project has applications in problems that involve searching for objects in unfamiliar areas.

## Approach

### Entropy reinforcement maximum learning: soft actor critic (SAC)
<!--
Reward the agent for encountering resource in observation space, touching the block, and collecting the block. Reward shaping will be an extremely important part in training our neural network as we must reward the agent as it gradually gets closer to desired objectives.
-->

We will use entropy reinforcement maximum learning: soft actor critic (SAC), which is an off-policy, independent of the agent’s action algorithm. The agent will try to maximize the expected award as well as entropy. Since the agent tries to maximize the entropy, the agent will take more random actions and therefore is encouraged to explore more possibilities. The algorithm prefers the most random action that receives the highest reward.

Reward functions:
<img src='https://github.com/jhnguyen521/SpeedCrafter/blob/main/img/reward_f.png' title='Reward function' width='' alt='' />
                                                                                                                  

 
H() = entropy measure, α = how important the entropy is (weight of entropy, temperature parameter) 


SAC uses three main network:
<img src='https://github.com/jhnguyen521/SpeedCrafter/blob/main/img/3functions.png' title='threefunctions' width='' alt='' />

 
Soft state value function aims to minimize the mean squared error 
<img src='https://github.com/jhnguyen521/SpeedCrafter/blob/main/img/soft_state.png' title='soft state Q' width='' alt='' />


Soft Q function aims to minimize the soft Bellman residual
<img src='https://github.com/jhnguyen521/SpeedCrafter/blob/main/img/soft_q.png' title='soft state Q' width='' alt='' />

 
Pseudo algorithm

<img src='https://github.com/jhnguyen521/SpeedCrafter/blob/main/img/algorithm.png' title='algorithm' width='' alt='' />




## Evaluation
<!--
The agent will be evaluated on its efficiency in finding the given resources. Every action taken will incur a small negative reward to encourage the agent to complete the task with fewer actions. For example, moving 1 block can have a "reward" of -0.005, while mining a block other than the targeted one can have a larger penalty of -0.01. Taking damage (such as falling or touching lava) will also incur larger penalties to encourage the agent to avoid hazards.

The agent will also be evaluated on its ability to collect resources and fulfill tasks of varying complexities. Simple tasks such as gathering wood would give a lower reward
-->
## Remaining Goals and Challenges

Regarding remaining goals and challenges, we are still deciding what kind of neural network may be best for our application and train the agent using it to gather resources. We also need to implement algorithms to actually use the collected resources and craft the requested item. Reward shaping will definitely be a large challenge in optimizing our neural network because we need to create some method for rewarding the agent for getting closer to certain objectives while being careful about possible ways the agent could take advantage of the reward system while not performing desired actions.

## Resources Used
Resources that were helpful included the following:
* Malmo documentation
External Libraries:
https://github.com/haarnoja/sac

